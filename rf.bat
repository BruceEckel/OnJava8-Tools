@echo off
pushd %~dp0
python %~dp0Reformat.py %*
popd
