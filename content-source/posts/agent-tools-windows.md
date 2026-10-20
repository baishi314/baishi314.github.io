---
title: 把 AI Agent 命令行工具一次装好（Windows）
date: 2026-10-20 21:30:00
tags: [AI, Agent, Windows, 工具]
category: 折腾记录
summary: Claude Code、Codex、Gemini CLI 这些终端 agent 装起来不难，难的是 Node、Python、环境变量、代理一个个配。这里备了一个双击就能跑的安装脚本，外加每个报错对应的解法。
pinned: false
draft: false
cover: ""
---

这些工具本身装起来不难，难的是它们各要一套底座：有的要 Node 18+，有的要 Python 和 uv，有的认 `ANTHROPIC_BASE_URL`、有的认 `OPENAI_BASE_URL`。配完一圈，人已经不想写代码了。

所以干脆写了个脚本，把这些步骤压成一个菜单。**它只是把我手工敲过的命令按顺序抄了一遍**，没有黑魔法，你可以先打开看再决定跑不跑。

## 一分钟装完

三种方式，挑一个：

**① 双击（推荐）** — 下载 [install-agent-cli.bat](https://github.com/baishi314/baishi314.github.io/raw/main/tools/install-agent-cli.bat)，双击它。同目录没有 `.ps1` 也没关系，它会自己去仓库取。

**② 一行命令** — 打开 PowerShell，粘这一行：

```powershell
irm https://raw.githubusercontent.com/baishi314/baishi314.github.io/main/tools/install-agent-cli.ps1 | iex
```

**③ 手动** — 不信脚本就自己敲，下面的表格就是脚本干的事。

跑起来大概长这样：

```
  [基础环境]
    1  Node.js LTS            （一切 CLI 的底座）
    2  pnpm
    3  uv                     （Python 工具，Aider 需要）
    4  Git
    5  ripgrep                （代码全文搜索）
  [命令行 Agent]
    6  Claude Code            7  Codex CLI
    8  Gemini CLI             9  Qwen Code
   10  Aider                 11  OpenCode
   12  Crush                 13  Continue CLI
  [本地模型]
   14  Ollama
  [其它]
    A  全部推荐     M  换 npm 镜像    E  配 API 密钥
    P  代理自检     V  验证版本       Q  退出
```

支持组合输入，比如敲 `1,6,8` 一次装 Node + Claude Code + Gemini CLI。装完敲 `V` 可以一次看全部版本，哪个没装上一眼就出来。

## 它到底装了什么

| 命令 | 装它的命令 | 要什么 |
|---|---|---|
| `claude` | `npm i -g @anthropic-ai/claude-code` | Node 18+，Anthropic key 或中转地址 |
| `codex` | `npm i -g @openai/codex` | Node 18+，OpenAI key |
| `gemini` | `npm i -g @google/gemini-cli` | Node 20+，Google 账号登录即可 |
| `qwen` | `npm i -g @qwen-code/qwen-code` | Node 20+，通义千问 key |
| `aider` | `uv tool install aider-chat` | Python + uv，任意模型 |
| `opencode` | `npm i -g opencode-ai` | Node 18+，任意 OpenAI 兼容端点 |
| `crush` | `npm i -g @charmland/crush` | Node 18+ |
| `cn` | `npm i -g @continuedev/cli` | Node 18+，可接本地模型 |

Node 没装的话脚本先调 `winget install OpenJS.NodeJS.LTS`，再走 corepack 开 pnpm；uv 走 `winget install astral-sh.uv`，失败了退回官方安装脚本。每一步都先查「是不是已经装过了」，所以重复跑不会装两遍。

## 密钥与环境变量

脚本的 `E` 菜单会问你四个值，只写进**当前用户**的环境变量，不动系统级，不清空已有的：

| 变量 | 谁在用 | 填什么 |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude Code | 官方 key（`sk-ant-...`） |
| `ANTHROPIC_BASE_URL` | Claude Code | 用中转时填网关地址 |
| `ANTHROPIC_AUTH_TOKEN` | Claude Code | 用中转时填中转的 key |
| `OPENAI_BASE_URL` | Codex / Aider / OpenCode | 如 `https://api.deepseek.com/v1` |
| `OPENAI_API_KEY` | 同上 | 对应平台的 key |

写完**必须关掉终端重开**，新窗口才会读到。当前窗口里 `echo $env:OPENAI_API_KEY` 看不到值，不代表没写进去。

## 五个坑，按出现频率排

**1. 装完了但命令找不到**
`npm i -g` 装完，当前窗口的 `PATH` 还是旧的。关掉重开。如果新窗口还是找不到，看全局目录在不在 PATH 里：

```powershell
npm config get prefix     # 通常是 C:\Users\你\AppData\Roaming\npm
```

这个目录要出现在 `PATH` 里。

**2. npm 报 `EACCES` / 权限错误**
别用管理员身份硬来，也别去改 C 盘目录权限。改个全局目录就行：

```powershell
npm config set prefix "$env:APPDATA\npm"
```

然后把 `%APPDATA%\npm` 加进 PATH。

**3. `ECONNREFUSED 127.0.0.1:7890`**
你以前设过一个代理，软件卸载了，环境变量还留着。脚本的 `P` 菜单能查出来并清掉。手动查：

```powershell
[Environment]::GetEnvironmentVariable('HTTPS_PROXY','User')
```

**4. `UNABLE_TO_VERIFY_LEAF_SIGNATURE` / 证书错误**
多半是代理软件做了中间人 TLS 拦截。要么关掉代理，要么让 Node 信任它的证书：

```powershell
$env:NODE_EXTRA_CA_CERTS = "C:\你的代理证书.crt"
```

**5. 跑 ps1 报「禁止运行脚本」**
执行策略的问题。脚本里的 bat 已经带了 `-ExecutionPolicy Bypass`，自己手动跑时加上这个参数即可，不用去改全局策略。

## 从哪个开始

如果只是想试试，别一次装八个：

1. **Gemini CLI** —— 登录 Google 账号就有免费额度，零成本试水；
2. **Claude Code** —— 写正经项目时它最省心，但按量计费；
3. **Ollama + Continue** —— 完全本地、不花钱、代码不出机器，代价是模型笨一点；
4. **Aider** —— 已经在用 git 的话，它跟版本控制的配合最舒服。

## 卸载

脚本没写注册表、没装服务，卸就是卸包：

```powershell
npm uninstall -g @anthropic-ai/claude-code    # 换成对应包名
winget uninstall OpenJS.NodeJS.LTS            # 卸载底层环境
```

装了哪个、装了没有，敲 `V` 一目了然。

---

脚本在仓库里：[tools/](https://github.com/baishi314/baishi314.github.io/tree/main/tools)。有坑踩到过、或者想让脚本多装一个工具，提 issue 或直接改。
