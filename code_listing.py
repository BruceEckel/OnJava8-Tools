"""
Capture fenced code listings
"""
import config
from pathlib import Path

# Candidate for betools, after adding the "ignore unknown characters" option:
def show(thing):
    try:
        print(thing.rstrip())
    except:
        print(thing.rstrip().encode("windows-1252"))


class CodeListing:

    def __init__(self, book, begin_line):
        self.book = book
        self.startfence = None
        self.endfence = None
        for n in range(begin_line, len(book)):
            if book[n].startswith("```"):
                self.startfence = n
                break
        if self.startfence is None:
            return
        for n in range(self.startfence + 1, len(book)):
            if book[n].startswith("```"):
                self.endfence = n
                break

    def ensure_trailing_space(self):
        trailing_line = self.book[self.endfence + 1].rstrip()
        if len(trailing_line):
            show(trailing_line)

    def check_listing_width(self):
        pass

    def __repr__(self):
        return str("".join([self.book[n] for n in range(self.startfence, self.endfence + 1)]))

    def __getitem__(self, index):
        return self.book[self.startfence + 1 + index]

    def __iter__(self):
        for line in self.book[self.startfence + 1 : self.endfence]:
            yield line

    def after(self):
        print("after: {}".format(self.book[self.endfence + 1].encode("windows-1252")))

    def dump(self):
        print("*" * 70)
        for n in range(self.startfence, self.endfence + 1):
            show(self.book[n].rstrip())
        self.after()
        print("=" * 70)

    @staticmethod
    def next(code_listing):
        cl = CodeListing(code_listing.book, code_listing.endfence + 1)
        if cl.startfence:
            return cl
        return None

    @staticmethod
    def parse_listings(book_file_name):
        with Path(book_file_name).open(encoding="utf8") as bk:
            book = bk.readlines()
        listings = []
        code_listing = CodeListing(book, 0)
        while code_listing:
            listings.append(code_listing)
            code_listing = CodeListing.next(code_listing)
        return listings

    @staticmethod
    def show_all_listings(listing_list):
        for listing in listing_list:
            for line in listing:
                show(line)
            print("-" * 80)