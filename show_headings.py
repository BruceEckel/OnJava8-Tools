from pathlib import Path
import sys
import shutil
import config
import re
import os

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Need argument: name of markdown file")
        sys.exit()
    md = config.markdown_dir / sys.argv[1]
    if not md.exists():
        print(sys.argv[1] + " doesn't exist in " + str(config.markdown_dir))
        sys.exit()
    lines = md.read_text().splitlines()
    for n, line in enumerate(lines):
        if re.match(r"^[=-]+$", line):
            heading = lines[n-1]
            highbound = len(heading) + 2
            lowbound = len(heading) - 2
            borderlen = len(line)
            if borderlen <= highbound and borderlen >= lowbound:
                if line.startswith("-"):
                    print()
                print(heading)
                print(line)
        if re.match(r"^#+", line):
            if line.startswith("#####"):
                indent = 12
            elif line.startswith("####"):
                indent = 8
            elif line.startswith("###"):
                indent = 4
            print(" " * indent + line)
