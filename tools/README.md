# tools/ · 站内脚本

放一些「配起来很烦、干脆写个脚本一次搞定」的东西。全部是可读的纯文本，跑之前可以直接打开看。

| 文件 | 干什么 |
|---|---|
| `install-agent-cli.ps1` | Windows 上一键装 AI Agent 命令行工具（Node/pnpm/uv/Git/ripgrep + Claude Code/Codex/Gemini/Qwen/Aider/OpenCode/Crush/Continue + Ollama），带镜像切换、API 变量写入、代理自检 |
| `install-agent-cli.bat` | 双击运行的壳，内部调用上面的 ps1；只下载了 bat 也能用（自动取回 ps1） |

## 怎么用

**双击 `install-agent-cli.bat`** 就行，会出一个带编号的菜单。

不想下载文件的话，在任何 PowerShell 窗口里粘这一行：

```powershell
irm https://raw.githubusercontent.com/baishi314/baishi314.github.io/main/tools/install-agent-cli.ps1 | iex
```

## 它不会干什么

- 不改系统目录、不写注册表、不动已有的环境变量（只在值为空或你确认时才写）
- 不需要管理员权限（winget 装 Node 时系统可能弹一次 UAC，那是 winget 的）
- 不装驱动、不装后台服务，卸载就是 `npm uninstall -g <包名>` / `winget uninstall <包名>`

## 出问题

`install-agent-cli.ps1` 里每个函数开头都会先 `Test-Cmd` 检查，已装过就跳过，所以重复跑是安全的。
装完命令找不到 → 关掉终端重开（PATH 要新窗口才生效）。

配套教程（每个报错怎么修）：<https://baishi314.github.io/minimal/posts/agent-tools-windows/>
