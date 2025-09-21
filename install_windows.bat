@echo off
REM SQLmap GUI Windows Installer
REM Run this script to automatically set up everything needed for SQLmap GUI

echo ============================================
echo    SQLmap GUI Windows Installer
echo ============================================
echo.
echo This installer will:
echo - Check and install Python if needed
echo - Download and setup SQLmap
echo - Install required Python packages
echo - Create desktop shortcuts
echo.

set /p "continue=Do you want to continue? (Y/N): "
if /i not "%continue%"=="Y" (
    echo Installation cancelled.
    pause
    exit /b 0
)

echo.
echo Starting installation...

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "DESKTOP=%USERPROFILE%\Desktop"

REM Run the main setup script
call "%SCRIPT_DIR%start_gui.bat"

if %errorlevel% neq 0 (
    echo.
    echo Installation encountered errors.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Creating desktop shortcuts...

REM Create batch file for easy access
set "LAUNCHER=%SCRIPT_DIR%SQLmap_GUI.bat"
echo @echo off > "%LAUNCHER%"
echo cd /d "%SCRIPT_DIR%" >> "%LAUNCHER%"
echo call start_gui.bat >> "%LAUNCHER%"

REM Create desktop shortcut
set "SHORTCUT=%DESKTOP%\SQLmap GUI.lnk"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%LAUNCHER%'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'SQLmap GUI - SQL Injection Testing Tool'; $Shortcut.Save()"

if exist "%SHORTCUT%" (
    echo ✓ Desktop shortcut created
) else (
    echo ✗ Failed to create desktop shortcut
)

echo.
echo ============================================
echo Installation completed successfully!
echo.
echo You can now:
echo 1. Double-click "SQLmap GUI" on your desktop
echo 2. Run start_gui.bat from this directory
echo 3. Run start_gui.ps1 from PowerShell
echo.
echo The GUI will automatically:
echo - Detect and use your installed Python
echo - Use the downloaded SQLmap
echo - Manage dependencies in a virtual environment
echo.
pause