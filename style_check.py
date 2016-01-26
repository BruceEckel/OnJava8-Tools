from pathlib import Path
import sys
import shutil
import config
import re
import os
import pprint
from linewidth import check_listing_widths

def open_on_line(md, n):
    os.system("subl {}:{}".format(md, n + 1))


exclusions = [
  "-i,",
  "Git/on-",
  "Git\on-",
  "(1)r on-",
  "(size - position)",
  "javap -c",
  "length - 1",
]
def exclude(line):
  for e in exclusions:
      if line.startswith(e) or line.endswith(e):
          return True
  return False

bad_hyph_start = re.compile("(-|---)[A-Za-z]+")
bad_hyph_end = re.compile(".*[A-Za-z]+(-|---)$")

exclusions2 = [
  "(size - position)",
  "javap -c",
  "length - 1",
]

neg_num = re.compile("-\d")

def inline_gapped_hyphenation(line):
    line = line.strip()
    for e in exclusions2:
        if e in line:
            return False
    if line.startswith("-"):
        line = line[1:]
    if not "-" in line:
        return False
    if neg_num.search(line):
        return False
    if "- " in line or " -" in line:
        return True

class Flag:
    def __init__(self):
        self.flag = False
    def invert(self):
        self.flag = False if self.flag else True
    def __bool__(self):
        return self.flag

def remove_listings(lines):
    in_listing = Flag()
    cleaned = []
    for line in lines:
        if line.startswith("```"):
            in_listing.invert()
            cleaned.append("")
            continue
        if in_listing:
            cleaned.append("")
        else:
            cleaned.append(line)
    return cleaned


def bad_hyphenation(lines, md):
    for n, line in enumerate(remove_listings(lines)):
        if exclude(line):
            continue
        if line.startswith("|") or "-----------------" in line:
            continue
        bhs = bad_hyph_start.match(line.strip())
        bhe = bad_hyph_end.match(line.strip())
        if bhs or bhe or inline_gapped_hyphenation(line):
            return open_on_line(md, n)
    return None


def comment_period(lines, md):
    for n, line in enumerate(lines):
        if (line.endswith("...")
            or "// this case." in line
            or "// functionality for each type of event." in line
            or "// with a thread-safe one." in line
            or "// the use of RTTI, is extensible." in line
            or "// with a thread-safe one." in line
            or "// generalize using generics in this case." in line
            ):
            continue
        if line.startswith("//") and line.strip().endswith("."):
            return open_on_line(md, n)
    return None


def check_listing_widths(lines, md):
    "Make sure listings don't exceed max width of %d" % config.code_width
    in_listing = False
    in_output = False
    for n, line in enumerate(lines):
        if line.startswith("/* Output:"):
            in_output = True
            continue
        if line.startswith("```java"):
            in_listing = True
            continue
        if line.startswith("```"):
            in_listing = False
            in_output = False
            continue
        # if in_listing:
        #     print(line, len(line), config.code_width -2, in_output)
        if in_listing and len(line) > (config.code_width -2) and not in_output:
            return open_on_line(md, n)


def long_main_style(lines, md):
    for n, line in enumerate(lines):
        if "main(String" in line:
            if "public static void main(String[] args) {" in line:
                continue
            if line.startswith("  main(String[] args) throws"):
                continue
            if line == "public static void main(String[])":
                continue
            if line == "  void main(String[] args) throws IOException {" and md.name == "17_Exceptions.md":
                continue
            return open_on_line(md, n)


def no_cuddle_parens_and_braces(lines, md):
    for n, line in enumerate(lines):
        if '''(abc){2,}''' in line:
            continue
        if "){" in line:
            return open_on_line(md, n)

twr_file = config.example_dir / "try_with_resources.txt"

def try_with_resources_style(lines, md):
    in_try = False
    with twr_file.open('a') as twr_output:
        for n, line in enumerate(lines):
            if "Entry" in line or "industry" in line or "Registry(" in line:
                continue
            if "try(" in line or "try (" in line:
                in_try = True
                print("[> {}:{}\n".format(md.name, n), file=twr_output)
            if in_try is True:
                print(line, file=twr_output)
            if "{" in line and in_try is True:
                in_try = False
                print("\n\n", file=twr_output)



def post_listing_blank(lines, md):
    for n, line in enumerate(lines):
        if line == "```" and lines[n+1] != "":
            return open_on_line(md, n)


def test(md):
    print(md.name)
    lines = md.read_text(encoding="utf-8").splitlines()
    bad_hyphenation(lines, md)
    comment_period(lines, md)
    check_listing_widths(lines, md)
    long_main_style(lines, md)
    no_cuddle_parens_and_braces(lines, md)
    try_with_resources_style(lines, md)
    # post_listing_blank(lines, md)


if __name__ == '__main__':
    if twr_file.exists():
        twr_file.unlink()
    start = ""
    if len(sys.argv) > 1:
        start = sys.argv[1]
    for md in config.markdown_dir.glob(start + "*.md"):
        test(md)
    os.system("subl {}".format(twr_file))
