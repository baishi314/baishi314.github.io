@echo off
chcp 65001 >nul
cd /d "%~dp0"
rem Python 要按 UTF-8 读写，否则中文会变乱码
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo.
echo ================================================================
echo   baishi314 博客 - 发布文章
echo ================================================================
echo.

rem ---- 找 Python ----
set PY=
if exist "C:\Python\Python314\python.exe" set PY=C:\Python\Python314\python.exe
if "%PY%"=="" (
  where python >nul 2>nul && set PY=python
)
if "%PY%"=="" (
  echo [错误] 找不到 Python，请先安装 Python 3
  pause
  exit /b 1
)

rem ---- 1. 新建 / 编辑文章 ----
echo [1/4] 新建文章
echo.
"%PY%" "content-source\newpost.py"
if errorlevel 1 (
  echo.
  echo 已取消，什么都没改。
  pause
  exit /b 1
)

rem ---- 2. 同步到三套站点 ----
echo [2/4] 同步到三套站点
"%PY%" "content-source\sync-content.py"
if errorlevel 1 (
  echo.
  echo [错误] 同步失败，已停止。
  pause
  exit /b 1
)

rem ---- 3. 本地构建检查 ----
echo.
echo [3/4] 本地构建检查（约 30 秒）
set HUGO_OK=0
where hugo >nul 2>nul && set HUGO_OK=1
if "%HUGO_OK%"=="1" (
  hugo --source minimal-src --destination "%TEMP%\bs_build\minimal" --minify --gc >nul 2>nul
  if errorlevel 1 (
    echo [错误] Hugo 构建失败，未提交。
    pause
    exit /b 1
  )
  echo     极简笔记  OK
) else (
  echo     极简笔记  跳过（未装 hugo）
)

echo     注意：三站完整构建由 GitHub Actions 完成，这里只做快速语法检查。

rem ---- 4. 提交 + 推送 ----
echo.
echo [4/4] 提交并推送
git add -A
git -c safe.directory=%CD% commit -m "post: 新增文章" >nul 2>nul
if errorlevel 1 (
  echo     没有变化需要提交。
  pause
  exit /b 0
)
set GIT_SSH_COMMAND=ssh -o StrictHostKeyChecking=accept-new -o BatchMode=yes -o ConnectTimeout=20
git -c safe.directory=%CD% push ssh://git@ssh.github.com:443/baishi314/baishi314.github.io.git main

echo.
echo ================================================================
echo   推送完成
echo.
echo   大约 2 分钟后，三套站点都会出现这篇文章：
echo     https://baishi314.github.io/minimal/
echo     https://baishi314.github.io/anime/
echo     https://baishi314.github.io/xinghui/
echo ================================================================
echo.
pause
