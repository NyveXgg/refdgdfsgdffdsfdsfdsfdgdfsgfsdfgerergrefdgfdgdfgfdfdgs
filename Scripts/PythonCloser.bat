@echo off
title Nuclear Python Killer

for /f "tokens=2 delims=," %%i in ('wmic process get Name^,ProcessId^,CommandLine /format:csv ^| findstr /I python') do (
    taskkill /F /PID %%i >nul 2>&1
)

exit
