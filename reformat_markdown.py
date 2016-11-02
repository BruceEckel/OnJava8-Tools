"""
Reformats Pandoc-flavored Markdown, preserving hyphen cuddling.

Doesn't touch code listings.

Has the option to fix other issues as well, such as the underlines for section
headings and ensuring there are blank lines after various items.

        print(x.encode("windows-1252"))
"""
import config
import textwrap
import string
import pprint
import sys
import logging
from logging import debug
logging.basicConfig(filename= __file__.split('.')[0] + ".log", filemode='w', level=logging.DEBUG)
def debug(x): pass # Comment this to produce debug file

subhead_chars = string.ascii_letters + string.digits + "`"

END = "æ" # End sentinel: A character unused in the document

class MarkdownLines:
    """
    Manages the lines from a Markdown file
    """
    def __init__(self, doc_text):
        self.index = 0
        self.lines = []
        self.result = []
        for line in doc_text.strip().splitlines():
            self.lines.append(line.rstrip())
        self.size = len(self.lines)
        self.end = False

    def not_eof(self):
        if self.index >= self.size:
            self.end = True
        return not self.end

    def line(self):
        if self.not_eof():
            return self.lines[self.index]
        return END

    def next_line(self):
        if self.index + 1 < self.size:
            return self.lines[self.index + 1]
        else:
            return END

    def increment(self):
        if self.index + 1 < self.size:
            self.index += 1
        else:
            self.end = True

    def blank(self): return len(self.line()) is 0

    def nonblank(self): return len(self.line()) is not 0

    def next_line_blank(self): return len(self.next_line()) is 0

    def transfer(self, count = 1):
        for _ in range(count):
            if self.not_eof():
                self.result.append(self.line())
                self.increment()


class ReformatMarkdownDocument(MarkdownLines):
    """
    Reformat an entire document, but only the paragraphs,
    not code or subheads or any other markup.
    """
    def __init__(self, doc_name, doc_text, width = 80):
        super().__init__(doc_text)
        self.doc_name = doc_name
        self.normal_formatter = textwrap.TextWrapper(
            width = width,
            break_long_words = False,
            break_on_hyphens = False,
        )
        self.indent_formatter = textwrap.TextWrapper(
            width             = width,
            break_long_words  = False,
            break_on_hyphens  = False,
            initial_indent    = "    ",
            subsequent_indent = "    ",
        )
        # Skip header block:
        if self.line() == "---":
            while not self.line().startswith("...") and self.not_eof():
                self.transfer()
            self.transfer() # "..."


    def reformat(self):
        # Chain-of-responsibility parser:
        while self.not_eof():
            debug("=" * 40)
            debug("[" + self.doc_name + "] line " +
                str(self.index) + ": " +
                str(self.line().encode("windows-1252")))
            if self.special_line(): continue
            if self.subhead(): continue
            if self.listing(): continue
            if self.table(): continue
            if self.bulleted_block(): continue
            if self.numbered_block(): continue
            if self.blank_lines(): continue
            if self.reformat_paragraph(): continue
            raise ValueError("Illegal parser state")
        return "\n".join(self.result)

    def special_line(self):
        """
        Don't touch lines that should be left alone. Note that because
        every line is rstripped, a line that starts with a space is indented
        text and should be passed through untouched.
        """
        debug("special_line")
        if self.line().startswith((">", "!", "#", "<", " ")):
            self.transfer()
            debug("--> success")
            return True
        debug("--> fail")
        return False

    def subhead(self):
        debug("subhead")
        if (self.nonblank() and self.next_line().startswith(("-", "="))):
                debug("--> success: " + self.next_line()[0])
                self.transfer(2)
                return True
        debug("--> fail")
        return False

    def listing(self):
        "Skip anything marked as a code listing"
        debug("listing")
        if self.line().startswith("```"):
            self.transfer()
            while not self.line().startswith("```") and self.not_eof():
                self.transfer()
            self.transfer() # for closing ```
            debug("--> success")
            return True
        debug("--> fail")
        return False

    def table(self):
        "Skip a markdown table"
        debug("table")
        if self.line().startswith("+-"):
            self.transfer()
            while self.line().startswith(("|", "+")) and self.not_eof():
                self.transfer()
            debug("--> success")
            return True
        debug("--> fail")
        return False

    def fill_paragraph(self, formatter):
        text = ""
        while self.nonblank() and self.not_eof():
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
        return formatter.fill(text)

    def bulleted_block(self):
        debug("bulleted_block")
        if self.line().startswith("+ "):
            formatted = self.fill_paragraph(self.indent_formatter)
            formatted = formatted.replace("+ ", "", 1)
            formatted = formatted.replace("  ", "+ ", 1)
            self.result.append(formatted)
            debug("--> success:::")
            return True
        debug("--> fail")
        return False

    def numbered_block(self):
        debug("numbered_block")
        if self.line().startswith(
            ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")):
            formatted = self.fill_paragraph(self.indent_formatter).lstrip()
            num, par = formatted.split(".", 1)
            graph = "%-4s" % (num + "." )
            graph += par.lstrip()
            self.result.append(graph)
            debug("--> success:::")
            return True
        debug("--> fail")
        return False

    def blank_lines(self):
        debug("blank_lines")
        if self.nonblank():
            debug("--> fail")
            return False
        while self.blank() and self.not_eof():
            self.transfer()
        debug("--> success")
        return True

    def reformat_paragraph(self):
        "Reformat a single normal prose markdown paragraph"
        debug("reformat_paragraph")
        if self.blank(): # Is this possible?
            debug("--> fail")
            return False
        self.result.append(self.fill_paragraph(self.normal_formatter))
        debug("--> success")
        return True
