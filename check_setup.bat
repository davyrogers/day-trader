@echo off
REM Setup verification script

echo ========================================
echo   Day Trader Setup Verification
echo ========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Running setup verification...
echo.
python verify_setup.py

pause
