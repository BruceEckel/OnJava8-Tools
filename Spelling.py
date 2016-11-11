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
    return re.sub(r'`.*?`', ' ', decoded, flags=re.DOTALL)


@CmdLine('s')
def spell_combined_files():
    """
    Put markdown files together and filter out code to prepare for aspell
    """
    combine_markdown_files(config.combined_markdown)
    combined = filter_out_code(config.combined_markdown.read_text(encoding="utf-8"))
    config.stripped_for_spelling.write_text(combined + "\n", encoding="utf8")
    # os.system("subl {}".format(config.stripped_for_spelling))
    os.chdir(str(config.build_dir))
    # os.system("bash -c aspell {}".format(config.stripped_for_spelling.name))



if __name__ == '__main__':
    CmdLine.run()


# print(combined.encode("windows-1252"))
