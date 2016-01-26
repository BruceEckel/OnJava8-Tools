@echo off
rem cd %~dp0
pushd %~dp0
python %~dp0Examples.py %*
popd
rem cd %~dp0/../ExtractedExamples
ant build
