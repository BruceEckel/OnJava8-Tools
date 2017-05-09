# Various tests to check Pandoc-flavored markdown documents
# Used in "On Java 8"
import os
import re
import shutil
import sys
from collections import Counter
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
            if re.match("={5,}", line) or re.match("-{5,}", line):
                if re.search("\d+", lines[n - 1]):
                    continue
                if not re.search("\w+", lines[n - 1]):
                    continue
                marked_headings.append(lines[n - 1])
                marked_headings.append(line)
                pure_headings.append(lines[n - 1])
    return pure_headings, marked_headings


@CmdLine("s")
def show_all_headings():
    "Display all markdown headings in book"
    pure, marked = find_headings()
    for m in marked:
        print(m)


@CmdLine("c")
def check_underlined_section_heads():
    "Check lengths of '-' and '=' used to mark section heads"
    pure, marked = find_headings()
    marked = [good for good in marked if not good.startswith("#")]
    for name, underline in zip(marked[::2], marked[1::2]):
        if '-' not in underline and '=' not in underline:
            print("Error in underline: {}".format(underline))
            sys.exit(1)
        # print("name: {}\nunderline:{}".format(name, underline))
        if len(name) != len(underline):
            print(name)
            print(underline)



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


@CmdLine("l")
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
    assert config.combined_markdown.exists()
    book = remove_code(Path(config.combined_markdown).read_text(
        encoding="utf8")).splitlines()
    for n, line in enumerate(book):
        if line.startswith("-") or line.rstrip().endswith("-"):
            if re.match("^-{1,2}[^- ]+", line) or re.search("[^-]+-{1,2}$", line):
                print("[{}]: {}".format(n, line))
                # os.system("subl {}:{}".format(config.combined_markdown, n))


@CmdLine('t')
def find_all_bracket_tags():
    "Find comment tags in Java files"
    look_for = re.compile("^//\s*\{")
    all = list()
    for md in config.markdown_dir.glob("[0-9][0-9]_*.md"):
        lines = md.read_text().splitlines()
        for n, line in enumerate(lines):
            if look_for.search(line):
                all.append(line)
    for k, v in sorted(Counter(all).items()):
        print("[{}]\t{}".format(v, k))


@CmdLine('x')
def show_NUL_bytes_in_output():
    """Look for NUL bytes in output files`"""
    normals = list(config.example_dir.rglob("*.out"))
    if len(normals) == 0:
        print("no *.out files found; execute 'gradlew run' first")
        sys.exit(1)
    for normal in normals:
        with normal.open() as codeFile:
            if "\0" in codeFile.read():
                os.system("subl {}".format(normal))
                print(normal)
    for errors in config.example_dir.rglob("*.err"):
        with errors.open() as codeFile:
            if "\0" in codeFile.read():
                os.system("subl {}".format(errors))
                print(errors)


@CmdLine('b')
def blankOutputFiles():
    """
    Show java files with expected output where there is none
    (Not sure if this is working right)
    """
    find_output = re.compile(r"/\* Output:(.*)\*/", re.DOTALL)
    for java in config.example_dir.rglob("*.java"):
        with java.open() as codeFile:
            output = find_output.search(codeFile.read())
            if output:
                # print(output.group(1))
                if not output.group(1).strip():
                    print(java)


if __name__ == '__main__':
    CmdLine.run()
