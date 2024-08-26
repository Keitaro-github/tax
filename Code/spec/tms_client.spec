# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Code\\tms_client.py'],
    pathex=['C:/Users/serge/PycharmProjects/pythonProject/pet_projects/tms'],
    binaries=[],
    datas=[
    	('Code/database/taxpayers.db', 'Code/database'),
    	('Code/configs/log_config.json', 'Code/configs'),
    	('Code/configs/tcp_config.json', 'Code/configs'),
    	('Code', 'Code'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='tms_client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
