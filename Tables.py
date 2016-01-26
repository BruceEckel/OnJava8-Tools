# py -3
# -*- coding: utf8 -*-
"""
Extract markdown tables into all_tables.md
"""
from pathlib import Path
import os
import sys
import re
from betools import CmdLine

rootPath = Path(sys.path[0]).parent / "on-java"
markdown_dir = rootPath / "Markdown"
assert markdown_dir.exists()
build_dir = rootPath / "ebook_build"

table_divider = re.compile(r"(?:\+[-=]+)+\+")


@CmdLine('t')
def extract_tables():
    """
    Extract tables into all_tables.md
    """
    with (build_dir / "all_tables.md").open('w', encoding="utf8") as all_tables:
        for md in markdown_dir.glob("[0-9][0-9]_*.md"):
            all_tables.write("## {}\n\n".format(md.name))
            with md.open(encoding="utf8") as chapter:
                lines = chapter.read().splitlines()
                in_table = False
                for line in lines:
                    if table_divider.match(line):
                        all_tables.write(line + "\n")
                        in_table = True
                    elif line.startswith('|') and line.endswith('|') and in_table:
                        all_tables.write(line + "\n")
                    elif in_table:
                        in_table = False
                        all_tables.write("\n")
                        all_tables.write("-" * 40)
                        all_tables.write("\n\n")


@CmdLine('e')
def convert_to_epub():
    "Pandoc all_tables.md to epub"
    os.chdir(str(build_dir))
    pandoc = "pandoc all_tables.md -f markdown-native_divs -t epub -o all_tables.epub  --epub-stylesheet=onjava.css"
    print(pandoc)
    os.system(pandoc)
    # shutil.copy("all_tables.epub", "all_tables.zip")
    # os.system("unzip all_tables.zip -d all_tables_epub_files")


@CmdLine('a')
def all():
    "Full conversion from start"
    extract_tables()
    convert_to_epub()
    os.system("start all_tables.epub /MAX")


if __name__ == '__main__':
    CmdLine.run()
