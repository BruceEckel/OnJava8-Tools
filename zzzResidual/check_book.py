#! python
"""
Check book for problems before building ebook
"""
import logging
from logging import debug
logging.basicConfig(filename= __file__.rsplit('.')[0] + '.log', level=logging.DEBUG)

from pathlib import Path
from pprint import pprint
from betools import CmdLine
from code_listing import CodeListing, show
import config

assert config.build_dir.exists()
assert config.combined_markdown.exists()


@CmdLine('w')
def check_listing_widths():
    "Make sure listings don't exceed max width of %d" % config.code_width
    listings = CodeListing.parse_listings(config.combined_markdown)
    for listing in listings:
        for n, line in enumerate(listing):
            if len(line) > config.code_width:
                print("-" * 60)
                print(listing[0].rstrip())
                print(n, end=": ")
                show(line)
                print("line length: %d" % len(line))


@CmdLine('t')
def check_for_trailing_hyphen():
    "Make sure there are no lines with broken hyphenation"
    with Path(config.combined_markdown).open(encoding="utf8") as bk:
        book = bk.readlines()
    for n, line in enumerate(book):
        if line.rstrip().endswith("-") and not line.rstrip().endswith("--"):
            print(n, end=": ")
            show(line)


@CmdLine('c')
def all():
    "Perform all checks"
    check_listing_widths()


if __name__ == '__main__':
    CmdLine.run()
