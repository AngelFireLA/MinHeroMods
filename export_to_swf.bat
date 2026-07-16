@echo off
setlocal
cd /d "%~dp0"

echo == Building Min Hero SWF ==
python build_swf.py
if errorlevel 1 (
    echo.
    echo Build failed. default.swf was not replaced.
    pause
    exit /b 1
)

echo.
echo Build completed successfully: default.swf
pause
