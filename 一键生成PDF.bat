@echo off
setlocal
cd /d "%~dp0"

set "PYEXE="
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not defined PYEXE if exist "C:\Python312\python.exe" set "PYEXE=C:\Python312\python.exe"
if not defined PYEXE for /f "delims=" %%P in ('where python 2^>nul') do if not defined PYEXE set "PYEXE=%%P"
if not defined PYEXE (
  echo [ERROR] 没有找到 Python 3.10 以上版本，请先安装。
  pause
  exit /b 1
)

set PYTHONIOENCODING=utf-8

echo [1/5] 检查依赖
"%PYEXE%" -c "import markdown, pygments, playwright, pymupdf, matplotlib, PIL" >nul 2>nul
if errorlevel 1 (
  "%PYEXE%" -m pip install -r book\build\requirements.txt
  if errorlevel 1 (
    echo [ERROR] 依赖安装失败。
    pause
    exit /b 1
  )
)

echo [2/5] 生成参考文献
"%PYEXE%" book\build\gen_appendix.py
if errorlevel 1 goto fail

echo [3/5] 生成插图
"%PYEXE%" book\build\render_figures.py
if errorlevel 1 goto fail

echo [4/5] 排版 PDF
"%PYEXE%" book\build\build_book.py
if errorlevel 1 goto fail

echo [5/5] 自检
"%PYEXE%" book\build\checks\verify_pdf_text.py

echo.
echo 完成：output\embodied-ai.pdf
pause
exit /b 0

:fail
echo.
echo [ERROR] 构建失败，请查看上面的报错。若提示 PDF 被占用，请先关闭阅读器。
pause
exit /b 1
