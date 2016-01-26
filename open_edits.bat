@setlocal enabledelayedexpansion && py -3 -x "%~f0" %* & exit /b !ERRORLEVEL!
from pathlib import Path
import sys
import config
import os

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: open_edits edits_file.txt")
        sys.exit()
    for line in (Path(".") / sys.argv[1]).read_text().splitlines():
        if line.startswith("[>"):
            line = line[2:].strip()
            fname, num = line.split(":")
            md = config.markdown_dir / fname
            os.system("subl {}:{}".format(md, int(num) + 1))