# GitHub Release Upload Guide

## 📍 File Locations

All release files are located in: `/home/devil/SQLmap-GUI/`

### Release Files:
1. **SQLmap-GUI-linux.tar.gz** (97MB) - Linux executable
2. **SQLmap-GUI-macOS.tar.gz** (97MB) - macOS application bundle
3. **checksums.txt** - SHA256 verification file
4. **RELEASE_NOTES.md** - Release documentation

## 🚀 GitHub Release Steps

### 1. Create New Release
1. Go to your GitHub repository: `https://github.com/nanragav/SQLmap-GUI`
2. Click "Releases" (usually in the right sidebar)
3. Click "Create a new release"

### 2. Tag and Title
- **Tag version**: `v1.0.0`
- **Release title**: `SQLmap GUI v1.0.0 - Cross-Platform Release`

### 3. Release Description
Copy and paste the content from `RELEASE_NOTES.md` or use this summary:

```markdown
# SQLmap GUI v1.0.0

Cross-platform GUI for SQLmap with support for Linux and macOS.

## 📦 Downloads
- **Linux**: SQLmap-GUI-linux.tar.gz
- **macOS**: SQLmap-GUI-macOS.tar.gz

## 🔧 Installation
### Linux
```bash
tar -xzf SQLmap-GUI-linux.tar.gz
./SQLmap-GUI/SQLmap-GUI
```

### macOS
1. Extract SQLmap-GUI-macOS.tar.gz
2. Copy SQLmap-GUI.app to Applications
3. Right-click → Open (first time only)

## 📋 Requirements
- SQLmap installed and in PATH
- Python 3.8+
- Linux: Ubuntu 18.04+ or equivalent
- macOS: 10.14+ (Mojave or newer)

## 🔒 Verification
```bash
sha256sum -c checksums.txt
```
```

### 4. Upload Files
Drag and drop these files into the release:
- `SQLmap-GUI-linux.tar.gz`
- `SQLmap-GUI-macOS.tar.gz`
- `checksums.txt`

### 5. Pre-release Settings
- ✅ Check "Set as the latest release" (if this is your latest version)
- ⚠️ Consider checking "Set as a pre-release" if this is a beta/testing version

### 6. Publish
Click "Publish release"

## 📊 File Checksums

**SHA256 Checksums:**
- SQLmap-GUI-linux.tar.gz: `6d2b89b45df2b357b10b6e37299c60a8ff8c487c297abefb0cc243b44ce33de5`
- SQLmap-GUI-macOS.tar.gz: `d86ffdacca7e8ef1b0d88fc84059ab2d0d7da86c302956d40f37192b19259162`

## 💡 Tips

1. **File Order**: Upload the files in this order for better organization:
   - SQLmap-GUI-linux.tar.gz
   - SQLmap-GUI-macOS.tar.gz
   - checksums.txt

2. **Description**: The release description supports Markdown, so you can format it nicely.

3. **Assets**: The uploaded files will appear in the "Assets" section below the description.

4. **Download Stats**: GitHub will track download statistics for each file.

## 🔍 Post-Release Verification

After publishing, verify:
1. All files are uploaded correctly
2. Download links work
3. Checksums match
4. Release appears in the releases list

## 🎯 Future Releases

For future releases:
1. Update version numbers in the code
2. Re-run the build scripts
3. Update release notes
4. Create new tag (v1.0.1, v1.1.0, etc.)
