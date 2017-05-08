import os
import re
import shutil
import sys
from pathlib import Path
from betools import CmdLine
import config


def find_headings():
    "Find all markdown headings in book"
    marked_headings = []
    pure_headings = []
    for md in config.markdown_dir.glob("[0-9][0-9]_*.md"):
        lines = md.read_text(encoding="utf-8").splitlines()
        for n, line in enumerate(lines):
            if line.startswith("##"): # Must be at least two
                marked_headings.append(line)
                pure_headings.append(line.split(maxsplit=1)[1])
                continue
            if re.match("={6,}", line) or re.match("-{6,}", line):
                if re.search("\d+", lines[n - 1]):
                    continue
                if not re.search("\w+", lines[n - 1]):
                    continue
                marked_headings.append(lines[n - 1])
                marked_headings.append(line)
                pure_headings.append(lines[n - 1])
    return pure_headings, marked_headings
                # if len(line) != len(lines[n - 1]):
                #     os.system("subl {}:{}".format(md, n))

@CmdLine("s")
def show_all_headings():
    "Display all markdown headings in book"
    pure, marked = find_headings()
    for p in pure:
        print(p)


if __name__ == '__main__':
    CmdLine.run()
