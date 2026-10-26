"""东秦版启动入口：any 异常都不静默，写日志并弹窗告知。

支持 `--selftest`：只做导入自检，把结果写进 boot.log 后退出，
用于验证打包产物是否可用（不弹窗、不开界面）。
"""
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path


def _log_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def _boot(msg: str) -> None:
    """启动即写一行日志，保证任何静默失败都留痕。"""
    try:
        line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}\n"
        with open(_log_dir() / "boot.log", "a", encoding="utf-8") as fh:
            fh.write(line)
    except Exception:
        pass


def _report(exc: BaseException) -> None:
    text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    _boot("EXCEPTION\n" + text)
    try:
        log = _log_dir() / "crash.log"
        log.write_text(text, encoding="utf-8")
        where = str(log)
    except Exception:
        where = "（日志写入失败）"
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "启动失败",
            "程序初始化出错，请把下面这个文件发给管理员：\n\n"
            f"{where}\n\n"
            f"{type(exc).__name__}: {exc}",
            parent=root,
        )
        root.destroy()
    except Exception:
        pass


def _selftest() -> int:
    ok = True
    checks = [
        ("tkinter", "import tkinter"),
        ("tkintermapview", "import tkintermapview"),
        ("requests", "import requests"),
        ("PIL", "from PIL import Image"),
        ("Crypto", "from Crypto.Cipher import AES"),
        ("funsport.config", "from funsport import config"),
        ("funsport.gui", "from funsport import gui"),
        ("funsport.api_client", "from funsport.api import client"),
    ]
    for name, stmt in checks:
        try:
            exec(stmt, {})  # noqa: S102 - 固定字面量
            _boot(f"selftest OK   {name}")
        except BaseException as exc:  # noqa: BLE001
            ok = False
            _boot(f"selftest FAIL {name}: {type(exc).__name__}: {exc}")
    try:
        from funsport import config
        _boot(f"selftest data_dir = {config._find_data_dir()}")
    except BaseException as exc:  # noqa: BLE001
        ok = False
        _boot(f"selftest data_dir FAIL: {type(exc).__name__}: {exc}")
    _boot("selftest RESULT " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main() -> int:
    _boot(f"start pid={os.getpid()} frozen={getattr(sys, 'frozen', False)} argv={sys.argv[1:]}")
    if "--selftest" in sys.argv:
        return _selftest()
    try:
        from funsport.gui import launch
        launch()
        _boot("gui closed normally")
        return 0
    except SystemExit:
        raise
    except BaseException as exc:  # noqa: BLE001 - 兜底，保证错误可见
        _report(exc)
        return 1


if __name__ == "__main__":
    os.environ.setdefault("PYTHONUTF8", "1")
    sys.exit(main())
