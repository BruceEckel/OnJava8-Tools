"""
Reformats Pandoc-flavored Markdown, preserving hyphen cuddling.

Doesn't touch code listings.

Has the option to fix other issues as well, such as the underlines for section
headings and ensuring there are blank lines after various items.

TODO: Create class that is just for managing lines in the doc, possibly called
Index or Lines. Keeps track of where you are, whether a line is blank or has
characters, whether the following line is blank or has characters, if you're at
the end, if you have a next line. You explicitly tell it to move the index
forward and at that point it calculates everything about where it is.

"""
import textwrap
import string

marker_chars = ">!#<"

subhead_chars = string.ascii_letters + string.digits + "`"

def reformat_paragraph(text, width = 80):
    "Reformat a single paragraph that is not-code or a subhead"
    formatter = textwrap.TextWrapper(
        width = width,
        break_long_words = False,
        break_on_hyphens = False,
      )
    text = text.strip().replace("\n", " ")
    while text.find("  ") is not -1:
      text = text.replace("  ", " ")
    while text.find("- ") is not -1:
      text = text.replace("- ", "-")
    while text.find(" -") is not -1:
      text = text.replace(" -", "-")
    return formatter.fill(text)


class ReformatDocument:
    """
    Reformat an entire document, but only the paragraphs,
    not code or subheads or any other markup.
    """
    def __init__(self, doc_text, width = 80):
        self.result = []
        self.lines = doc_text.split()
        self.n = 0

    def at_least_one(self, offset=0):
        "How to determine a blank line vs out of lines?"
        index = self.n + offset
        if index >= len(self.lines):
            return False
        if len(self.lines[index].strip()) == 0
            return False
        return True

    def at_least_two(self):
        return at_least_one() and at_least_one(1)

    def blank_line(self):
        return not at_least_one()

    def absorb(self, num_of_lines):
        for i in range(num_of_lines):
            if self.n < len(self.lines):
                self.result.append(self.lines[self.n])
                self.n += 1

    def skip_blank_line(self):
        if not self.at_least_one():
            self.absorb(1)
            return True

    def skip_marked_line(self):
        if self.at_least_one() and self.lines[self.n][0] in marker_chars:
            self.absorb(1)
            return True
        return False

    def skipsubhead(self):
        if not self.at_least_two():
            return False
        if self.lines[self.n][0] in subhead_chars and self.lines[self.n + 1][0] in "-=":
            self.absorb(2)
            return True
        return False

    def skiplisting(self):
        "skip anything marked as a code listing"
        if self.lines[self.n].startswith("```"):
            self.absorb(1)
            while not self.lines[self.n].startswith("```"):
                self.absorb(1)
            self.absorb(1)
            return True
        return False

    def skiptable(self):
        "skip a markdown table"
        if self.blank_line(): # followed by
            if at_least_one(1):
                if self.lines[self.n + 1].startswith("+-"):


    def start(self):
        while self.n < len(self.lines):
            if self.skip_marked_line(): continue
            if self.skipsubhead(): continue
            if self.skiplisting(): continue
            if self.skiptable(): continue
            if self.skip_blank_line(): continue




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
