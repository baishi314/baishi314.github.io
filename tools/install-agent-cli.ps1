# -*- coding: utf-8 -*-
<#
  AI Agent CLI 一键安装器（Windows / PowerShell 5.1+）
  =====================================================
  作者：baishi314 · 仓库：https://github.com/baishi314/baishi314.github.io
  教程：https://baishi314.github.io/minimal/posts/agent-tools-windows/

  用法（三种，任选）：
    1. 双击 install-agent-cli.bat
    2. 在本目录右键「在终端中打开」，执行：
         powershell -NoProfile -ExecutionPolicy Bypass -File .\install-agent-cli.ps1
    3. 一行命令（不想下载文件）：
         irm https://raw.githubusercontent.com/baishi314/baishi314.github.io/main/tools/install-agent-cli.ps1 | iex

  设计原则：
    · 不碰系统目录、不要求管理员权限（winget 装 Node 时可能弹一次 UAC）
    · 国内网络默认给 npm 换镜像，失败会提示不改也能继续
    · 每一步都先检查「是不是已经装过」，装过的直接跳过
    · 不覆盖你已有的环境变量，除非它明确是空的
#>

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'

# ---------------------------------------------------------------- 输出样式
function Say  ($m) { Write-Host $m }
function Ok   ($m) { Write-Host "  [OK] $m"   -ForegroundColor Green }
function Warn ($m) { Write-Host "  [!]  $m"   -ForegroundColor Yellow }
function Bad  ($m) { Write-Host "  [X]  $m"   -ForegroundColor Red }
function Head ($m) { Write-Host ""; Write-Host "== $m ==" -ForegroundColor Cyan }

function Test-Cmd ($name) {
    $c = Get-Command $name -ErrorAction SilentlyContinue
    return [bool]$c
}

function Refresh-Path {
    $m = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $u = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = "$m;$u"
}

# ---------------------------------------------------------------- npm 镜像
function Set-NpmMirror {
    Head 'npm 镜像'
    if (-not (Test-Cmd npm)) { Warn '还没装 Node/npm，先跑第 1 项。'; return }
    Say "当前 registry: $(npm config get registry 2>$null)"
    Say '换成 https://registry.npmmirror.com （国内通常快很多，恢复官方用 npm config set registry https://registry.npmjs.org）'
    $ans = Read-Host '  换吗？(y/N)'
    if ($ans -match '^[yYsS]') {
        npm config set registry https://registry.npmmirror.com 2>$null | Out-Null
        Ok "已切换：$(npm config get registry 2>$null)"
    } else {
        Say '  保持不动。'
    }
}

# ---------------------------------------------------------------- 单项安装
function Ensure-Node {
    Head 'Node.js LTS'
    if (Test-Cmd node) {
        Ok "已安装 Node $(node -v)  (npm $(npm -v 2>$null))"
        return
    }
    if (-not (Test-Cmd winget)) {
        Bad '没有 winget（Windows 10 1809 之前或精简版系统）。'
        Say '    手动安装：https://nodejs.org/zh-cn/download  （选 LTS，一路下一步，勾选 Add to PATH）'
        return
    }
    Say '用 winget 安装 Node.js LTS（可能弹一次 UAC）...'
    winget install --id OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements
    Refresh-Path
    if (Test-Cmd node) { Ok "装好了：Node $(node -v)" } else { Warn '装完了但当前窗口还没生效，关掉重开终端再验证。' }
}

function Ensure-Pnpm {
    Head 'pnpm'
    if (Test-Cmd pnpm) { Ok "已安装 pnpm $(pnpm -v)"; return }
    if (-not (Test-Cmd node)) { Warn '先装 Node（第 1 项）。'; return }
    if (Test-Cmd corepack) {
        Say '用 corepack 启用 pnpm（最快，不需要下载）...'
        corepack enable 2>$null | Out-Null
        corepack prepare pnpm@latest --activate 2>$null | Out-Null
    }
    Refresh-Path
    if (-not (Test-Cmd pnpm)) {
        Say 'corepack 没成，改用 npm 全局安装...'
        npm install -g pnpm
    }
    Refresh-Path
    if (Test-Cmd pnpm) { Ok "装好了：pnpm $(pnpm -v)" } else { Warn '仍未生效，重开终端再试。' }
}

