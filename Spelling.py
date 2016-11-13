# py -3
# -*- coding: utf8 -*-
"""
Manage spell checking using aspell

"""
from pathlib import Path
import os
import sys
import re
import shutil
from betools import CmdLine
from ebook_build import *
import config

# print(combined.encode("windows-1252"))


def filter_out_code(text):
    result = []
    index = 0
    code = False
    for line in text.splitlines():
        if line.startswith("```"):
            code = not code
            continue
        if code:
            continue
        result.append(line)
    decoded = "\n".join(result)
    config.stripped_for_style.write_text(decoded + "\n", encoding="utf8")
    stripped = re.sub(r'`.*?`', ' ', decoded, flags=re.DOTALL)
    config.stripped_for_spelling.write_text(stripped + "\n", encoding="utf8")


@CmdLine('s')
def spell_combined_files():
    """
    Put markdown files together and filter out code to prepare for aspell
    """
    combine_markdown_files(config.combined_markdown)
    filter_out_code(config.combined_markdown.read_text(encoding="utf-8"))
    os.chdir(str(config.build_dir))
    print("now run sp.bat")


if __name__ == '__main__':
    CmdLine.run()


