@echo off
REM -------------------------------
REM Configuration
REM -------------------------------
set PYTHON_CMD=python
set BACKEND_SCRIPT=chatbot.py
set FRONTEND_HTML=index.html

REM Optional: Path to a specific Python executable
REM set PYTHON_CMD=C:\Path\To\Your\Python\python.exe

REM -------------------------------
REM Start Python backend in background
REM -------------------------------
echo Starting Python backend...
start "" /b "%PYTHON_CMD%" "%~dp0%BACKEND_SCRIPT%"

REM Give backend some time to start
timeout /t 3 /nobreak >nul

REM -------------------------------
REM Open frontend in default browser
REM -------------------------------
echo Opening frontend...
start "" "%~dp0%FRONTEND_HTML%"

REM -------------------------------
REM Wait and monitor Python process
REM -------------------------------
:WAIT_LOOP
REM Check if Python backend is still running
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "python.exe" >NUL
if ERRORLEVEL 1 (
    echo Python backend has stopped. Exiting launcher.
    goto END
)
REM Optional: wait 5 seconds before checking again
timeout /t 5 /nobreak >nul
goto WAIT_LOOP

:END
echo Launcher finished.
exit
