@echo off
title Study Assistant Setup
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Checking for Tesseract OCR...
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo Tesseract OCR is installed.
) else (
    echo Tesseract OCR is not installed.
    echo Please download and install Tesseract OCR from:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo After installation, please run this setup again.
    pause
    exit
)

echo.
echo Setting up directories...
mkdir "%USERPROFILE%\Documents\.temp_study_data" 2>NUL
mkdir "%USERPROFILE%\Documents\.temp_study_data\temp" 2>NUL

echo.
echo Checking Claude API key...
findstr /C:"YOUR_CLAUDE_API_KEY" src\stealth_capture.py > NUL
if %errorlevel% equ 0 (
    echo.
    echo WARNING: You need to set your Claude API key.
    echo Please edit src\stealth_capture.py and replace YOUR_CLAUDE_API_KEY with your actual API key.
    echo.
    pause
)

echo.
echo Setup complete! You can now run the application.
echo.
echo 1. Normal mode: python src/main.py
echo 2. Stealth mode: pythonw stealth_launcher.pyw
echo.
echo Would you like to start the program now?
echo 1. Start normal mode
echo 2. Start stealth mode
echo 3. Exit
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Starting normal mode...
    start python src/main.py
) else if "%choice%"=="2" (
    echo Starting stealth mode...
    start pythonw stealth_launcher.pyw
    echo Program is running in the background!
    echo Use Ctrl+Alt+L to capture a LeetCode problem.
    echo Use Ctrl+Alt+P to paste the solution.
) else (
    echo Exiting...
)

echo.
echo Thank you for using Study Assistant!
timeout /t 5 