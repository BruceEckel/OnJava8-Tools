# py -3
"""
Ensures there's a space after each code listing
"""
import logging
from logging import debug
logging.basicConfig(filename='tmp.log', level=logging.DEBUG)

from pathlib import Path
import sys
from pprint import pprint
import re
from betools import CmdLine
from code_listing import CodeListing
import config

assert config.build_dir.exists()
assert config.combined_markdown.exists()


@CmdLine('s')
def space_after_each_listing_x():
    "Ensures there's a space after each code listing"
    with Path(config.combined_markdown).open(encoding="utf8") as ojmd:
        book = ojmd.readlines()
    cl = CodeListing(book, 0)
    while cl:
        cl.ensure_trailing_space()
        cl = CodeListing.next(cl)


if __name__ == '__main__':
    CmdLine.run()
