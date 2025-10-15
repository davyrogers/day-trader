@echo off
REM Quick start script for Day Trader Forex Analyzer

echo ========================================
echo   Day Trader Forex Analyzer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or newer from python.org
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found
    echo Creating from .env.example...
    copy .env.example .env >nul
    echo.
    echo Please edit .env and add your Discord webhook URL
    echo Then run this script again
    pause
    exit /b 1
)

REM Run the workflow
echo Starting workflow...
echo.
python run.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Workflow failed
    pause
    exit /b 1
)

echo.
echo Workflow completed successfully!
pause