function Ensure-Uv {
    Head 'uv（Python 包/工具管理器，Aider 等需要）'
    if (Test-Cmd uv) { Ok "已安装 uv $(uv --version 2>$null)"; return }
    $done = $false
    if (Test-Cmd winget) {
        Say '用 winget 安装 astral-sh.uv ...'
        winget install --id astral-sh.uv -e --accept-source-agreements --accept-package-agreements 2>$null
        Refresh-Path
        $done = Test-Cmd uv
    }
    if (-not $done) {
        Say '改走官方安装脚本...'
        try {
            Invoke-RestMethod -Uri 'https://astral.sh/uv/install.ps1' -TimeoutSec 60 | Invoke-Expression
            Refresh-Path
            $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
            $done = Test-Cmd uv
        } catch { Bad "官方脚本失败：$($_.Exception.Message)" }
    }
    if ($done) { Ok "装好了：$(uv --version 2>$null)" } else { Warn '没装上，手动：https://docs.astral.sh/uv/getting-started/installation/' }
}

function Ensure-Git {
    Head 'Git'
    if (Test-Cmd git) { Ok "已安装 $(git --version)"; return }
    if (Test-Cmd winget) {
        winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements
        Refresh-Path
    }
    if (Test-Cmd git) { Ok "装好了：$(git --version)" } else { Warn '手动：https://git-scm.com/download/win' }
}

function Ensure-Ripgrep {
    Head 'ripgrep（Claude Code 等拿它全文搜索）'
    if (Test-Cmd rg) { Ok "已安装 $(rg --version | Select-Object -First 1)"; return }
    $done = $false
    if (Test-Cmd winget) {
        winget install --id BurntSushi.ripgrep.MSVC -e --accept-source-agreements --accept-package-agreements 2>$null
        Refresh-Path
        $done = Test-Cmd rg
    }
    if (-not $done) { Warn '没装上，手动：https://github.com/BurntSushi/ripgrep/releases' }
    else { Ok '装好了。' }
}

# npm 全局包装一个，统一处理 EACCES / 镜像 / 已装判断
function Npm-Global ($bin, $pkg, $note) {
    Head "$bin"
    if (Test-Cmd $bin) { Ok "已安装（$(Get-Command $bin).Source）"; return }
    if (-not (Test-Cmd npm)) { Warn '先装 Node（第 1 项）。'; return }
    Say "npm install -g $pkg"
    npm install -g $pkg 2>&1 | Select-Object -Last 8
    Refresh-Path
    if (Test-Cmd $bin) {
        $v = & $bin --version 2>$null | Select-Object -First 1
        Ok "装好了：$bin $v"
        if ($note) { Say "  下一步：$note" }
    } else {
        Warn "命令 $bin 还没出现。先关掉这个窗口、重开终端再敲 $bin --version 验证。"
        Say '  常见原因：PATH 没刷新 / npm 全局目录不在 PATH / 网络断了'
    }
}

function Ensure-Ollama {
    Head 'Ollama（本机跑开源模型）'
    if (Test-Cmd ollama) { Ok "已安装 $(ollama --version 2>$null)"; return }
    if (Test-Cmd winget) {
        winget install --id Ollama.Ollama -e --accept-source-agreements --accept-package-agreements
        Refresh-Path
    }
    if (Test-Cmd ollama) { Ok '装好了。拉个模型试试：ollama pull qwen3:8b' }
    else { Warn '手动：https://ollama.com/download/windows' }
}

