# SQLmap GUI Launcher Script for Windows (PowerShell)
# This script automatically installs Python and SQLmap if needed

param(
    [switch]$Force,
    [string]$PythonVersion = "3.12.0"
)

# Set execution policy for current session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

Write-Host "Starting SQLmap GUI for Windows..." -ForegroundColor Green
Write-Host ""

# Variables
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir = Join-Path $ScriptDir ".venv"
$SqlmapDir = Join-Path $ScriptDir "sqlmap-master"
$PythonUrl = "https://www.python.org/ftp/python/$PythonVersion/python-$PythonVersion-amd64.exe"
$SqlmapUrl = "https://github.com/sqlmapproject/sqlmap/archive/master.zip"
$TempDir = Join-Path $env:TEMP "sqlmap-gui-setup"

# Function to check if command exists
function Test-Command {
    param($Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Function to download file with progress
function Download-File {
    param($Url, $OutputPath)
    try {
        Write-Host "Downloading from $Url..." -ForegroundColor Yellow
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($Url, $OutputPath)
        return $true
    }
    catch {
        Write-Host "Download failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Check if Python is installed
Write-Host "Checking for Python installation..." -ForegroundColor Cyan

$PythonCmd = $null
if (Test-Command "python") {
    $PythonCmd = "python"
    Write-Host "✓ Python found" -ForegroundColor Green
}
elseif (Test-Command "py") {
    $PythonCmd = "py"
    Write-Host "✓ Python launcher found" -ForegroundColor Green
}
else {
    Write-Host "✗ Python not found" -ForegroundColor Red
    $InstallPython = $true
}

# Check Python version if found
if ($PythonCmd -and -not $Force) {
    Write-Host "Checking Python version..." -ForegroundColor Cyan
    try {
        $VersionOutput = & $PythonCmd --version 2>&1
        $CurrentVersion = ($VersionOutput -split " ")[1]
        Write-Host "Current Python version: $CurrentVersion" -ForegroundColor Yellow
        
        $Version = [Version]$CurrentVersion
        if ($Version.Major -ge 3 -and $Version.Minor -ge 8) {
            Write-Host "✓ Python version is compatible (3.8+)" -ForegroundColor Green
        }
        else {
            Write-Host "✗ Python version is too old (need 3.8+)" -ForegroundColor Red
            $InstallPython = $true
        }
    }
    catch {
        Write-Host "✗ Failed to check Python version" -ForegroundColor Red
        $InstallPython = $true
    }
}

# Install Python if needed
if ($InstallPython -or $Force) {
    Write-Host ""
    Write-Host "Installing Python $PythonVersion..." -ForegroundColor Yellow
    Write-Host "This may take a few minutes..." -ForegroundColor Yellow
    
    # Create temp directory
    if (Test-Path $TempDir) {
        Remove-Item $TempDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
    
    $InstallerPath = Join-Path $TempDir "python-installer.exe"
    
    # Download Python installer
    if (Download-File $PythonUrl $InstallerPath) {
        Write-Host "Installing Python..." -ForegroundColor Yellow
        
        # Install Python silently
        $InstallArgs = @(
            "/quiet",
            "InstallAllUsers=0",
            "PrependPath=1",
            "Include_test=0",
            "AssociateFiles=1",
            "Shortcuts=1"
        )
        
        $Process = Start-Process -FilePath $InstallerPath -ArgumentList $InstallArgs -Wait -PassThru
        
        if ($Process.ExitCode -eq 0) {
            Write-Host "✓ Python installed successfully" -ForegroundColor Green
            
            # Refresh environment variables
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            
            # Update Python command
            if (Test-Command "python") {
                $PythonCmd = "python"
            }
            elseif (Test-Command "py") {
                $PythonCmd = "py"
            }
        }
        else {
            Write-Host "✗ Python installation failed with exit code: $($Process.ExitCode)" -ForegroundColor Red
            Write-Host "Please install Python manually from https://python.org" -ForegroundColor Yellow
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
    else {
        Write-Host "✗ Failed to download Python installer" -ForegroundColor Red
        Write-Host "Please download and install Python manually from https://python.org" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Clean up
    if (Test-Path $TempDir) {
        Remove-Item $TempDir -Recurse -Force
    }
}

# Check for SQLmap
Write-Host ""
Write-Host "Checking for SQLmap..." -ForegroundColor Cyan

$SqlmapFound = $false

# Check if sqlmap is in PATH
if (Test-Command "sqlmap") {
    Write-Host "✓ SQLmap found in PATH" -ForegroundColor Green
    $SqlmapFound = $true
}
# Check if sqlmap.py exists in script directory
elseif (Test-Path (Join-Path $ScriptDir "sqlmap.py")) {
    Write-Host "✓ SQLmap found in script directory" -ForegroundColor Green
    $SqlmapFound = $true
}
# Check if sqlmap-master directory exists
elseif (Test-Path (Join-Path $SqlmapDir "sqlmap.py")) {
    Write-Host "✓ SQLmap found in sqlmap-master directory" -ForegroundColor Green
    $SqlmapFound = $true
}
else {
    Write-Host "✗ SQLmap not found" -ForegroundColor Red
}

# Install SQLmap if needed
if (-not $SqlmapFound -or $Force) {
    Write-Host ""
    Write-Host "Installing SQLmap..." -ForegroundColor Yellow
    
    # Create temp directory
    if (Test-Path $TempDir) {
        Remove-Item $TempDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
    
    $SqlmapZip = Join-Path $TempDir "sqlmap.zip"
    
    # Download SQLmap
    if (Download-File $SqlmapUrl $SqlmapZip) {
        Write-Host "Extracting SQLmap..." -ForegroundColor Yellow
        
        try {
            Expand-Archive -Path $SqlmapZip -DestinationPath $TempDir -Force
            
            $ExtractedDir = Join-Path $TempDir "sqlmap-master"
            if (Test-Path $ExtractedDir) {
                # Remove existing sqlmap directory if it exists
                if (Test-Path $SqlmapDir) {
                    Remove-Item $SqlmapDir -Recurse -Force
                }
                
                # Move to script directory
                Move-Item $ExtractedDir $SqlmapDir
                Write-Host "✓ SQLmap installed successfully" -ForegroundColor Green
            }
            else {
                Write-Host "✗ Failed to extract SQLmap" -ForegroundColor Red
                Read-Host "Press Enter to exit"
                exit 1
            }
        }
        catch {
            Write-Host "✗ Failed to extract SQLmap: $($_.Exception.Message)" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
    else {
        Write-Host "✗ Failed to download SQLmap" -ForegroundColor Red
        Write-Host "Please download SQLmap manually from https://github.com/sqlmapproject/sqlmap" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Clean up
    if (Test-Path $TempDir) {
        Remove-Item $TempDir -Recurse -Force
    }
}

# Setup virtual environment
Write-Host ""
Write-Host "Setting up virtual environment..." -ForegroundColor Cyan

if (Test-Path (Join-Path $VenvDir "Scripts\Activate.ps1")) {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}
else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    
    try {
        & $PythonCmd -m venv $VenvDir
        
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create virtual environment"
        }
        
        Write-Host "✓ Virtual environment created" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        Write-Host "Trying to install virtualenv..." -ForegroundColor Yellow
        
        & $PythonCmd -m pip install virtualenv
        & $PythonCmd -m virtualenv $VenvDir
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
        
        Write-Host "✓ Virtual environment created with virtualenv" -ForegroundColor Green
    }
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow

$ActivateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
if (Test-Path $ActivateScript) {
    & $ActivateScript
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
}
else {
    Write-Host "✗ Failed to find activation script" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan

$RequirementsFile = Join-Path $ScriptDir "requirements.txt"
if (-not (Test-Path $RequirementsFile)) {
    Write-Host "Creating requirements.txt..." -ForegroundColor Yellow
    $Requirements = @(
        "PyQt6>=6.5.0",
        "psutil>=5.9.0",
        "requests>=2.28.0"
    )
    $Requirements | Out-File -FilePath $RequirementsFile -Encoding UTF8
}

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
python -m pip install -r $RequirementsFile

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install dependencies from requirements.txt" -ForegroundColor Red
    Write-Host "Trying individual installations..." -ForegroundColor Yellow
    
    python -m pip install PyQt6
    python -m pip install psutil
    python -m pip install requests
}

# Verify PyQt6 installation
Write-Host "Verifying PyQt6 installation..." -ForegroundColor Yellow
python -c "import PyQt6" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
}
else {
    Write-Host "✗ Failed to import PyQt6" -ForegroundColor Red
    Write-Host "Trying alternative installation..." -ForegroundColor Yellow
    
    python -m pip install PyQt6 --index-url https://pypi.org/simple/
    python -c "import PyQt6" 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to install PyQt6. Please install manually." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    else {
        Write-Host "✓ PyQt6 installed successfully" -ForegroundColor Green
    }
}

# Launch GUI
Write-Host ""
Write-Host "Launching SQLmap GUI..." -ForegroundColor Green
Write-Host ""

$MainScript = Join-Path $ScriptDir "main.py"
if (Test-Path $MainScript) {
    python $MainScript
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "✗ SQLmap GUI encountered an error" -ForegroundColor Red
        Write-Host "Check the error messages above for details" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
    }
    else {
        Write-Host ""
        Write-Host "✓ SQLmap GUI closed successfully" -ForegroundColor Green
    }
}
else {
    Write-Host "✗ main.py not found in script directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Press Enter to exit..." -ForegroundColor Yellow
Read-Host