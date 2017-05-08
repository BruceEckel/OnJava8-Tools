# py -3
# -*- coding: utf8 -*-
"""
Fix footnotes for Pandoc Markdown syntax
"""
from pathlib import Path
import sys
import re
from betools import CmdLine

rootPath = Path(sys.path[0]).parent / "on-java"
markdown_dir = rootPath / "Markdown"
assert markdown_dir.exists()

test_dir = rootPath / "test_footnotes"


@CmdLine('f')
def fix_footnotes():
    "Fix word-extracted footnotes to make them pandoc-markdown compatible"
    old_footnote = re.compile(r"\[\\\[(\d+)\\\]\]\(#_ftn\d+\)")
    if not test_dir.exists():
        test_dir.mkdir()

    def fix(matchobj):
        fixed = "[^" + matchobj.group(1) + "]"
        print(fixed)
        return fixed

    for md in markdown_dir.glob("[0-9][0-9]_*.md"):
        if "38_Appendix_OnBeingaProgrammer.md" in md.name:
            continue
        with md.open('r', encoding="utf8") as chp:
            print(md.name)
            chapter = chp.read()
            chapter = old_footnote.sub(fix, chapter)
        test_file = test_dir / md.name
        with test_file.open('w', encoding="utf8") as chp:
            chp.write(chapter)


if __name__ == '__main__':
    CmdLine.run()
