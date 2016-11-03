@echo off
pushd %~dp0
python %~dp0CheckReformatted.py %*
popd
