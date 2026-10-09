@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo.
echo ================================================================
echo   本地预览（不会推送）
echo ================================================================
echo.
echo   先把 content-source/ 的内容同步到三套站点...
echo.

set PY=
if exist "C:\Python\Python314\python.exe" set PY=C:\Python\Python314\python.exe
if "%PY%"=="" ( where python >nul 2>nul && set PY=python )
if "%PY%"=="" ( echo [错误] 找不到 Python & pause & exit /b 1 )

"%PY%" "content-source\sync-content.py"
if errorlevel 1 ( echo [错误] 同步失败 & pause & exit /b 1 )

echo.
echo 选一个预览：
echo   1 = 极简笔记   (Hugo)
echo   2 = 二次元小屋 (Astro)
echo   3 = 星辉小屋   (Next.js)
echo.
set /p WHICH=输入 1/2/3 后回车: 

if "%WHICH%"=="1" goto minimal
if "%WHICH%"=="2" goto anime
if "%WHICH%"=="3" goto xinghui
echo 无效选择。
pause
exit /b 1

:minimal
where hugo >nul 2>nul || ( echo [错误] 未安装 hugo & pause & exit /b 1 )
hugo --source minimal-src --destination "%TEMP%\bs_preview\minimal" --minify --gc
echo.
echo 预览地址： http://127.0.0.1:8801/
start "" http://127.0.0.1:8801/
cd /d "%TEMP%\bs_preview\minimal" && "%PY%" -m http.server 8801
goto :eof

:anime
cd /d "anime-src"
call corepack pnpm build
if errorlevel 1 ( echo [错误] 构建失败 & pause & exit /b 1 )
echo.
echo 预览地址： http://127.0.0.1:8802/
start "" http://127.0.0.1:8802/
cd /d dist && "%PY%" -m http.server 8802
goto :eof

:xinghui
cd /d "xinghui-src"
set BASE_PATH=/xinghui
call corepack pnpm build
if errorlevel 1 ( echo [错误] 构建失败 & pause & exit /b 1 )
echo.
cd /d "%TEMP%\bs_preview"
if exist xinghui rmdir /s /q xinghui
mkdir xinghui
xcopy /e /i /q "%~dp0xinghui-src\out\*" "%TEMP%\bs_preview\xinghui\" >nul
echo 预览地址： http://127.0.0.1:8803/xinghui/
start "" http://127.0.0.1:8803/xinghui/
"%PY%" -m http.server 8803
goto :eof
