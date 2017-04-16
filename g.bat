@echo off
pushd %~dp0
py -3 %~dp0recreate_github_examples.py %*
popd
