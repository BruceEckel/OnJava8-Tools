import os
import re
import shutil
import sys
from pathlib import Path
from betools import CmdLine
import config


def find_headings():
    "Find all markdown headings in book"
    marked_headings = []
    pure_headings = []
    for md in config.markdown_dir.glob("[0-9][0-9]_*.md"):
        lines = md.read_text(encoding="utf-8").splitlines()
        for n, line in enumerate(lines):
            if line.startswith("##"):  # Must be at least two
                marked_headings.append(line)
                pure_headings.append(line.split(maxsplit=1)[1])
                continue
            if re.match("={6,}", line) or re.match("-{6,}", line):
                if re.search("\d+", lines[n - 1]):
                    continue
                if not re.search("\w+", lines[n - 1]):
                    continue
                marked_headings.append(lines[n - 1])
                marked_headings.append(line)
                pure_headings.append(lines[n - 1])
    return pure_headings, marked_headings
    # if len(line) != len(lines[n - 1]):
    #     os.system("subl {}:{}".format(md, n))


@CmdLine("s")
def show_all_headings():
    "Display all markdown headings in book"
    pure, marked = find_headings()
    for p in pure:
        print(p)


def remove_code(doc):
    cleaned = []
    inside_code = False
    for line in doc.splitlines():
        if inside_code:
            if line.startswith("```"):
                inside_code = False
            continue
        if line.startswith("```"):
            inside_code = True
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def find_links():
    cleaned_doc = ""
    for md in config.markdown_dir.glob("[0-9][0-9]_*.md"):
        cleaned_doc += remove_code(md.read_text(encoding="utf-8")) + "\n"
    raw = re.findall("[^^`]\[.*?\].", cleaned_doc, re.DOTALL)
    links = [link.strip()[:] for link in raw
             if not link.endswith("(")
             and not link.endswith("*")
             and not link.endswith("`")
             and not link.startswith("\\")
             ]
    links2 = []
    for link in links:
        link = link.strip()
        if link.endswith("]"):
            links2.append(link)
        else:
            links2.append(link[:-1])
    links2 = [link for link in links2 if not link.endswith("]]")]
    links2 = [link for link in links2 if not "[]" in link]
    return [" ".join(link.split()) for link in links2]


@CmdLine("c")
def check_links_against_headings():
    "check [Cross Links] to ensure they all match a heading"
    link_text = [link[1:-1] for link in find_links()]
    pure, marked = find_headings()
    for link in link_text:
        if link not in pure:
            print(link)


@CmdLine('d')
def check_for_leading_or_trailing_dashes():
    "Make sure there are no lines with broken hyphenation"
    print("Checking for leading or trailing dashes")
    book = remove_code(Path(config.combined_markdown).read_text(encoding="utf8")).splitlines()
    for n, line in enumerate(book):
        if line.startswith("-") or line.rstrip().endswith("-"):
            if re.match("^-{1,2}[^- ]+", line) or re.search("[^-]+-{1,2}$", line):
                print("[{}]: {}".format(n, line))
                # os.system("subl {}:{}".format(config.combined_markdown, n))


if __name__ == '__main__':
    CmdLine.run()
