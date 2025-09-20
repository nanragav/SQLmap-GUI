# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Get the current directory and src path
current_dir = Path(__file__).parent
src_path = current_dir / 'src'

block_cipher = None

# Define additional data files to include
added_files = [
    (str(src_path / 'gui'), 'src/gui'),
    (str(src_path / 'core'), 'src/core'),
    (str(src_path / 'utils'), 'src/utils'),
    (str(current_dir / 'README.md'), '.'),
    (str(current_dir / 'LICENSE'), '.'),
]

# Define hidden imports for PyQt6 and other dependencies
hidden_imports = [
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'configparser',
    'psutil',
    'requests',
    'pathlib',
    'json',
    'subprocess',
    'threading',
    'logging',
    'colorlog',
    'qdarkstyle',
]

a = Analysis(
    ['main.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SQLmap-GUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want console for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path here if you have one
)

# For macOS, create an app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='SQLmap-GUI.app',
        icon=None,  # Add icon file path here if you have one
        bundle_identifier='com.nanragav.sqlmap-gui',
        info_plist={
            'CFBundleName': 'SQLmap GUI',
            'CFBundleDisplayName': 'SQLmap GUI',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleIdentifier': 'com.nanragav.sqlmap-gui',
            'NSHighResolutionCapable': 'True',
        },
    )