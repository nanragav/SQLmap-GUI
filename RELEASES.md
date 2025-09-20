# 🚀 Complete GitHub Release Guide for SQLmap GUI

This guide explains how to create and manage releases with pre-built binaries for Windows, Linux, and macOS.

## 📋 Release Process Overview

### Method 1: Automated Release (Recommended)

The easiest way to create a release with binaries for all platforms:

```bash
# 1. Ensure all changes are committed and pushed
git add .
git commit -m "Prepare for v1.0.0 release"
git push origin main

# 2. Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

**What happens automatically:**
1. GitHub Actions detects the new tag
2. Builds executables for Windows, Linux, and macOS
3. Creates a GitHub release
4. Uploads all binaries to the release
5. Generates release notes

### Method 2: Manual Release

If you prefer manual control or the automated process fails:

#### Step 1: Build Binaries Locally

**Windows:**
```cmd
build_windows.bat
```

**Linux:**
```bash
./build_linux.sh
```

**macOS:**
```bash
./build_mac.sh
```

#### Step 2: Create Archives

**Windows:**
```cmd
# In PowerShell
Compress-Archive -Path dist\SQLmap-GUI -DestinationPath SQLmap-GUI-v1.0.0-windows.zip
```

**Linux:**
```bash
tar -czf SQLmap-GUI-v1.0.0-linux.tar.gz -C dist SQLmap-GUI
```

**macOS:**
```bash
cd dist
zip -r ../SQLmap-GUI-v1.0.0-macos.zip SQLmap-GUI.app
cd ..
```

#### Step 3: Create GitHub Release

1. Go to your repository on GitHub
2. Click **"Releases"** → **"Create a new release"**
3. Click **"Choose a tag"** → Type `v1.0.0` → **"Create new tag"**
4. **Release title:** `SQLmap GUI v1.0.0`
5. **Description:** Use the template below
6. **Attach files:** Upload all three archive files
7. Click **"Publish release"**

## 📝 Release Notes Template

```markdown
## 🚀 SQLmap GUI v1.0.0

### 📥 Download and Installation

Choose the appropriate version for your operating system:

#### Windows
- **Download:** `SQLmap-GUI-v1.0.0-windows.zip`
- **Installation:** 
  1. Extract the ZIP file
  2. Run `SQLmap-GUI.exe`
  3. No additional installation required!

#### Linux
- **Download:** `SQLmap-GUI-v1.0.0-linux.tar.gz`
- **Installation:**
  ```bash
  tar -xzf SQLmap-GUI-v1.0.0-linux.tar.gz
  cd SQLmap-GUI
  chmod +x SQLmap-GUI
  ./SQLmap-GUI
  ```

#### macOS
- **Download:** `SQLmap-GUI-v1.0.0-macos.zip`
- **Installation:**
  1. Extract the ZIP file
  2. Right-click `SQLmap-GUI.app` and select "Open"
  3. Click "Open" when macOS asks for permission

### 📋 Requirements

- **SQLmap must be installed** on your system
- **No Python or other dependencies** required for these binaries
- **Windows 10+, Linux (most distributions), macOS 10.14+**

### ✨ Features

- Full SQLmap GUI interface
- Cross-platform support
- No Python installation required
- Standalone executable
- All SQLmap features accessible through GUI

### 🐛 Known Issues

- Antivirus software may flag the executable (false positive)
- First startup might be slower on some systems

### 📞 Support

- **Issues:** [GitHub Issues](https://github.com/nanragav/SQLmap-GUI/issues)
- **Documentation:** [README.md](https://github.com/nanragav/SQLmap-GUI/blob/main/README.md)
```

## 🔄 Updating Releases

### For Bug Fixes (Patch Version)
```bash
git tag v1.0.1
git push origin v1.0.1
```

### For New Features (Minor Version)
```bash
git tag v1.1.0
git push origin v1.1.0
```

### For Breaking Changes (Major Version)
```bash
git tag v2.0.0
git push origin v2.0.0
```

## ⚙️ GitHub Actions Workflow

The automated release process uses `.github/workflows/build-release.yml`:

### Triggers
- **Tag push:** Any tag starting with `v` (e.g., v1.0.0, v2.1.3)
- **Manual trigger:** Can be run manually from GitHub Actions tab

### Build Matrix
- **Windows:** `windows-latest` with Python 3.11
- **Linux:** `ubuntu-latest` with Python 3.11  
- **macOS:** `macos-latest` with Python 3.11

### Outputs
- **Windows:** `SQLmap-GUI-windows.zip`
- **Linux:** `SQLmap-GUI-linux.tar.gz`
- **macOS:** `SQLmap-GUI-macos.zip`

## 🚨 Troubleshooting

### Workflow Fails

**Check the Actions tab:**
1. Go to your repository
2. Click **"Actions"**
3. Click on the failed workflow
4. Check the error logs

**Common issues:**
- Missing dependencies in `requirements.txt`
- Incorrect file paths in workflow
- PyInstaller build errors

### Manual Release Required

If automated release fails:
1. Build binaries locally on each platform
2. Create archives manually
3. Upload to GitHub release manually

### Version Conflicts

If you need to recreate a release:
```bash
# Delete tag locally and remotely
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0

# Delete the release on GitHub (go to Releases page)

# Create new tag
git tag v1.0.0
git push origin v1.0.0
```

## 📊 Release Checklist

Before creating a release:

- [ ] All code changes committed and pushed
- [ ] Version numbers updated in relevant files
- [ ] Build scripts tested locally
- [ ] Documentation updated
- [ ] Release notes prepared
- [ ] Previous releases tested on target platforms

After release creation:

- [ ] All three binaries uploaded successfully
- [ ] Download links work correctly
- [ ] Binaries run on clean systems
- [ ] Release announcement posted (if applicable)
- [ ] Documentation reflects new version

## 🎯 Best Practices

1. **Test before release:** Always test builds locally
2. **Semantic versioning:** Use proper version numbering
3. **Clear release notes:** Explain what's new and what's fixed
4. **Platform testing:** Test on actual target systems
5. **Documentation:** Keep README and docs up to date
6. **Backup:** Keep local copies of release files

## 📈 Analytics

Track release effectiveness:
- Download counts per platform
- Issue reports related to specific versions
- User feedback on installation process

This information helps improve future releases and identify popular platforms.

---

**Need help?** Create an issue or check the main README.md for more information.