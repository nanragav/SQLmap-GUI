# Building and Releasing SQLmap GUI

This document explains how to build standalone executables for Windows, Linux, and macOS, and how to create releases.

## Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment with dependencies installed
- SQLmap installed on the system

## Building Standalone Executables

### Windows

1. Open Command Prompt or PowerShell
2. Navigate to the project directory
3. Run the build script:
   ```cmd
   build_windows.bat
   ```
4. The executable will be created in `dist\SQLmap-GUI\SQLmap-GUI.exe`

### Linux

1. Open terminal
2. Navigate to the project directory
3. Make the script executable and run:
   ```bash
   chmod +x build_linux.sh
   ./build_linux.sh
   ```
4. The executable will be created in `dist/SQLmap-GUI/SQLmap-GUI`

### macOS

1. Open terminal
2. Navigate to the project directory
3. Make the script executable and run:
   ```bash
   chmod +x build_mac.sh
   ./build_mac.sh
   ```
4. The app bundle will be created in `dist/SQLmap-GUI.app`

## Manual Building

If you prefer to build manually or customize the process:

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install PyInstaller if not already installed
pip install PyInstaller==6.16.0

# Build the executable
pyinstaller sqlmap_gui.spec

# The output will be in the dist/ directory
```

## Distribution Structure

After building, you'll get the following structure:

### Windows
```
dist/
└── SQLmap-GUI/
    ├── SQLmap-GUI.exe     # Main executable
    └── _internal/         # Dependencies and libraries
```

### Linux
```
dist/
└── SQLmap-GUI/
    ├── SQLmap-GUI         # Main executable
    └── _internal/         # Dependencies and libraries
```

### macOS
```
dist/
└── SQLmap-GUI.app/        # macOS app bundle
    └── Contents/
        ├── MacOS/
        ├── Resources/
        └── Info.plist
```

## Creating Releases

### Manual Release Process

1. **Build for all platforms** (you'll need access to each OS):
   - Windows: Run `build_windows.bat`
   - Linux: Run `build_linux.sh` 
   - macOS: Run `build_mac.sh`

2. **Create archives**:
   - Windows: `SQLmap-GUI-v1.0.0-windows.zip`
   - Linux: `SQLmap-GUI-v1.0.0-linux.tar.gz`
   - macOS: `SQLmap-GUI-v1.0.0-mac.dmg` or `.zip`

3. **Upload to GitHub**:
   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Tag version (e.g., v1.0.0)
   - Upload the archives
   - Write release notes

### Automated Release (GitHub Actions)

The project includes GitHub Actions workflow (`.github/workflows/release.yml`) that automatically builds and releases executables when you push a tag:

```bash
# Create and push a new tag
git tag v1.0.0
git push origin v1.0.0
```

This will trigger the workflow to:
1. Build executables for Windows, Linux, and macOS
2. Create a new GitHub release
3. Upload all executables to the release

## Testing Releases

Before distributing, test each executable:

### Windows
```cmd
# Navigate to the executable
cd dist\SQLmap-GUI

# Run the executable
SQLmap-GUI.exe
```

### Linux
```bash
# Navigate to the executable
cd dist/SQLmap-GUI

# Make executable if needed
chmod +x SQLmap-GUI

# Run the executable
./SQLmap-GUI
```

### macOS
```bash
# Open the app bundle
open dist/SQLmap-GUI.app
```

## Release Checklist

- [ ] All builds complete without errors
- [ ] Executables run on clean systems (without Python installed)
- [ ] GUI loads correctly
- [ ] SQLmap integration works
- [ ] All tabs and features functional
- [ ] File operations work correctly
- [ ] Version number updated in code
- [ ] Release notes written
- [ ] Archives created with proper naming
- [ ] GitHub release created
- [ ] Documentation updated

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Ensure all required packages are in requirements.txt
2. **Import errors**: Check the hiddenimports list in sqlmap_gui.spec
3. **Large file size**: Consider using UPX compression (enabled by default)
4. **Antivirus false positives**: This is common with PyInstaller executables

### Reducing File Size

- Use `--exclude-module` for unused modules
- Enable UPX compression (default in spec file)
- Remove unnecessary PyQt6 modules from hiddenimports

### Security Considerations

- Executables may trigger antivirus warnings (false positives)
- Consider code signing for official releases
- Test on multiple systems before release

## Version Management

Update version numbers in:
- `sqlmap_gui.spec` (for macOS app bundle)
- `src/utils/config.py` (if version is stored there)
- `README.md`
- Release tags and notes