from pathlib import Path
import sys
import shutil
import config
import re
import os

def say(str):
    try:
        print(str)
    except:
        print(str.encode("utf-8"))


printed = []
def print_once(arg):
    if arg in printed:
        return
    printed.append(arg)
    print(arg)

if __name__ == '__main__':
    for md in config.markdown_dir.glob("[0-9][0-9]_*.md"):
        lines = md.read_text(encoding="utf-8").splitlines()
        for n, line in enumerate(lines):
            if re.match("={6,}", line) or re.match("-{6,}", line):
                if re.search("\d+", lines[n-1]):
                    continue
                if not re.search("\w+", lines[n-1]):
                    continue
                if len(line) != len(lines[n-1]):
                    os.system("subl {}:{}".format(md, n))
                    print_once(md.name)
                    say(lines[n-1])
                    say(line)