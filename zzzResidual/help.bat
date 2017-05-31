@setlocal enabledelayedexpansion && py -3 -x "%~f0" %* & exit /b !ERRORLEVEL!
#start python code here
import sys
import importlib
if sys.argv[1:]:
    for arg in sys.argv[1:]:
        if arg.endswith(".py"):
            arg = arg[:-len(".py")]
        module = importlib.import_module(arg)
        print(type(module))
        print(dir(module))
        print(module.__doc__)
else:
    print("""
    Reusable Hacking Help System
    Running "Help" with no arguments displays doc info
    from all Python files that use @CmdLine
    Running "Help" with a file name displays doc info
    from only that Python file
    """)
