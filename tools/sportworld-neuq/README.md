# 运动世界校园 · 东秦助手 —— 构建说明

成品下载在站点根目录的 [`sportworld.html`](../../sportworld.html)，文件是 `downloads/sportworld-neuq-v1.zip`。

本目录放的是**打包用的脚手架**，不含第三方源码本体。核心逻辑来自：

- <https://github.com/Funrestan/FunSportWorld>（主仓库）
- <https://github.com/YanamiNeko/NekoSportsWorldTool>

两者均为 MIT 许可，原作者署名与 LICENSE 已随压缩包一起分发。

---

## 这版到底改了什么

只改了三处，业务逻辑（登录、轨迹生成、加密、提交）一行没碰。

### 1. 配置目录兼容打包后的运行方式

`funsport/config.py` 的 `_find_data_dir()` 原本靠 `__file__` 向上找仓库根目录。PyInstaller 打包后 `__file__` 落在 `_MEIPASS` 临时目录，每次重启配置都会丢。

改成 frozen 感知：

1. `FUNSPORT_DATA_DIR` 环境变量优先；
2. `getattr(sys, "frozen", False)` 为真时用 `Path(sys.executable).resolve().parent`；
3. 否则保持原来的向上查找逻辑；
4. 生成的 `.funsport` 目录不可写（比如装在 Program Files）时回落 `Path.home() / ".funsport"`。

同时顶部补了 `import sys`。

### 2. 预设改为东秦

- `DEFAULT_CONFIG["city"]`：`成都市` → `秦皇岛市`
- `load_identity()` 默认值：`anchor_lat` `38.901678` → `39.939226`，`anchor_lon` `121.540241` → `119.602341`

锚点只是初始值，登录后会按真实打卡点重新校准，所以填偏了也不影响提交。

### 3. 界面去原作者痕迹

- `funsport/gui.py` 窗口标题 → `运动世界校园 - 东秦助手`
- 同文件页头 `FunSportWorld` 标签 → `运动世界校园 · 东秦助手`
- 地图默认中心从成都（`30.8885, 103.5965`）改为秦皇岛

---

## 怎么重新打包

### 环境

```powershell
# 用官方 CPython 3.12（不要用 Microsoft Store 的 WindowsApps 别名，那是空壳）
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pycryptodome requests pillow numpy tkintermapview pyinstaller `
  --index-url https://mirrors.cloud.tencent.com/pypi/simple --timeout 30 --retries 2
```

国内镜像实测：腾讯云可用，清华可用；阿里、pypi.org、上海交大当时全部超时。装之前记得清掉失效的代理环境变量（`HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY`）。

### 打包

```powershell
.\.venv\Scripts\pyinstaller.exe build.spec --noconfirm
```

产物在 `dist/运动世界校园-东秦助手/`，整目录分发。

### 两个必须知道的坑

1. **不要用 onefile。** 单文件版在这台机器上稳定报 `[PYI-41616:ERROR] Could not create temporary directory!`，exe 根本进不了 Python 层，连日志都写不出来。onedir（目录版）没有这个问题，启动也更快。
2. **`excludes` 别乱填。** 早期把 `email` / `http` / `xml` / `unittest` 排掉，结果 `requests` 直接断链。`build.spec` 里现在只排 `pytest`、`setuptools`、`pip`、`distutils`、`lib2to3`、`tkinter.test`。

### 自检

```powershell
& ".\dist\运动世界校园-东秦助手\运动世界校园-东秦助手.exe" --selftest
```

会在同目录写 `boot.log`，逐项检查 tkinter / tkintermapview / requests / PIL / Crypto / funsport，最后一行是 `selftest RESULT PASS`。

正常启动时 `boot.log` 至少有一行 `start pid=... frozen=True`；崩溃会额外生成 `crash.log`，里面是完整 traceback —— 让反馈的人直接发这个文件。

---

## 分发注意

`.funsport/` 目录会存账号和路线缓存。打包 zip 之前要删掉，否则把自己的账号信息发出去。
