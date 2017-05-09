from pathlib import Path
import sys
import shutil
import config
import re
import os

look_for = re.compile("\Wtry\s*\(")

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
    for md in config.example_dir.glob("**/*.java"):
        lines = md.read_text(encoding="utf-8").splitlines()
        for n, line in enumerate(lines):
            if look_for.search(line):
                os.system("subl {}:{}".format(md, n+1))
                print_once(md.name)
                say(line)