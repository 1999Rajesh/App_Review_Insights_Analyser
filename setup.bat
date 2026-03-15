@echo off
REM Quick Start Script for App Review Insights Analyzer

echo ========================================
echo App Review Insights Analyzer - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/4] Setting up Backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install backend dependencies
echo Installing backend dependencies...
pip install fastapi uvicorn python-multipart groq pandas python-dotenv pydantic pydantic-settings aiofiles email-validator

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and fill in your credentials:
    echo   GROQ_API_KEY=your_key_here
    echo   SENDER_EMAIL=your_email@gmail.com
    echo   SENDER_PASSWORD=your_app_password
    echo.
    pause
)

cd ..

echo.
echo [2/4] Setting up Frontend...
cd frontend

REM Install frontend dependencies
echo Installing frontend dependencies...
call npm install

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Configure your .env file in backend folder
echo 2. Run: .\start.bat
echo.
echo For detailed instructions, see README.md
echo.
pause
