@echo off
REM ==========================================
REM Backend Deployment to Railway - Automated
REM ==========================================

echo.
echo ============================================
echo   Backend Deployment to Railway
echo   Step-by-Step with Verification
echo ============================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install from https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Node.js found
node --version
echo.

REM Check if Railway CLI is installed
where railway >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Installing Railway CLI...
    npm install -g @railway/cli
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install Railway CLI
        pause
        exit /b 1
    )
)

echo [OK] Railway CLI found
railway --version
echo.

REM Navigate to backend directory
cd backend

REM Step 1: Login
echo ============================================
echo   Step 1: Login to Railway
echo ============================================
echo.
echo This will open your browser. Please login with GitHub.
echo.
pause
railway login
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Login failed
    pause
    exit /b 1
)
echo [OK] Login successful
echo.

REM Step 2: Initialize/Link Project
echo ============================================
echo   Step 2: Create or Link Railway Project
echo ============================================
echo.
echo Do you want to:
echo 1. Create new project
echo 2. Link existing project
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo Creating new project...
    railway init
) else (
    echo Linking to existing project...
    railway link
)

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Project setup failed
    pause
    exit /b 1
)
echo [OK] Project setup complete
echo.

REM Step 3: Set Environment Variables
echo ============================================
echo   Step 3: Set Environment Variables
echo ============================================
echo.
echo IMPORTANT: You need the following credentials ready:
echo.
echo 1. Gemini API Key (from https://makersuite.google.com/app/apikey)
echo 2. Gmail App Password (from https://myaccount.google.com/apppasswords)
echo    - Copy WITHOUT SPACES
echo 3. Your Vercel URL (for CORS, e.g., your-app.vercel.app)
echo.
pause

set /p GEMINI_KEY="Enter Gemini API Key: "
set /p GMAIL_EMAIL="Enter Gmail Address: "
set /p GMAIL_PASS="Enter Gmail App Password (NO SPACES): "
set /p RECIPIENT="Enter Recipient Email: "
set /p VERCEL_URL="Enter Vercel URL (without https://): "

echo.
echo Setting environment variables...
echo.

railway variables set ^
  GEMINI_API_KEY=%GEMINI_KEY% ^
  GEMINI_MODEL=gemini-2.5-flash ^
  SMTP_SERVER=smtp.gmail.com ^
  SMTP_PORT=465 ^
  SENDER_EMAIL=%GMAIL_EMAIL% ^
  SENDER_PASSWORD=%GMAIL_PASS% ^
  RECIPIENT_EMAIL=%RECIPIENT% ^
  BACKEND_CORS_ORIGINS=https://%VERCEL_URL% ^
  MAX_THEMES=5 ^
  MAX_WORDS=250 ^
  REVIEW_WEEKS_RANGE=8 ^
  MAX_REVIEWS_TO_FETCH=500 ^
  PLAY_STORE_DEFAULT_APP_ID=in.groww ^
  PLAY_STORE_COUNTRY=in ^
  PLAY_STORE_LANGUAGE=en ^
  PORT=8000 ^
  SCHEDULER_INTERVAL_MINUTES=10080

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to set environment variables
    pause
    exit /b 1
)
echo [OK] Environment variables set
echo.

REM Step 4: Deploy with Docker
echo ============================================
echo   Step 4: Deploy to Railway with Docker
echo ============================================
echo.
echo This will take 3-5 minutes. Please wait...
echo.

railway up --dockerfile Dockerfile

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Deployment failed
    pause
    exit /b 1
)
echo [OK] Deployment successful
echo.

REM Step 5: Get Railway URL
echo ============================================
echo   Step 5: Get Your Railway URL
echo ============================================
echo.

railway domain

echo.
echo OR check dashboard:
railway open

echo.
echo ============================================
echo   Deployment Complete!
echo ============================================
echo.
echo Your backend is now deployed to Railway
echo.
echo NEXT STEPS:
echo 1. Note your Railway URL from above
echo 2. Test the endpoints using these commands:
echo.
echo    curl https://YOUR_URL.up.railway.app/api/reviews/stats
echo.
echo 3. Open API docs in browser:
echo    https://YOUR_URL.up.railway.app/docs
echo.
echo 4. Test Play Store fetch:
echo    curl -X POST https://YOUR_URL.up.railway.app/api/reviews/fetch-play-store ^
      -H "Content-Type: application/json" ^
      -d "{\"app_id\":\"com.whatsapp\",\"weeks\":4}"
echo.
echo See BACKEND_DEPLOYMENT_STEPS.md for detailed testing guide
echo.
pause
