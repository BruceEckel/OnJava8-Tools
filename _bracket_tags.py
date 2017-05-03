# Finds comment tags in Java files
import os
import pprint
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

look_for = re.compile("^//\s*\{")

if __name__ == '__main__':
    all = list()
    for md in Path(".").glob("**/*.java"):
        lines = md.read_text().splitlines()
        for n, line in enumerate(lines):
            if look_for.search(line):
                all.append(line)
    for k, v in sorted(Counter(all).items()):
        print("[{}]\t{}".format(v, k))
