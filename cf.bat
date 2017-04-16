@echo off
pushd %~dp0
py -3 %~dp0CheckReformatted.py %*
popd
