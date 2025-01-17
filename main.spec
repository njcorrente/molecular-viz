# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['molecular_viz/main.py'],
    pathex=['molecular_viz'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'models.potential_models',
        'frames.parameter_frame',
        'frames.plot_frame',
        'frames.molecule_canvas',
        'pkg_resources.py2_warn',
        'numpy',
        'matplotlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['backports'],  # Exclude backports to avoid the tarfile issue
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
    name='molecular_viz',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
