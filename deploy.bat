@echo off
REM ==========================================
REM Deployment Script for Vercel + Railway
REM ==========================================

echo.
echo ============================================
echo   App Review Insights Analyzer - Deployment
echo ============================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install from https://nodejs.org/
    exit /b 1
)

echo [INFO] Node.js version:
node --version
echo.

REM ==========================================
REM Deploy Backend to Railway
REM ==========================================
echo ============================================
echo   Step 1: Deploy Backend to Railway
echo ============================================
echo.

cd backend

REM Check if Railway CLI is installed
where railway >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Installing Railway CLI...
    npm install -g @railway/cli
)

echo [INFO] Logging in to Railway...
railway login

echo.
echo [INFO] Linking to Railway project...
railway link

echo.
echo [INFO] Setting environment variables...
set /p GEMINI_KEY="Enter Gemini API Key: "
set /p GMAIL_EMAIL="Enter Gmail Address: "
set /p GMAIL_PASS="Enter Gmail App Password (no spaces): "
set /p RECIPIENT="Enter Recipient Email: "
set /p VERCEL_URL="Enter Vercel URL (for CORS): "

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

echo.
echo [INFO] Deploying to Railway with Docker...
railway up --dockerfile Dockerfile

echo.
echo [SUCCESS] Backend deployed to Railway!
echo.

cd ..

REM ==========================================
REM Deploy Frontend to Vercel
REM ==========================================
echo ============================================
echo   Step 2: Deploy Frontend to Vercel
echo ============================================
echo.

cd frontend

REM Check if Vercel CLI is installed
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Installing Vercel CLI...
    npm install -g vercel
)

echo [INFO] Logging in to Vercel...
vercel login

echo.
echo [INFO] Linking to Vercel project...
vercel link

echo.
echo [INFO] Setting environment variables...
set /p RAILWAY_URL="Enter Railway Backend URL: "

vercel env add VITE_API_BASE_URL https://%RAILWAY_URL%/api

echo.
echo [INFO] Deploying to Vercel...
vercel --prod

echo.
echo [SUCCESS] Frontend deployed to Vercel!
echo.

cd ..

REM ==========================================
REM Summary
REM ==========================================
echo ============================================
echo   Deployment Complete!
echo ============================================
echo.
echo Backend:  https://your-app-production.up.railway.app
echo Frontend: https://your-app.vercel.app
echo.
echo Next Steps:
echo 1. Test the frontend URL in your browser
echo 2. Verify backend API is accessible
echo 3. Test email delivery
echo 4. Monitor Railway logs for scheduler
echo.
pause
