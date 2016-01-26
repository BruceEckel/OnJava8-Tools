# py -3
# -*- coding: utf8 -*-
"""
Find text bugs in book

Spell checker Uses:
https://pythonhosted.org/pyenchant/api/enchant.html
"""
from pathlib import Path
import os
import sys
import re
from betools import CmdLine, ruler
import enchant
import difflib

rootPath = Path(sys.path[0]).parent / "on-java"
resource_path = rootPath / "resources"
markdown_dir = rootPath / "Markdown"
assert markdown_dir.exists()
build_dir = rootPath / "ebook_build"
example_path = rootPath / "ExtractedExamples"

code_listings = re.compile(r"```.*?```", re.DOTALL)

isolated_code_font = re.compile(r"[^`]`[^`]+?`[^`]")


@CmdLine('e')
def check_examples_against_extracted():
    """
    Compare extracted examples with those in markdown files
    """
    for md in markdown_dir.glob("[0-9][0-9]_*.md"):
        with md.open(encoding="utf8") as chapter:
            # print(md.name)
            for example in code_listings.findall(chapter.read()):
                lines = example.strip().splitlines()
                if lines[1].startswith("//") and lines[1].endswith(".java"):
                    slug = lines[1][3:].strip()
                    extracted = example_path / slug
                    if not extracted.is_file():
                        print("Doesn't exist: {}".format(extracted))
                    with extracted.open() as ex:
                        ex_lines = ex.read().strip().splitlines()
                    for i, line in enumerate(lines[1:-1]):
                        if line not in ex_lines[i]:
                            print(md.name)
                            print(slug)
                            print("chapter:   {}".format(line))
                            print("extracted: {}".format(ex_lines[i]))


@CmdLine('w')
def find_weird_characters():
    """
    Locate strange characters in markdown files
    """
    def is_ascii(s):
        return all(ord(c) < 128 or c in '‘’“”—ç…©ï–·' for c in s)

    with (build_dir / "weird_chars.txt").open('w', encoding="utf8") as weird:
        for md in markdown_dir.glob("[0-9][0-9]_*.md"):
            with md.open(encoding="utf8") as chapter:
                for line in chapter.read().splitlines():
                    if is_ascii(line):
                        continue
                    else:
                        print(line.encode("utf8"))


@CmdLine('p')
def purify_code_listings():
    """
    Ensure all characters in code listings are pure ascii
    """
    def pure_ascii(s):
        return all(ord(c) < 128 for c in s)
    badcode = build_dir / "bad_code_chars.txt"
    with badcode.open('w', encoding="utf8") as weird:
        for md in markdown_dir.glob("[0-9][0-9]_*.md"):
            with md.open(encoding="utf8") as chapter:
                for codeblock in code_listings.findall(chapter.read()):
                    for line in codeblock.splitlines():
                        if pure_ascii(line):
                            continue
                        else:
                            print(line.encode("utf8"))
                            weird.write(ruler(md.name))
                            weird.write(line + "\n")

    os.system("subl {}".format(badcode))


@CmdLine('f')
def strip_fenced_code_blocks():
    """
    Produce nocode.md from onjava-assembled.md by stripping out
    all code entities. Allows searching for items only in prose.
    """
    assembled = build_dir / "onjava-assembled.md"
    nocode = build_dir / "nocode.md"
    if not assembled.exists():
        print("Can't find onjava-assembled.md")
        sys.exit()
    with assembled.open(encoding="utf8") as ass:
        text = code_listings.sub("", ass.read())
        text = isolated_code_font.sub("", text)
    with nocode.open("w", encoding="utf8") as nc:
        nc.write(text)


# @CmdLine('t')
def find_embedded_backslash():
    """
    Extract tables into bugs.txt
    """
    with (build_dir / "bugs.txt").open('w', encoding="utf8") as bugs:
        for md in markdown_dir.glob("[0-9][0-9]_*.md"):
            bugs.write("## {}\n\n".format(md.name))
            with md.open(encoding="utf8") as chapter:
                # text = code_listings.sub("", chapter.read())
                text = chapter.read()
                for p in isolated_code_font.findall(text):
                    if "\\" in p:
                        bugs.write(p + "\n")


pg_exclude = [
    '1.  `Collection`',
    '2.  `Map`',
    '1.  `Creational`',
    '2.  `Structural`',
    '3.  `Behavioral`',
    '1.  `Remote proxy`',
    '2.  `Virtual proxy`',
    '3.  `Protection proxy`',
    '4.  `Smart reference`',
    '1.  `TbinList`',
    '2.  `sortBin()`',
]


@CmdLine('g')
def fix_programming_guidelines():
    """
    Change backquotes in appendix to **
    """
    assembled = build_dir / "onjava-assembled.md"
    headline = re.compile("(\d+\.\s+)`(.+?)`", re.DOTALL)

    def subheadline(matchobj):
        if matchobj.group(0) in pg_exclude:
            print(("(excluded) " + matchobj.group(0)).encode("utf8"))
            return matchobj.group(0)
        fixed = matchobj.group(1) + "**" + matchobj.group(2) + "**"
        print(fixed.encode("utf8"))
        return fixed
    with assembled.open(encoding="utf8") as ass:
        text = ass.read()
        text = headline.sub(subheadline, text)
    with (build_dir / "test.md").open("w", encoding="utf8") as test:
        test.write(text)


