@echo off
chcp 65001 >nul 2>nul
rem ============================================================
rem  AI Agent CLI 一键安装器（Windows）
rem  用法：双击本文件即可。全部逻辑在同目录的 install-agent-cli.ps1
rem  若你只下载了这个 bat，它会自动从 GitHub 取回配套的 ps1
rem ============================================================
setlocal
set "PS1=%~dp0install-agent-cli.ps1"
set "RAW=https://raw.githubusercontent.com/baishi314/baishi314.github.io/main/tools/install-agent-cli.ps1"

where powershell >nul 2>nul
if errorlevel 1 (
  echo [!] 找不到 powershell.exe，请在 Windows 上运行本脚本。
  pause
  exit /b 1
)

if not exist "%PS1%" (
  echo [*] 本地没有 install-agent-cli.ps1，正在从 GitHub 取回...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; try { Invoke-WebRequest -Uri '%RAW%' -OutFile '%~dp0install-agent-cli.ps1' -UseBasicParsing -TimeoutSec 60 } catch { Write-Host '[!] 下载失败: ' $_.Exception.Message; exit 1 }"
  if not exist "%PS1%" (
    echo [!] 仍找不到 install-agent-cli.ps1，退出。
    pause
    exit /b 1
  )
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%" %*
echo.
pause
endlocal
