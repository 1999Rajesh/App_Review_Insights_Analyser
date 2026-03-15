@echo off
REM Railway Deployment Helper Script
REM This script helps you deploy to Railway quickly

echo ======================================================================
echo   Railway Deployment - App Review Insights Analyzer
echo ======================================================================
echo.
echo This script will help you deploy to Railway
echo.
echo Prerequisites:
echo   1. GitHub account with repo pushed
echo   2. Railway account (https://railway.app)
echo   3. Node.js installed (for Railway CLI)
echo.
echo ======================================================================
echo.

REM Step 1: Check if Railway CLI is installed
where railway >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] Railway CLI not found. Installing...
    echo.
    npm install -g @railway-cli
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install Railway CLI
        echo Please install Node.js first from https://nodejs.org
        pause
        exit /b 1
    )
)

echo [OK] Railway CLI is installed
echo.

REM Step 2: Login to Railway
echo ======================================================================
echo Step 1: Login to Railway
echo ======================================================================
echo.
echo Opening Railway login in your browser...
echo.
railway login

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Login failed
    pause
    exit /b 1
)

echo.
echo [OK] Successfully logged in!
echo.

REM Step 3: Initialize Railway project
echo ======================================================================
echo Step 2: Link to Railway Project
echo ======================================================================
echo.
echo This will create or link to a Railway project
echo.
railway init

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to initialize Railway project
    pause
    exit /b 1
)

echo.
echo [OK] Railway project linked!
echo.

REM Step 4: Add environment variables
echo ======================================================================
echo Step 3: Environment Variables Setup
echo ======================================================================
echo.
echo IMPORTANT: You need to add these environment variables in Railway Dashboard
echo.
echo Copy these variables and paste them in Railway dashboard:
echo   - Variables tab -^> New Variable
echo.
echo ===== PLAY STORE CONFIGURATION =====
echo PLAY_STORE_DEFAULT_APP_ID=com.nextbillion.groww
echo PLAY_STORE_LANGUAGE=en
echo PLAY_STORE_COUNTRY=in
echo.
echo ===== REVIEW FILTERS =====
echo MAX_REVIEWS_TO_FETCH=500
echo REVIEW_WEEKS_RANGE=12
echo MIN_REVIEW_WORD_COUNT=5
echo ALLOW_EMOJIS=false
echo REQUIRED_LANGUAGE=en
echo.
echo ===== DATA DIRECTORIES =====
echo REVIEWS_DATA_DIR=data/reviews
echo CSV_DATA_DIR=weekly_reviews
echo.
echo ===== EMAIL CONFIGURATION =====
echo SMTP_SENDER_EMAIL=your-email@gmail.com
echo SMTP_PASSWORD=YOUR_GMAIL_APP_PASSWORD
echo SMTP_HOST=smtp.gmail.com
echo SMTP_PORT=587
echo WEEKLY_REPORT_EMAIL=recipient@example.com
echo.
echo ===== SCHEDULER =====
echo SCHEDULER_INTERVAL_MINUTES=5
echo.
echo Press any key when you've added all environment variables...
pause >nul

echo.
echo [OK] Environment variables noted!
echo.

REM Step 5: Deploy
echo ======================================================================
echo Step 4: Deploy to Railway
echo ======================================================================
echo.
echo Starting deployment...
echo.
railway up

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Deployment failed
    pause
    exit /b 1
)

echo.
echo [OK] Deployment started!
echo.

REM Step 6: Get deployment URL
echo ======================================================================
echo Step 5: Get Your Deployment URL
echo ======================================================================
echo.
railway domain

echo.
echo ======================================================================
echo   NEXT STEPS
echo ======================================================================
echo.
echo 1. Go to Railway dashboard: https://railway.app
echo 2. Add environment variables (see list above)
echo 3. Wait for deployment to complete (~2-3 minutes)
echo 4. Create scheduled task:
echo    - Command: python -m services.railway_weekly_task
echo    - Schedule: 0 10 * * 1  (Every Monday at 10 AM IST)
echo.
echo For detailed instructions, see:
echo docs/DEPLOY_TO_RAILWAY_STEP_BY_STEP.md
echo.
echo ======================================================================
echo   DEPLOYMENT STARTED SUCCESSFULLY!
echo ======================================================================
echo.
pause
