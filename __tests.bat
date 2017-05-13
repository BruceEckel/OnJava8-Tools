@echo off
py -3 %ONJAVA_TOOLS%\check_markdown.py -c
py -3 %ONJAVA_TOOLS%\check_markdown.py -l
py -3 %ONJAVA_TOOLS%\check_markdown.py -d
rem py -3 %ONJAVA_TOOLS%\check_markdown.py -x
echo run _check_markdown -d by hand
py -3 %ONJAVA_TOOLS%\check_markdown.py -b
