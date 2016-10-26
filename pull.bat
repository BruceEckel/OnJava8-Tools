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
cd %GIT_HOME%\AtomicKotlin
git pull
cd %GIT_HOME%\BruceEckel.github.io
git pull
