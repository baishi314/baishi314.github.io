# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller 打包配置：目录版（onedir）。

不用单文件（onefile）：onefile 每次启动都要把自己解压到临时目录，
在部分机器上会报 "Could not create temporary directory!" 直接跑不起来，
而且首次启动慢、更容易被杀软误杀。目录版解压后双击即用，启动快、稳定。
"""
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

ROOT = r"C:\Users\baishi314\Documents\deepseek-harness\default-workspace\neuko-run"
SRC = ROOT + r"\src\FunSportWorld-main"
APP_NAME = "运动世界校园-东秦助手"

hiddenimports = (
    collect_submodules("tkintermapview")
    + collect_submodules("funsport")
    + ["PIL._tkinter_finder", "Crypto.Cipher.AES", "Crypto.Cipher._raw_aes"]
)

datas = collect_data_files("tkintermapview")
datas += [(SRC + r"\LICENSE", ".")]

a = Analysis(
    [ROOT + r"\build\app_entry.py"],
    pathex=[SRC],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["pytest", "setuptools", "pip", "distutils", "lib2to3", "tkinter.test"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name=APP_NAME,
)
