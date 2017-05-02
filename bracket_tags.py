# Finds comment tags in Java files
from pathlib import Path
import sys
import shutil
import config
import re
import os
import pprint
from collections import Counter

look_for = re.compile("^//\s*\{")

if __name__ == '__main__':
    all = list()
    for md in config.example_dir.glob("**/*.java"):
        lines = md.read_text().splitlines()
        for n, line in enumerate(lines):
            if look_for.search(line):
                all.append(line)
    for k, v in sorted(Counter(all).items()):
        print("[{}]\t{}".format(v, k))