# ---------------------------------------------------------------- 环境变量
function Set-ApiEnv {
    Head '配置 API 地址与密钥（可选）'
    Say '作用：让 Claude Code / Codex / Aider 这些 CLI 走你自己的中转地址或国产模型。'
    Say '留空表示跳过。只写入当前用户的环境变量，不改系统级。'
    Say ''
    Say '常见组合：'
    Say '  · Anthropic 官方      ANTHROPIC_API_KEY=sk-ant-...'
    Say '  · 中转 / 国产兼容     ANTHROPIC_BASE_URL=https://你的网关/v1  +  ANTHROPIC_AUTH_TOKEN=xxx'
    Say '  · OpenAI 兼容         OPENAI_BASE_URL=https://api.deepseek.com/v1  +  OPENAI_API_KEY=sk-...'
    Say ''

    $pairs = @(
        @{ Name = 'ANTHROPIC_BASE_URL';   Prompt = 'ANTHROPIC_BASE_URL  (回车跳过)' },
        @{ Name = 'ANTHROPIC_AUTH_TOKEN'; Prompt = 'ANTHROPIC_AUTH_TOKEN / API key (回车跳过)' },
        @{ Name = 'OPENAI_BASE_URL';      Prompt = 'OPENAI_BASE_URL  (回车跳过)' },
        @{ Name = 'OPENAI_API_KEY';       Prompt = 'OPENAI_API_KEY  (回车跳过)' }
    )
    $changed = @()
    foreach ($p in $pairs) {
        $cur = [Environment]::GetEnvironmentVariable($p.Name, 'User')
        $shown = if ($cur) { "当前: " + $cur.Substring(0, [Math]::Min(12, $cur.Length)) + "..." } else { '当前: (空)' }
        Say "  $($p.Name)  —  $shown"
        $v = Read-Host "    $($p.Prompt)"
        if ($v -and $v.Trim()) {
            [Environment]::SetEnvironmentVariable($p.Name, $v.Trim(), 'User')
            Set-Item -Path "Env:$($p.Name)" -Value $v.Trim()
            $changed += $p.Name
        }
    }
    if ($changed.Count -gt 0) {
        Ok ("已写入用户环境变量：" + ($changed -join ', '))
        Say '  新开的终端才会自动带上这些变量。'
    } else {
        Say '  没改动。'
    }
}

function Check-Proxy {
    Head '代理自检'
    $keys = 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy'
    $found = $false
    foreach ($k in $keys) {
        $v = [Environment]::GetEnvironmentVariable($k, 'User')
        if ($v) { $found = $true; Say "  $k = $v" }
    }
    if ($found) {
        Warn '检测到用户级代理变量。如果 npm / curl 报 ECONNREFUSED、证书错误，多半是这个代理已经失效。'
        $ans = Read-Host '  现在清掉它们？(y/N)'
        if ($ans -match '^[yYsS]') {
            foreach ($k in $keys) { [Environment]::SetEnvironmentVariable($k, $null, 'User'); Remove-Item "Env:$k" -ErrorAction SilentlyContinue }
            Ok '已清除用户级代理变量（系统级的不动）。'
        }
    } else {
        Ok '没有用户级代理变量。'
    }
}

# ---------------------------------------------------------------- 菜单
function Show-Menu {
    Write-Host ''
    Write-Host '  ┌──────────────────────────────────────────────┐' -ForegroundColor DarkCyan
    Write-Host '  │   AI Agent CLI 一键安装器 · baishi314        │' -ForegroundColor DarkCyan
    Write-Host '  └──────────────────────────────────────────────┘' -ForegroundColor DarkCyan
    Say ''
    Say '  [基础环境]'
    Say '    1  Node.js LTS            （一切 CLI 的底座）'
    Say '    2  pnpm                   （跑前端/博客工具链）'
    Say '    3  uv                     （Python 工具，Aider 需要）'
    Say '    4  Git'
    Say '    5  ripgrep                （代码全文搜索）'
    Say ''
    Say '  [命令行 Agent]'
    Say '    6  Claude Code            （Anthropic，终端里最强的那个）'
    Say '    7  Codex CLI              （OpenAI 官方命令行）'
    Say '    8  Gemini CLI             （Google，免费额度大）'
    Say '    9  Qwen Code              （阿里通义，国内可直接用）'
    Say '   10  Aider                  （老牌结对编程，git 集成好）'
    Say '   11  OpenCode               （开源 TUI，多模型）'
    Say '   12  Crush                  （Charm 出品，界面漂亮）'
    Say '   13  Continue CLI           （可接本地模型）'
    Say ''
    Say '  [本地模型]'
    Say '   14  Ollama                 （在自己电脑上跑模型）'
    Say ''
    Say '  [其它]'
    Say '    A  全部推荐（1-5 + 6 + 8 + 11 + 14）'
    Say '    M  换 npm 镜像（国内加速）'
    Say '    E  配置 API 地址 / 密钥'
    Say '    P  代理自检'
    Say '    V  验证已装工具版本'
    Say '    Q  退出'
    Write-Host ''
}

