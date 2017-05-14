# py -3
# -*- coding: utf8 -*-
"""
Manage spell checking using aspell

"""
from pathlib import Path
import os
import sys
import re
import pprint
import shutil
from betools import CmdLine
from sortedcontainers import SortedSet
from ebook_build import *
import config

# print(combined.encode("windows-1252"))

def filter_out_code(text):
    "Remove all code listings from text"
    result = []
    index = 0
    code = False
    for line in text.splitlines():
        if line.startswith("```"):
            code = not code
            continue
        if code:
            continue
        result.append(line)
    decoded = "\n".join(result)
    config.stripped_for_style.write_text(decoded + "\n", encoding="utf8")
    stripped = re.sub(r'`.*?`', ' ', decoded, flags=re.DOTALL)
    config.stripped_for_spelling.write_text(stripped + "\n", encoding="utf8")


@CmdLine('s')
def spell_combined_files():
    """
    Put markdown files together and filter out code to prepare for aspell.
    """
    combine_markdown_files(config.markdown_dir, config.combined_markdown)
    filter_out_code(config.combined_markdown.read_text(encoding="utf-8"))
    os.chdir(str(config.build_dir))
    print("""
now run sp.bat
but correct spellings in the original using b -s
""")


def filter_comments(comments):
    clump = " ".join(comments)
    clump = clump.replace(":", "")
    clump = clump.replace(";", "")
    clump = clump.replace(",", "")
    parts = clump.split()
    parts2 = []
    for part in parts:
        if part.endswith("."):
            parts2.append(part[:-1])
        else:
            parts2.append(part)
    parts = [part for part in parts2 if (
        "*" not in part
        and "@" not in part
        and re.search("\w", part) # At least one letter
        and not re.search("[^A-Za-z]", part) # Nothing but letters
        )]
    return parts


def extract_java_code(text):
    "Return combined Java code listings"
    java_listings = re.findall("```java.*?```", text, re.DOTALL)
    just_code = "\n".join(java_listings)
    just_code = re.sub("/\* Output:.*?\*/", "", just_code, flags=re.DOTALL)
    just_code = re.sub("//\s+{.*?}", "//", just_code, flags=re.DOTALL)
    just_code = re.sub("```java\s+//[^\n]+", "```java", just_code, flags=re.DOTALL)
    config.java_code_only.write_text(just_code.strip() + "\n", encoding="utf8")

    slash_star = re.findall("[^*]/\*.*?\*/", just_code, re.DOTALL)
    slash_star = [line for line in slash_star if "/* ... */" not in line]
    slash_star = filter_comments(slash_star)

    slash_slash = []
    for ss in [ss.strip() for ss in re.findall("//.*", just_code)]:
        if ss == "// ...":
            continue
        if ss == "//":
            continue
        if "//" in ss[2:]:
            ss = "// " + (ss[2:].split("//")[1]).strip()
        if re.match("// \[\d+\]", ss):
            continue
        if ss.startswith("//-"):
            continue
        if ss.endswith(";"):
            continue
        if ss.endswith(":"):
            ss = ss[:-1]
        ss = ss[2:]
        ss = ss.replace("...","").strip()
        if ss.endswith("{") or ss.endswith("}"):
            continue
        slash_slash.append(ss)
    slash_slash = filter_comments(slash_slash)
    all_comments = SortedSet(slash_star + slash_slash)

    config.java_comments_only.write_text("\n".join(all_comments).strip() + "\n")


@CmdLine('c')
def extract_comments_for_spellchecking():
    """
    Put markdown files together and extract comments from code to prepare for aspell.
    Produces onjava-code-only.md
    """
    combine_markdown_files(config.markdown_dir, config.combined_markdown)
    extract_java_code(config.combined_markdown.read_text(encoding="utf-8"))
    print("""
now run sp_comments.bat
but correct spellings in the original using b -s
""")


if __name__ == '__main__':
    CmdLine.run()


