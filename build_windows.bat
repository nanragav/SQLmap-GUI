@echo off
echo Building SQLmap GUI for Windows...

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Clean previous builds
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

REM Build executable
echo Building executable...
pyinstaller sqlmap_gui.spec

REM Check if build was successful
if exist "dist\SQLmap-GUI\SQLmap-GUI.exe" (
    echo.
    echo ✅ Build successful!
    echo Executable created: dist\SQLmap-GUI\SQLmap-GUI.exe
    echo.
    echo To distribute:
    echo 1. Zip the entire dist\SQLmap-GUI folder
    echo 2. Upload to GitHub releases
) else (
    echo.
    echo ❌ Build failed!
    echo Check the output above for errors.
)

pause