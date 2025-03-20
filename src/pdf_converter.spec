# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Caminhos importantes
WORKSPACE_PATH = os.path.abspath(os.path.join(SPECPATH, '..'))
SRC_PATH = os.path.join(WORKSPACE_PATH, 'src')
RESOURCES_PATH = os.path.join(WORKSPACE_PATH, 'resources')

# Arquivos de dados
datas = [
    (RESOURCES_PATH, 'resources'),
    ('C:\\Program Files\\Tesseract-OCR', 'Tesseract-OCR'),
    ('C:\\Program Files\\poppler\\Library\\bin', 'poppler')
]

# Coletando arquivos adicionais das bibliotecas
datas += collect_data_files('pytesseract')

a = Analysis(
    [os.path.join(SRC_PATH, 'main.py')],
    pathex=[SRC_PATH],
    binaries=[],
    datas=datas,
    hiddenimports=['PIL._tkinter_finder'],
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
    name='Conversor de PDF',
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
    name='Conversor de PDF',
) 