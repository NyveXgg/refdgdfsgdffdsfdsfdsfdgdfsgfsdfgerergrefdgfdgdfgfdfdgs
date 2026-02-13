@echo off
title Kill ALL Python Processes
echo Killing all Python related processes...

:: Kill by common process names
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
taskkill /F /IM pip.exe >nul 2>&1
taskkill /F /IM py.exe >nul 2>&1

:: Kill everything that contains "python" in process list
for /f "skip=1 tokens=2 delims=," %%i in ('wmic process where "CommandLine like '%%python%%'" get ProcessId /format:csv') do (
    taskkill /F /PID %%i >nul 2>&1
)

:: Kill virtualenv python too
for /f "skip=1 tokens=2 delims=," %%i in ('wmic process where "Name like '%%python%%'" get ProcessId /format:csv') do (
    taskkill /F /PID %%i >nul 2>&1
)

echo All Python-related processes terminated.
pause
