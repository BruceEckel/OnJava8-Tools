@echo off
if exist %GIT_HOME%\AtomicKotlin\ExtractedExamples (
  cd %GIT_HOME%\AtomicKotlin\ExtractedExamples
) else (
  cd %GIT_HOME%\AtomicKotlin
)
%GIT_HOME%\AtomicKotlinBuilder\virtualenv\Scripts\activate.bat
