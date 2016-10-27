"""
Reformats Pandoc-flavored Markdown, preserving hyphen cuddling
"""
import textwrap

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

def reformat_document(doc_text, width = 80):
    """
    Reformat an entire document, but only the paragraphs,
    not code or subheads or any other markup.
    """
    result = []
    lines = doc_text.split()
    n = 0
    while n < len(lines):




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
