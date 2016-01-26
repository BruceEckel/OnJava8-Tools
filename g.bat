@echo off
pushd %~dp0
python %~dp0recreate_github_examples.py %*
popd