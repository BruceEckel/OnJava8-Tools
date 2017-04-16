@echo off
pushd %~dp0
py -3 %~dp0Reformat.py %*
popd
