@echo off
setlocal

if "%1"=="" (
    echo Usage: switch_env.bat [development|integration|production]
    exit /b 1
)

set ENV=%1

if not exist "..\.env.%ENV%" (
    echo Environment file .env.%ENV% not found!
    exit /b 1
)

copy /Y "..\.env.%ENV%" "..\.env"
echo Switched to %ENV% environment 