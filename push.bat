@echo off
echo ==========================================
echo           ELITE SYSTEM: GIT PUSH
echo ==========================================
echo.
echo Adding changes to git...
git add .
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] git add failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Committing changes...
git commit -m "feat(chat): remove Agora WebRTC calling, specialize in ultra-fast Instagram-style direct messaging"
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] git commit failed (perhaps no changes to commit?).
)

echo.
echo Pushing to GitHub...
git push
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] git push failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ==========================================
echo   SUCCESS: Changes successfully pushed!
echo ==========================================
echo.
pause
