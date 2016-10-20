%echo off
if "%GIT_HOME%"=="" (
  echo Please set GIT_HOME
  exit /B
)
cd %GIT_HOME%\OnJava-Tools
git pull
cd %GIT_HOME%\OnJava-Examples
git pull
cd %GIT_HOME%\on-java
git pull

rem if %COMPUTERNAME% == TEENYVERSE (
rem cd C:\Users\bruce\Documents\Git\OnJava-Tools
rem git pull
rem cd C:\Users\bruce\Documents\Git\OnJava-Examples
rem git pull
rem cd C:\Users\bruce\Documents\Git\on-java
rem git pull
rem ) Else (
rem cd C:\Users\Bruce\Documents\GitHub\OnJava-Tools
rem git pull
rem cd C:\Users\Bruce\Documents\GitHub\OnJava-Examples
rem git pull
rem cd C:\Users\Bruce\Documents\GitHub\on-java
rem git pull
rem )