@echo off
rem venv.bat

if exist virtualenv (
  if defined VIRTUAL_ENV (
    virtualenv\Scripts\deactivate.bat
  ) else (
    virtualenv\Scripts\activate.bat
  )
) else (
  py -m venv virtualenv
  virtualenv\Scripts\activate.bat
)
