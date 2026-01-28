# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app/run.py'],
    pathex=[],
    binaries=[],
    datas=[('app/templates', 'app/templates'), ('app/static', 'app/static')],
    hiddenimports=['fastapi', 'uvicorn', 'uvicorn.logging', 'uvicorn.loops', 'uvicorn.protocols', 'uvicorn.protocols.http', 'uvicorn.protocols.websockets', 'uvicorn.lifespan', 'app.gitutils', 'app.git_sync'],
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
    name='GitItonal',
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
