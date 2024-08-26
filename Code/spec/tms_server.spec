# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ['C:\\Users\\serge\\PycharmProjects\\pythonProject\\pet_projects\\tms\\Code\\tms_server.py'],  # Path to your script within the Code folder
    pathex=['C:\\Users\\serge\\PycharmProjects\\pythonProject\\pet_projects\\tms'],
    binaries=[],
    datas=[
        ('C:\\Users\\serge\\PycharmProjects\\pythonProject\\pet_projects\\tms\\Code\\configs', 'configs'),
        ('C:\\Users\\serge\\PycharmProjects\\pythonProject\\pet_projects\\tms\\Code\\database', 'database'),
        ('C:\\Users\\serge\\PycharmProjects\\pythonProject\\pet_projects\\tms\\Code\\tcp_ip', 'tcp_ip'),
        ('C:\\Users\\serge\\PycharmProjects\\pythonProject\\pet_projects\\tms\\Code\\utils', 'utils'),
        ('C:\\Users\\serge\\PycharmProjects\\pythonProject\\pet_projects\\tms\\Code', 'Code')
    ],  # Include the Code directory to preserve its structure
    hiddenimports=['sqlite3', 'json', 'bcrypt'],  # Add hidden imports here
    hookspath=['C:\\Users\\serge\\PycharmProjects\\pythonProject\\pet_projects\\tms\\Code\\hooks'],  # Added comma here
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
    name='tms_server',
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