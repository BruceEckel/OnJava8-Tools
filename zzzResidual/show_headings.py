# Requires Python 3.6
from pathlib import Path
import sys
import re
import config
from betools import CmdLine

@CmdLine("1", num_args="+")
def single_file():
    if len(sys.argv) < 2:
        print("Need argument: name of markdown file")
        sys.exit()
    md = config.markdown_dir / sys.argv[2]
    if not md.exists():
        print(sys.argv[2] + " doesn't exist in " + str(config.markdown_dir))
        sys.exit()
    process(md)


@CmdLine("a")
def all_files():
    for md in config.markdown_dir.glob("*.md"):
        # print(md.name)
        process(md)


def process(md):
    lines = md.read_text().splitlines()
    for n, line in enumerate(lines):
        indent = 0
        if re.match(r"^[=-]+$", line):
            heading = lines[n-1]
            highbound = len(heading) + 2
            lowbound = len(heading) - 2
            borderlen = len(line)
            if borderlen <= highbound and borderlen >= lowbound:
                if line.startswith("="):
                    print()
                print()
                print(heading)
                print(line)
        if re.match(r"^#{2,5} ", line):
            if line.startswith("#####"):
                indent = 12
            elif line.startswith("####"):
                indent = 8
            elif line.startswith("###"):
                indent = 4
            print(" " * indent + line)


if __name__ == '__main__':
    CmdLine.run()
