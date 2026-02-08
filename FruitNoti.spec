# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['FruitNoti.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Tesseract-OCR', 'Tesseract-OCR'),  # Include the whole Tesseract folder
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5', 'PySide6', 'PyQt6', 'PySide2', 'Qt', 'PySide',
        'numpy', 'pandas', 'matplotlib', 'scipy', 'IPython', 'notebook', 
        'jupyter', 'sqlite3', 'test', 'unittest'
    ],
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
    name='FruitNoti',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Set to True if you want a console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
