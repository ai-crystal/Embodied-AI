@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

rem usage: build.bat [intro^|system^|all^|figures]

set "PYEXE="
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not defined PYEXE if exist "C:\Python312\python.exe" set "PYEXE=C:\Python312\python.exe"
if not defined PYEXE for /f "delims=" %%P in ('where python 2^>nul') do if not defined PYEXE set "PYEXE=%%P"
if not defined PYEXE (
  echo [ERROR] Python 3.10+ not found.
  pause
  exit /b 1
)
set PYTHONIOENCODING=utf-8

"%PYEXE%" -c "import markdown, pygments, playwright, pymupdf, matplotlib, PIL" >nul 2>nul
if errorlevel 1 (
  echo [1/4] installing dependencies ...
  "%PYEXE%" -m pip install -r books\build\requirements.txt
  if errorlevel 1 goto fail
)

if "%~1"=="" goto all
if /i "%~1"=="all" goto all
if /i "%~1"=="intro" goto intro
if /i "%~1"=="system" goto system
if /i "%~1"=="figures" goto figures
echo unknown target: %~1
echo usage: build.bat [intro^|system^|all^|figures]
exit /b 1

:all
call :one intro
if errorlevel 1 goto fail
call :one system
if errorlevel 1 goto fail
goto done

:intro
call :one intro
if errorlevel 1 goto fail
goto done

:system
call :one system
if errorlevel 1 goto fail
goto done

:figures
"%PYEXE%" books\build\figures.py --book books\intro
if errorlevel 1 goto fail
"%PYEXE%" books\build\figures.py --book books\system
if errorlevel 1 goto fail
goto done

:one
set "VOL=%~1"
echo.
echo ==== %VOL% ====
if /i "%VOL%"=="system" (
  echo [1/4] appendix C
  "%PYEXE%" books\build\gen_appendix.py
  if errorlevel 1 exit /b 1
) else (
  echo [1/4] appendix C skipped for %VOL%
)
echo [2/4] figures
"%PYEXE%" books\build\figures.py --book books\%VOL%
if errorlevel 1 exit /b 1
echo [3/4] typeset
"%PYEXE%" books\build\build.py --book books\%VOL%
if errorlevel 1 exit /b 1
echo [4/4] check
"%PYEXE%" books\build\checks\verify_pdf_text.py --book books\%VOL%
"%PYEXE%" books\build\checks\check_markdown.py --book books\%VOL%
exit /b 0

:fail
echo.
echo [ERROR] build failed. See messages above. Close any open PDF and retry.
pause
exit /b 1

:done
echo.
echo done. output\v1-intro.pdf  output\v2-system.pdf
pause
exit /b 0