@CmdLine('s')
def spell_check():
    """
    Check spelling of non-code blocks
    """
    stripchars = '''()*"“”‘’`',+-.;:=<>?#&/![]{}\\…—‑–|~©0123456789^$%@'''
    # re_word = re.compile("[a-zA-Z’]+")
    wordset = set()
    refined_removed = list()
    looking_for = list()
    test_dir = build_dir / "spelling"
    if not test_dir.exists():
        test_dir.mkdir()

    def refine_set(ch):
        for w in set(wordset):
            if ch in w:
                wordset.remove(w)
                refined_removed.append(w)
                if ")" in w:
                    looking_for.append(w)
                for sw in w.split(ch):
                    newpart = sw.strip(stripchars)
                    if len(newpart) > 1:
                        wordset.add(newpart)

    for md in markdown_dir.glob("[0-9][0-9]_*.md"):
        with md.open(encoding="utf8") as chapter:
            text = code_listings.sub("", chapter.read())
            with (test_dir / md.name).open('w', encoding="utf8") as testfile:
                testfile.write(text)
            for word in text.split():
                wordset.add(word.strip(stripchars))
    for ch in "`<>(’-/—_.:{,|\\":
        refine_set(ch)
    # Remove single chars:
    for w in set(wordset):
        if len(w) <= 1:
            wordset.remove(w)
    d = enchant.Dict("en_US")
    with (resource_path / "Dictionary.txt").open("r", encoding="utf8") as local_dict:
        for word in local_dict.readlines():
            d.add(word.strip())
    with (build_dir / "misspelled.txt").open('w', encoding="utf8") as misspelled:
        for word in sorted(wordset):
            if not d.check(word):
                misspelled.write(word + "\n")

    with (build_dir / "refined_bugs.txt").open('w', encoding="utf8") as refined_bugs:
        for rr in refined_removed:
            refined_bugs.write(rr + "\n")

    with (build_dir / "lookingFor.txt").open('w', encoding="utf8") as lookingFor:
        for lf in looking_for:
            lookingFor.write(lf + "\n")


@CmdLine('2')
def spell_check_2():
    """
    Spellcheck that first separates backquoted items
    """
    stripchars = '''()*"“”‘’`',+-.;:=<>?#&/![]{}\\…—‑–|~©0123456789^$%@'''
    extract_backquoted = re.compile(r"`([^`]+?)`")
    wordset = set()
    backquoted_removed = list()
    refined_removed = list()
    test_dir = build_dir / "spelling"
    if not test_dir.exists():
        test_dir.mkdir()

    def refine_set(ch):
        for w in set(wordset):
            if ch in w:
                wordset.remove(w)
                refined_removed.append(w)
                for sw in w.split(ch):
                    newpart = sw.strip(stripchars)
                    if len(newpart) > 1:
                        wordset.add(newpart)

    def remove_backquoted(matchobj):
        backquoted_removed.append(matchobj.group(1))
        return ""

    for md in markdown_dir.glob("[0-9][0-9]_*.md"):
        with md.open(encoding="utf8") as chapter:
            text = code_listings.sub("", chapter.read())
            text = extract_backquoted.sub(remove_backquoted, text)
            with (test_dir / md.name).open('w', encoding="utf8") as testfile:
                testfile.write(text)
            for word in text.split():
                wordset.add(word.strip(stripchars))
    for ch in "`<>(’-/—_.:{,|\\":
        refine_set(ch)
    # Remove single chars:
    for w in set(wordset):
        if len(w) <= 1:
            wordset.remove(w)
    d = enchant.Dict("en_US")

    with (resource_path / "Dictionary.txt").open("r", encoding="utf8") as local_dict:
        for word in local_dict.readlines():
            d.add(word.strip())

    with (build_dir / "misspelled.txt").open('w', encoding="utf8") as misspelled:
        for word in sorted(wordset):
            if not d.check(word):
                misspelled.write(word + "\n")

    with (build_dir / "backquoted_all.txt").open('w', encoding="utf8") as backquoted_all:
        for br in backquoted_removed:
            backquoted_all.write(br + "\n")

    with (build_dir / "backquoted.txt").open('w', encoding="utf8") as backquoted:
        for br in sorted(set(backquoted_removed)):
            backquoted.write(br + "\n")


def adjusted_compare(extracted, repo_ex):
    repo_file_name = repo_ex.relative_to(rootPath.parent)
    with extracted.open() as ex:
        extracted_text = ex.read().strip()
    with repo_ex.open() as rep:
        repo_text = rep.read().strip()
        repo_text = repo_text.replace("//:", "//")
        repo_text = repo_text.replace("\n// ©2016 MindView LLC: see Copyright.txt", "")
        repo_text = repo_text.replace("\n///~", "")
        repo_text = repo_text.replace("*///~", "*/")
        repo_text = repo_text.replace("} ///~", "}")
        repo_text = repo_text.replace("} /* Output:", "}\n/* Output:")
    for dif in difflib.ndiff(repo_text.splitlines(True), extracted_text.splitlines(True)):
        if dif.startswith("- ") or dif.startswith("+ "):
            if(repo_file_name):
                print("==", repo_file_name)
                repo_file_name = None
            print(dif.strip())


if __name__ == '__main__':
    CmdLine.run()
