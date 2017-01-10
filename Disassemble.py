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
import re
from collections import OrderedDict
from betools import CmdLine

assert config.markdown_dir.exists()
assert config.build_dir.exists()
combined_markdown = config.build_dir / "onjava-assembled.md"
assert config.combined_markdown.exists()
disassembled_dir = config.markdown_dir


@CmdLine('d')
def disassemble_combined_markdown_file():
    "turn markdown file into a collection of chapter-based files"
    with Path(combined_markdown).open(encoding="utf8") as ojmd:
        book = ojmd.read()
    chapters = re.compile(r"\n([A-Za-z\:\&\?\+\-\/\(\)\` ]*)\n=+\n")
    parts = chapters.split(book)
    names = parts[1::2]
    bodies = parts[0::2]
    chaps = OrderedDict()
    chaps["Front"] = bodies[0]
    for i, nm in enumerate(names):
        chaps[nm] = bodies[i + 1].strip() + "\n"

    def mdfilename(h1, n):
        fn = h1.replace(": ", "_")
        fn = fn.replace(" ", "_") + ".md"
        fn = fn.replace("&", "and")
        fn = fn.replace("?", "")
        fn = fn.replace("+", "P")
        fn = fn.replace("/", "")
        fn = fn.replace("-", "_")
        fn = fn.replace("(", "")
        fn = fn.replace(")", "")
        fn = fn.replace("`", "")
        return "%02d_" % n + fn

    for i, p in enumerate(chaps):
        disassembled_file_name = mdfilename(p, i)
        print(disassembled_file_name)
        dest = disassembled_dir / disassembled_file_name
        with dest.open('w', encoding="utf8") as chp:
            if "Front" not in p:
                chp.write(p + "\n")
                chp.write("=" * len(p) + "\n\n")
            chp.write(chaps[p])


if __name__ == '__main__':
    CmdLine.run()
