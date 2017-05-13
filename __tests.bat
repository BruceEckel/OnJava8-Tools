@echo off
echo *** Running _check_markdown -c ***
py -3 %ONJAVA_TOOLS%\check_markdown.py -c
echo *** Running _check_markdown -l ***
py -3 %ONJAVA_TOOLS%\check_markdown.py -l
echo *** Running _check_markdown -d ***
py -3 %ONJAVA_TOOLS%\check_markdown.py -d
rem py -3 %ONJAVA_TOOLS%\check_markdown.py -x
echo *** run _check_markdown -d by hand ***
echo *** Running _check_markdown -b ***
py -3 %ONJAVA_TOOLS%\check_markdown.py -b
echo *** Running _output_file_check -m ***
py -3 %ONJAVA_TOOLS%\_output_file_check.py -m
py -3 %ONJAVA_TOOLS%\_output_file_check.py -d
echo *** Running _verify_output -u ***
py -3 %ONJAVA_TOOLS%\_verify_output.py -u
