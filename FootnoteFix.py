# py -3
# -*- coding: utf8 -*-
"""
Modify footnotes to make them inline
"""
from pathlib import Path
import os
import sys
import re
from collections import OrderedDict
from betools import CmdLine

rootPath = Path(sys.path[0]).parent / "on-java"
markdown_dir = rootPath / "Markdown"
assert markdown_dir.exists()
build_dir = rootPath / "ebook_build"
combined_markdown = build_dir / "onjava-assembled.md"
extracted_footnotes = build_dir / "extracted-footnotes.txt"
reformatted_footnotes = build_dir / "reformatted-footnotes.txt"
fixed_markdown = build_dir / "onjava-assembled-footnotes-fixed.md"


# @CmdLine('c')
def combine_markdown_files():
    """
    Put markdown files together
    """
    assembled = ""
    for md in markdown_dir.glob("[0-9][0-9]_*.md"):
        print(str(md.name), end=", ")
        with md.open(encoding="utf8") as chapter:
            assembled += chapter.read() + "\n"
    with combined_markdown.open('w', encoding="utf8") as book:
        book.write(assembled)
    print("\n\n")


@CmdLine('f')
def inline_footnotes():
    """
    Convert footnotes to inline
    """
    if not combined_markdown.exists():
        combine_markdown_files()
    with combined_markdown.open(encoding="utf8") as book:
        text = book.read()
    footnotes = OrderedDict()
    fnote = re.compile("^\[\^(\d+)\]:", re.MULTILINE)
    parts = fnote.split(text)
    del parts[0]
    pairs = zip(parts[::2], parts[1::2])
    for p in pairs:
        footnotes[p[0]] = p[1].strip()
    # for k, v in footnotes.items():
    #     print("{}: {}\n".format(k, v.encode("utf8")))
    with extracted_footnotes.open('w', encoding="utf8") as fnotes:
        for k, v in footnotes.items():
            fnotes.write("{}: {}\n\n".format(k, v))
    numbers = [int(k) for k in footnotes]
    for x in range(1, numbers[-1]):
        if x not in numbers:
            print("missing", x)
    with reformatted_footnotes.open('w', encoding="utf8") as rfnotes:
        def footnote_fix(matchobj):
            index = matchobj.group(1)
            # new_footnote = matchobj.group(0) + ": {}\n\n".format(footnotes[index])
            new_footnote = "^[{}]\n".format(footnotes[index])
            rfnotes.write(new_footnote)
            return new_footnote
        text = re.sub('\[\^(\d+)\][^:]', footnote_fix, text)
    fixed_markdown.write_text(text, encoding="utf8")
    os.system("subl {}".format(reformatted_footnotes))
    os.system("subl {}".format(fixed_markdown))


if __name__ == '__main__':
    CmdLine.run()
