@echo off
title Konsultabot - EVSU DULAG AI Chatbot
echo.
echo ========================================
echo   Konsultabot - EVSU DULAG AI Chatbot
echo ========================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

:: Start main application
if exist "main.py" (
    echo Starting Konsultabot...
    echo.
    python main.py
) else (
    echo ERROR: main.py not found!
    echo Please ensure you're in the correct directory.
    echo.
    pause
    exit /b 1
)

:: If application exits with error
if errorlevel 1 (
    echo.
    echo Application encountered an error.
    echo Check the log files for details.
    echo.
    pause
)