function Run-All {
    Ensure-Node
    Ensure-Pnpm
    Ensure-Uv
    Ensure-Git
    Ensure-Ripgrep
    Npm-Global 'claude' '@anthropic-ai/claude-code' '进项目目录敲 claude'
    Npm-Global 'gemini' '@google/gemini-cli' '敲 gemini 登录或配 GEMINI_API_KEY'
    Npm-Global 'opencode' 'opencode-ai' '敲 opencode'
    Ensure-Ollama
    Say ''
    Ok '全部跑完了。关掉这个窗口重开一个终端，PATH 才完整生效。'
}

function Verify-All {
    Head '版本自检'
    $items = @(
        @{n='node';    a='-v'},
        @{n='npm';     a='-v'},
        @{n='pnpm';    a='-v'},
        @{n='uv';      a='--version'},
        @{n='git';     a='--version'},
        @{n='rg';      a='--version'},
        @{n='claude';  a='--version'},
        @{n='codex';   a='--version'},
        @{n='gemini';  a='--version'},
        @{n='qwen';    a='--version'},
        @{n='aider';   a='--version'},
        @{n='opencode';a='--version'},
        @{n='crush';   a='--version'},
        @{n='continue';a='--version'},
        @{n='ollama';  a='--version'}
    )
    foreach ($i in $items) {
        if (Test-Cmd $i.n) {
            $out = & $i.n $i.a 2>$null | Select-Object -First 1
            Write-Host ("  {0,-9} {1}" -f $i.n, $out) -ForegroundColor Green
        } else {
            Write-Host ("  {0,-9} -" -f $i.n) -ForegroundColor DarkGray
        }
    }
}

# ---------------------------------------------------------------- 主循环
Say ''
Say '这个脚本会往你电脑上装东西（npm 全局包、winget 包）。'
Say '不想要了可以逐条卸载：npm uninstall -g <包名> / winget uninstall <包名>'
Say ''

$loop = $true
while ($loop) {
    Show-Menu
    $choice = (Read-Host '  选一个（多个用逗号，如 1,6,8）').Trim()
    if (-not $choice) { continue }
    foreach ($c in ($choice -split '[,，\s]+')) {
        switch -Regex ($c) {
            '^1$'  { Ensure-Node }
            '^2$'  { Ensure-Pnpm }
            '^3$'  { Ensure-Uv }
            '^4$'  { Ensure-Git }
            '^5$'  { Ensure-Ripgrep }
            '^6$'  { Npm-Global 'claude' '@anthropic-ai/claude-code' '先跑 E 配密钥，再进项目目录敲 claude' }
            '^7$'  { Npm-Global 'codex' '@openai/codex' '敲 codex' }
            '^8$'  { Npm-Global 'gemini' '@google/gemini-cli' '敲 gemini' }
            '^9$'  { Npm-Global 'qwen' '@qwen-code/qwen-code' '敲 qwen' }
            '^10$' { Head 'Aider'; if (Test-Cmd aider) { Ok '已安装' } elseif (Test-Cmd uv) { Say 'uv tool install aider-chat'; uv tool install aider-chat; Refresh-Path; if (Test-Cmd aider) { Ok '装好了：aider --version' } else { Warn '没出现，重开终端再试' } } else { Warn '先装 uv（第 3 项）' } }
            '^11$' { Npm-Global 'opencode' 'opencode-ai' '敲 opencode' }
            '^12$' { Npm-Global 'crush' '@charmland/crush' '敲 crush' }
            '^13$' { Npm-Global 'continue' '@continuedev/cli' '敲 cn（Continue CLI 的命令名是 cn）' }
            '^14$' { Ensure-Ollama }
            '^[aA]$' { Run-All }
            '^[mM]$' { Set-NpmMirror }
            '^[eE]$' { Set-ApiEnv }
            '^[pP]$' { Check-Proxy }
            '^[vV]$' { Verify-All }
            '^[qQ]$' { $loop = $false }
            default { Warn "不认识的选项：$c" }
        }
    }
}

Head '结束'
Say '重开一个终端窗口，再敲 claude / codex / gemini 试试。'
Say '出问题把报错原文贴出来 —— 教程里有每个坑对应的解法。'
exit 0
