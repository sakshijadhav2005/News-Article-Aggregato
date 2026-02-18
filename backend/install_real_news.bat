@echo off
echo ========================================
echo Installing Real News Packages
echo ========================================
echo.

pip install feedparser beautifulsoup4 requests lxml

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Now restart your backend:
echo   python run_simple.py
echo.
pause
