from pathlib import Path
import sys
import shutil
import config
import re
import os
import pprint
from collections import Counter

look_for = re.compile("^//\s*\{")

exclusions = [
    "{Args:",
    "{Exec:",
    "{Requires:",
    "{JVMArgs:",
    "{RunFirst:",
    "{main:",
    "{TimeOut",
]

def include(line):
    for e in exclusions:
        if e in line:
            return False
    return True

if __name__ == '__main__':
    all = list()
    for md in config.example_dir.glob("**/*.java"):
        lines = md.read_text().splitlines()
        for n, line in enumerate(lines):
            if look_for.search(line) and include(line):
                all.append(line)
    # pprint.pprint(sorted(all))
    for k, v in sorted(Counter(all).items()):
        print("[{}]\t{}".format(v, k))