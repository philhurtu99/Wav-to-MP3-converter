# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import sys

block_cipher = None
ROOT = Path(SPECPATH).parent


a = Analysis(
    [str(ROOT / 'packaging' / 'entrypoints' / 'gui_entry.py')],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[],
    hiddenimports=['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets'],
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
    [],
    exclude_binaries=True,
    name='Convertisseur WAV vers MP3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Convertisseur WAV vers MP3',
)
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='Convertisseur WAV vers MP3.app',
        icon=None,
        bundle_identifier='local.philippeclement.wav-to-mp3',
        info_plist={
            'CFBundleDisplayName': 'Convertisseur WAV vers MP3',
            'CFBundleShortVersionString': '0.1.0',
            'CFBundleVersion': '0.1.0',
            'NSHighResolutionCapable': True,
        },
    )
