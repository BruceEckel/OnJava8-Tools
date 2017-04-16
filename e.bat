@echo off
cd %~dp0
py -3 %~dp0Examples.py %*
cd %EXTRACTED_EXAMPLES%
