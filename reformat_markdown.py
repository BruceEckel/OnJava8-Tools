"""
Reformats Pandoc-flavored Markdown, preserving hyphen cuddling.

Doesn't touch code listings.

Has the option to fix other issues as well, such as the underlines for section
headings and ensuring there are blank lines after various items.

"""
import config
import textwrap
import string
import pprint
import sys
import logging
from logging import debug
logfile = __file__.split('.')[0] + ".log"
logpath = config.tools_dir / logfile
if (logpath).exists():
    logpath.unlink()
logging.basicConfig(filename= logfile, level=logging.DEBUG)

subhead_chars = string.ascii_letters + string.digits + "`"


class MarkdownLines:
    """
    Manages the lines from a Markdown file
    """
    def __init__(self, doc_text):
        self.index = 0
        self.lines = []
        self.result = []
        for line in doc_text.splitlines():
            self.lines.append(line.rstrip())
        self.size = len(self.lines)
        self.eof = False
        self.errcount = 0
        #debug(pprint.pformat(self.lines))

    def line(self):
        if self.index < self.size:
            return self.lines[self.index]
        else:
            self.eof = True
            self.errcount += 1
            return "{-%d}" % self.errcount

    def blank(self): return len(self.line()) is 0

    def nonblank(self): return len(self.line()) is not 0

    def next_line(self):
        if self.eof:
            raise IndexError("next_line() out of range")
        return self.lines[self.index + 1]

    def next_line_blank(self): return len(self.next_line()) is 0

    def next_line_nonblank(self): return len(self.next_line()) is not 0

    def increment(self):
        if self.index < self.size:
            self.index += 1
        else:
            self.eof = True

    def transfer(self, count = 1):
        for i in range(count):
            if not self.eof:
                self.result.append(self.line())
                self.increment()


class ReformatMarkdownDocument(MarkdownLines):
    """
    Reformat an entire document, but only the paragraphs,
    not code or subheads or any other markup.
    """
    def __init__(self, doc_text, width = 80):
        super().__init__(doc_text)
        self.formatter = textwrap.TextWrapper(
            width = width,
            break_long_words = False,
            break_on_hyphens = False,
        )

    def reformat(self):
        # Chain-of-responsibility parser:
        while not self.eof:
            debug("=" * 40)
            debug(">>> Next line " + str(self.index) + ": " + str(self.line().encode("windows-1252")))
            if self.skip_marked_line(): continue
            if self.skipsubhead(): continue
            if self.skiplisting(): continue
            if self.skiptable(): continue
            if self.skip_blank_lines(): continue
            if self.reformat_paragraph(): continue
            raise ValueError("Illegal parser state")
        return "\n".join(self.result)
        # print(len(self.result))
        # for x in self.result:
        #     print(x.encode("windows-1252"))
        #     print()
        #     print("+" * 80)
        #     print()

    def skip_marked_line(self):
        debug("skip_marked_line: [" + self.line() + "]")
        if self.line().startswith((">", "!", "#", "<")):
            debug("skip_marked_line success")
            self.transfer(1)
            return True
        debug("skip_marked_line fail")
        return False

    def skipsubhead(self):
        debug("skipsubhead: [" + self.line() + "]")
        if (self.nonblank() and
            not self.eof and
            self.next_line().startswith(("-", "="))):
                debug("skipsubhead found " + self.next_line()[0])
                self.transfer(2)
                return True
        debug("skipsubhead fail")
        return False

    def skiplisting(self):
        "Skip anything marked as a code listing"
        debug("skiplisting: [" + self.line() + "]")
        if self.line().startswith("```"):
            debug("skiplisting found " + self.line())
            self.transfer(1)
            while not self.line().startswith("```"):
                self.transfer(1)
            self.transfer(1) # for closing ```
            return True
        debug("skiplisting fail")
        return False

    def skiptable(self):
        "Skip a markdown table"
        debug("skiptable: [" + self.line() + "]")
        if (self.blank() and
            not self.eof and
            self.next_line().startswith("+-")):
            debug("skiptable found")
            self.transfer(2)
            while self.line().startswith(("|", "+")):
                self.transfer(1)
            return True
        debug("skiptable fail")
        return False

    def skip_blank_lines(self):
        debug("skip_blank_lines: [" + self.line() + "]")
        if self.nonblank():
            debug("skip_blank_lines fail")
            return False
        while self.blank():
            debug("skip_blank_lines success")
            self.transfer()
        return True

    def reformat_paragraph(self):
        "Reformat a single normal prose markdown paragraph"
        debug("reformat_paragraph: [" + self.line() + "]")
        if self.blank():
            debug("reformat_paragraph fail")
            return False
        text = ""
        while self.nonblank() and not self.eof:
            text += self.line() + " "
            self.increment()
        # Remove double spaces:
        while text.find("  ") is not -1:
            text = text.replace("  ", " ")
        # Remove spaces around hyphens:
        while text.find("- ") is not -1:
            text = text.replace("- ", "-")
        while text.find(" -") is not -1:
            text = text.replace(" -", "-")
        self.result.append(self.formatter.fill(text))
        debug("reformat_paragraph success")
        return True


test = """
Note the
---
use of---
`@Override`. Without
-this annotation, if-
you didn't provide
-the exact method---
name or
--- signature, the `abstract` --- mechanism will see that-
you haven't implemented the `abstract`-method and - produce a compile-time
error.
Thus,
you could
-effectively argue
-
 that---`@Override` is-redundant here.
However, `@Override`---also gives-the reader-a signal - that this---method is
overriden---I consider-that useful, and-so will---use `@Override` even-when the-
compiler would---still inform-me of---mistakes.
"""

if __name__ == '__main__':
    print(reformat_paragraph(test, width=50))
