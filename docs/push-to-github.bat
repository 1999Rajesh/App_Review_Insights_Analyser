@echo off
REM ==========================================
REM Push Backend to GitHub - Automated Script
REM ==========================================

echo.
echo ============================================
echo   Push App Review Insights Analyzer to GitHub
echo ============================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed!
    echo Please install from https://git-scm.com/
    pause
    exit /b 1
)

echo [OK] Git found
git --version
echo.

REM Navigate to project directory
cd /d "%~dp0"

REM Check if already a git repository
if exist ".git" (
    echo [INFO] Git repository already exists
) else (
    echo [INFO] Initializing new git repository...
    git init
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to initialize git
        pause
        exit /b 1
    )
    echo [OK] Git repository initialized
)

echo.
echo ============================================
echo   Step 1: Add All Files
echo ============================================
echo.

git add .
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to add files
    pause
    exit /b 1
)
echo [OK] All files staged for commit
echo.

echo ============================================
echo   Step 2: Commit Changes
echo ============================================
echo.

git commit -m "Initial commit: App Review Insights Analyzer with Railway deployment

Features:
- Backend: FastAPI with Gemini AI (Phase 3)
- Frontend: React 18 + Vite + TypeScript  
- Auto-fetch from Google Play Store
- Weekly email reports via Gmail SMTP
- APScheduler running every 5 minutes
- Railway deployment with Docker
- Vercel deployment configuration
- Maximum 200 reviews for AI classification
- Modern glassmorphic UI design"

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to commit
    pause
    exit /b 1
)
echo [OK] Changes committed successfully
echo.

echo ============================================
echo   Step 3: Configure GitHub Remote
echo ============================================
echo.

REM Check if remote already exists
git remote | findstr "origin" >nul
if %ERRORLEVEL% EQU 0 (
    echo [WARNING] Remote 'origin' already exists
    set /p overwrite="Do you want to update it? (y/n): "
    if /i "%overwrite%"=="y" (
        git remote remove origin
    ) else (
        echo Skipping remote configuration
        goto :PUSH
    )
)

echo.
echo IMPORTANT: You need your GitHub repository URL ready
echo.
echo To create a repository:
echo 1. Go to https://github.com/new
echo 2. Enter repository name (e.g., app-review-insights-analyzer)
echo 3. Choose Public or Private
echo 4. DO NOT initialize with README
echo 5. Click Create Repository
echo 6. Copy the repository URL
echo.

set /p REPO_URL="Enter your GitHub repository URL: "

if "%REPO_URL%"=="" (
    echo [ERROR] No repository URL provided
    pause
    exit /b 1
)

echo.
echo Setting remote origin to: %REPO_URL%
git remote add origin %REPO_URL%

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to add remote origin
    echo Make sure the URL is correct and you have access
    pause
    exit /b 1
)
echo [OK] Remote origin configured
echo.

:PUSH
echo ============================================
echo   Step 4: Push to GitHub
echo ============================================
echo.

REM Rename branch to main
git branch -M main

echo Pushing to GitHub...
echo This may take a few minutes depending on file sizes
echo.

git push -u origin main

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to push to GitHub
    echo.
    echo Common issues:
    echo - Repository doesn't exist on GitHub
    echo - Incorrect repository URL
    echo - Authentication failed
    echo.
    echo Try these solutions:
    echo 1. Verify repository exists at: %REPO_URL%
    echo 2. Check you're logged into GitHub CLI or have credentials configured
    echo 3. Use HTTPS URL instead of SSH if having authentication issues
    pause
    exit /b 1
)

echo.
echo [OK] Successfully pushed to GitHub!
echo.

REM ==========================================
REM Summary
REM ==========================================
echo ============================================
echo   Push Complete!
echo ============================================
echo.
echo Your code has been pushed to GitHub:
echo %REPO_URL%
echo.
echo NEXT STEPS:
echo.
echo 1. Verify on GitHub:
echo    Open: %REPO_URL%
echo    Check that these files are present:
echo    - backend/Dockerfile
echo    - backend/requirements.txt
echo    - backend/app/ (all Python files)
echo    - frontend/ (all React files)
echo.
echo 2. Deploy to Railway:
echo    - Go to https://railway.app/
echo    - New Project ^→ Deploy from GitHub
echo    - Select: app-review-insights-analyzer
echo    - Set Root Directory: backend
echo    - Add environment variables
echo    - Deploy!
echo.
echo 3. Deploy to Vercel:
echo    - Go to https://vercel.com/
echo    - Add New ^→ Project
echo    - Import from GitHub
echo    - Select repository
echo    - Deploy!
echo.
echo See PUSH_TO_GITHUB_GUIDE.md for detailed instructions
echo.
pause
