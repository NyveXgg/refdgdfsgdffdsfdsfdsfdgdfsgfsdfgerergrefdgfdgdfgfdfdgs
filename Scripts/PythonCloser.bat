@echo off
taskkill /F /IM python.exe
taskkill /F /IM pythonw.exe
for /f "tokens=2" %%i in ('tasklist ^| findstr /I tsunami') do taskkill /F /PID %%i
exit
