# Building Releases

This document explains how to build standalone executables for SQLmap GUI on different platforms.

## Prerequisites

- Python 3.8 or higher
- PyInstaller (included in requirements.txt)
- Platform-specific tools as needed

## Local Building

### Windows

1. Open Command Prompt or PowerShell in the project directory
2. Run the build script:
   ```cmd
   build_windows.bat
   ```
3. The executable will be created in `dist/SQLmap-GUI.exe`
4. A zip archive `SQLmap-GUI-windows.zip` can be created for distribution

### Linux

1. Open terminal in the project directory
2. Make the script executable and run it:
   ```bash
   chmod +x build_linux.sh
   ./build_linux.sh
   ```
3. The executable will be created in `dist/SQLmap-GUI`
4. A tar.gz archive `SQLmap-GUI-linux.tar.gz` is automatically created

### macOS

1. Open terminal in the project directory
2. Make the script executable and run it:
   ```bash
   chmod +x build_mac.sh
   ./build_mac.sh
   ```
3. The app bundle will be created in `dist/SQLmap-GUI.app`
4. A zip archive `SQLmap-GUI-macos.zip` is automatically created

## Automated Releases (GitHub Actions)

The project includes a GitHub Actions workflow that automatically builds releases for all platforms when you push a version tag.

### Creating a Release

1. **Tag your commit** with a version number:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **GitHub Actions will automatically**:
   - Build executables for Windows, Linux, and macOS
   - Create a GitHub release
   - Upload all platform binaries
   - Generate release notes

3. **Manual trigger** (if needed):
   - Go to the "Actions" tab in your GitHub repository
   - Select "Build and Release SQLmap GUI"
   - Click "Run workflow"

## Build Configuration

The build process is configured through `sqlmap-gui.spec`:

- **Includes all source files** from `src/` directory
- **Bundles dependencies** like PyQt6, requests, etc.
- **Creates single-file executables** for easy distribution
- **Excludes console window** for cleaner user experience
- **Supports macOS app bundles** with proper metadata

## Troubleshooting Builds

### Common Issues

1. **Missing dependencies**: Ensure all packages in `requirements.txt` are installed
2. **Import errors**: Check `hiddenimports` in the spec file
3. **Missing files**: Verify `datas` section includes all necessary resources
4. **Console errors**: Temporarily set `console=True` in the spec file for debugging

### Platform-Specific Notes

**Windows:**
- UPX compression is enabled for smaller file size
- No console window by default
- Antivirus may flag the executable (false positive)

**Linux:**
- Built executable should work on most distributions
- May need to install additional system libraries on minimal systems
- Check file permissions after extraction

**macOS:**
- Creates proper .app bundle structure
- Users need to right-click → Open for unsigned apps
- Apple Silicon and Intel compatibility

## Distribution

The built executables are completely standalone and include:
- Python interpreter
- All Python dependencies
- Application source code
- Required data files

Users only need to:
1. Download the appropriate archive for their platform
2. Extract the files
3. Run the executable
4. Have SQLmap installed separately on their system

## File Sizes

Typical file sizes for releases:
- Windows: ~50-80MB (compressed: ~20-25MB)
- Linux: ~50-70MB (compressed: ~20-25MB)  
- macOS: ~60-90MB (compressed: ~25-30MB)

The larger size is due to bundling the Python interpreter and all dependencies for a completely portable application.