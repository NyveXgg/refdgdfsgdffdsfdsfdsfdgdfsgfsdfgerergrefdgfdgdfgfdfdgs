@echo off
title Close all Python processes

echo Closing all Python processes...

:: Kill python.exe
taskkill /F /IM python.exe >nul 2>&1

:: Kill pythonw.exe
taskkill /F /IM pythonw.exe >nul 2>&1

:: Kill pip.exe (optional)
taskkill /F /IM pip.exe >nul 2>&1

echo All Python processes have been closed.
pause
