# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Get application info
app_name = 'SQLmap-GUI'
main_script = 'main.py'

# Collect all data files and submodules
datas = []
datas += collect_data_files('PyQt6')

# Add source code directories
datas += [('src', 'src')]

# Collect hidden imports
hiddenimports = []
hiddenimports += collect_submodules('PyQt6')
hiddenimports += [
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'configparser',
    'psutil',
    'colorlog',
    'requests',
    'pathlib2',
    'qdarkstyle'
]

# Platform-specific settings
if sys.platform == 'win32':
    icon_file = None  # Add .ico file path if you have an icon
    console = False
elif sys.platform == 'darwin':
    icon_file = None  # Add .icns file path if you have an icon
    console = False
else:  # Linux
    icon_file = None  # Add .png file path if you have an icon
    console = False

a = Analysis(
    [main_script],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=console,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name,
)

# For macOS app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name=f'{app_name}.app',
        icon=icon_file,
        bundle_identifier='com.nanragav.sqlmap-gui',
        info_plist={
            'CFBundleName': app_name,
            'CFBundleDisplayName': app_name,
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSHighResolutionCapable': True,
        },
    )