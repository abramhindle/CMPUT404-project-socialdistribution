@echo off
setlocal enableextensions

if not "%HEROKU_REDIRECTED%"=="1" if exist "%LOCALAPPDATA%\heroku\client\bin\heroku.cmd" (
  set HEROKU_REDIRECTED=1
  "%LOCALAPPDATA%\heroku\client\bin\heroku.cmd" %*
  goto:EOF
)

if not defined HEROKU_BINPATH set HEROKU_BINPATH="%~dp0heroku.cmd"
if exist "%~dp0..\bin\node.exe" (
  "%~dp0..\bin\node.exe" "%~dp0..\bin\run" %*
) else if exist "%LOCALAPPDATA%\oclif\node\node-12.21.0.exe" (
  "%LOCALAPPDATA%\oclif\node\node-12.21.0.exe" "%~dp0..\bin\run" %*
) else (
  node "%~dp0..\bin\run" %*
)
