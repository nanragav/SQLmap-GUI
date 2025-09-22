@echo off
setlocal enabledelayedexpansion

REM SQLmap GUI Launcher Script for Windows
REM This script automatically installs Python and SQLmap if needed

echo Starting SQLmap GUI for Windows...
echo.

REM Set variables
set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%.venv"

REM Check if Python is installed
echo Checking for Python installation...
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found
    set "PYTHON_CMD=python"
    goto :check_python_version
) else (
    where py >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Python launcher found
        set "PYTHON_CMD=py"
        goto :check_python_version
    ) else (
        echo [ERROR] Python not found
        goto :install_python
    )
)

:check_python_version
echo Checking Python version...
for /f "tokens=2" %%i in ('!PYTHON_CMD! --version 2^>^&1') do set "CURRENT_VERSION=%%i"
echo Current Python version: !CURRENT_VERSION!

for /f "tokens=1,2 delims=." %%a in ("!CURRENT_VERSION!") do (
    set "MAJOR=%%a"
    set "MINOR=%%b"
)

if !MAJOR! geq 3 if !MINOR! geq 8 (
    echo [OK] Python version is compatible (3.8+)
    goto :check_sqlmap
) else (
    echo [ERROR] Python version is too old (need 3.8+)
    goto :install_python
)

:install_python
echo.
echo Installing Python !PYTHON_VERSION!...
echo This may take a few minutes...

REM Create temp directory
if not exist "%TEMP%\sqlmap-gui-setup" mkdir "%TEMP%\sqlmap-gui-setup"
cd /d "%TEMP%\sqlmap-gui-setup"

REM Download Python installer
echo Downloading Python installer...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile 'python-installer.exe'}"

if not exist "python-installer.exe" (
    echo ✗ Failed to download Python installer
    echo Please download and install Python manually from https://python.org
    pause
    exit /b 1
)

REM Install Python silently
echo Installing Python...
python-installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0

REM Wait for installation to complete
timeout /t 10 /nobreak >nul

REM Refresh environment variables
call :refresh_env

REM Verify installation
call :check_command python
if %errorlevel% equ 0 (
    echo ✓ Python installed successfully
    set "PYTHON_CMD=python"
) else (
    call :check_command py
    if %errorlevel% equ 0 (
        echo ✓ Python installed successfully
        set "PYTHON_CMD=py"
    ) else (
        echo ✗ Python installation failed
        echo Please install Python manually and run this script again
        pause
        exit /b 1
    )
)

REM Clean up
cd /d "%SCRIPT_DIR%"
rmdir /s /q "%TEMP%\sqlmap-gui-setup" 2>nul

:check_sqlmap
echo.
echo Checking for SQLmap...

REM Check if sqlmap is in PATH
where sqlmap >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] SQLmap found in PATH
    goto :setup_venv
)

REM Check if sqlmap exists in script directory
if exist "%SCRIPT_DIR%sqlmap.py" (
    echo [OK] SQLmap found in script directory
    goto :setup_venv
)

REM Check if sqlmap-master directory exists
if exist "%SQLMAP_DIR%\sqlmap.py" (
    echo [OK] SQLmap found in sqlmap-master directory
    goto :setup_venv
)

echo [ERROR] SQLmap not found
goto :install_sqlmap

:install_sqlmap
echo.
echo Installing SQLmap...

REM Create temp directory
if not exist "%TEMP%\sqlmap-gui-setup" mkdir "%TEMP%\sqlmap-gui-setup"
cd /d "%TEMP%\sqlmap-gui-setup"

REM Download SQLmap
echo Downloading SQLmap...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%SQLMAP_URL%' -OutFile 'sqlmap.zip'}"

if not exist "sqlmap.zip" (
    echo ✗ Failed to download SQLmap
    echo Please download SQLmap manually from https://github.com/sqlmapproject/sqlmap
    pause
    exit /b 1
)

REM Extract SQLmap
echo Extracting SQLmap...
powershell -Command "Expand-Archive -Path 'sqlmap.zip' -DestinationPath '.' -Force"

REM Move to script directory
if exist "sqlmap-master" (
    echo Moving SQLmap to script directory...
    xcopy /E /I /Y "sqlmap-master" "%SCRIPT_DIR%sqlmap-master\"
    echo ✓ SQLmap installed successfully
) else (
    echo ✗ Failed to extract SQLmap
    pause
    exit /b 1
)

REM Clean up
cd /d "%SCRIPT_DIR%"
rmdir /s /q "%TEMP%\sqlmap-gui-setup" 2>nul

:setup_venv
echo.
echo Setting up virtual environment...

REM Check if virtual environment exists
if exist "%VENV_DIR%\Scripts\activate.bat" (
    echo ✓ Virtual environment already exists
    goto :activate_venv
)

REM Create virtual environment
echo Creating virtual environment...
!PYTHON_CMD! -m venv "%VENV_DIR%"

if %errorlevel% neq 0 (
    echo ✗ Failed to create virtual environment
    echo Trying to install venv module...
    !PYTHON_CMD! -m pip install virtualenv
    !PYTHON_CMD! -m virtualenv "%VENV_DIR%"
    
    if %errorlevel% neq 0 (
        echo ✗ Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo ✓ Virtual environment created

:activate_venv
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

if %errorlevel% neq 0 (
    echo ✗ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment activated

:install_dependencies
echo.
echo Installing Python dependencies...

REM Check if requirements.txt exists
if not exist "%SCRIPT_DIR%requirements.txt" (
    echo Creating requirements.txt...
    echo PyQt6>=6.5.0> "%SCRIPT_DIR%requirements.txt"
    echo psutil>=5.9.0>> "%SCRIPT_DIR%requirements.txt"
    echo requests>=2.28.0>> "%SCRIPT_DIR%requirements.txt"
)

REM Install dependencies
python -m pip install --upgrade pip
python -m pip install -r "%SCRIPT_DIR%requirements.txt"

if %errorlevel% neq 0 (
    echo ✗ Failed to install dependencies
    echo Trying individual installations...
    python -m pip install PyQt6
    python -m pip install psutil
    python -m pip install requests
)

REM Verify PyQt6 installation
python -c "import PyQt6" 2>nul
if %errorlevel% equ 0 (
    echo ✓ Dependencies installed successfully
) else (
    echo ✗ Failed to install PyQt6
    echo Trying alternative installation...
    python -m pip install PyQt6 --index-url https://pypi.org/simple/
    
    python -c "import PyQt6" 2>nul
    if %errorlevel% neq 0 (
        echo ✗ Failed to install PyQt6. Please install manually.
        pause
        exit /b 1
    )
)

:launch_gui
echo.
echo Launching SQLmap GUI...
echo.

REM Start the GUI
python "%SCRIPT_DIR%main.py"

REM Check if GUI ran successfully
if %errorlevel% neq 0 (
    echo.
    echo ✗ SQLmap GUI encountered an error
    echo Check the error messages above for details
    pause
) else (
    echo.
    echo ✓ SQLmap GUI closed successfully
)

goto :end

:refresh_env
REM Refresh environment variables
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH') do set "SYSTEM_PATH=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USER_PATH=%%b"
if defined USER_PATH (
    set "PATH=%SYSTEM_PATH%;%USER_PATH%"
) else (
    set "PATH=%SYSTEM_PATH%"
)
exit /b

:end
echo.
echo Press any key to exit...
pause >nul