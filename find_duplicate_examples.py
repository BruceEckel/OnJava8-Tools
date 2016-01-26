from pathlib import Path
import sys
import shutil
import config
import re
import os
import pprint

look_for = re.compile("^//\s+.*\.java")

examples = []

if __name__ == '__main__':
    for md in config.markdown_dir.glob("*.md"):
        lines = md.read_text(encoding="utf-8").splitlines()
        for n, line in enumerate(lines):
            if look_for.fullmatch(line):
                if line in examples:
                    print("Multiple use:", line)
                examples.append(line)
