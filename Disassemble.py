# py -3
# -*- coding: utf8 -*-
"""
TODO: normalize spaces at ends of files

Splits combined markdown file into chapters.

For use after mass edits on single document.
"""
import config
from pathlib import Path
import sys
from betools import CmdLine
import ebook_build

assert config.markdown_dir.exists()
assert config.build_dir.exists()
assert config.combined_markdown.exists()

@CmdLine('d')
def disassemble_combined_markdown_file():
    "turn markdown file into a collection of chapter-based files"
    ebook_build.disassemble_combined_markdown_file(config.combined_markdown)


if __name__ == '__main__':
    CmdLine.run()
