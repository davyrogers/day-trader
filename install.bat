@echo off
echo ========================================
echo   Day Trader - One-Click Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo [1/5] Installing Python packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo [2/5] Creating .env file...
if not exist .env (
    copy .env.example .env >nul
    echo Created .env from template
) else (
    echo .env already exists, skipping
)

echo.
echo [3/5] Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Ollama not running or not installed
    echo.
    echo Please:
    echo 1. Install Ollama from https://ollama.ai
    echo 2. Run: ollama serve
    echo 3. Run this script again
    pause
    exit /b 1
)

echo Ollama is running!

echo.
echo [4/5] Checking required models...
echo This may take a while for first-time setup...
echo.

ollama list | findstr /C:"gpt-oss:20b" >nul 2>&1
if %errorlevel% neq 0 (
    echo Pulling gpt-oss:20b (this will take several minutes)...
    ollama pull gpt-oss:20b
)

ollama list | findstr /C:"deepseek-r1:8b" >nul 2>&1
if %errorlevel% neq 0 (
    echo Pulling deepseek-r1:8b (this will take several minutes)...
    ollama pull deepseek-r1:8b
)

echo.
echo [5/5] Running setup verification...
python verify_setup.py

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env and add your Discord webhook URL
echo 2. Run: start.bat
echo.
pause
