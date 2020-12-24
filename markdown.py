#!/usr/bin/env python
import re
import sys
import os
import subprocess
from collections import OrderedDict
from pathlib import Path
import backtrace
import click
from directories import exists, erase

backtrace.hook(
    reverse=False,
    align=False,
    strip_path=False,
    enable_on_envvar_only=False,
    on_tty=False,
    conservative=False,
    styles={},
)


def show(path):
    print(path)
    print(f"exists: {path.exists()}")
    sys.exit()


this_dir = Path(__file__).parent
git_dir = this_dir.parent
markdown_dir = git_dir / "OnJava8" / "Markdown"
example_dir = Path(r"C:\Users\Bruce\OnJava8_tmp")
# show(example_dir)
combined_markdown = this_dir / "MarkdownCombined.md"

java_example = re.compile(r"\n```java.+?\n```", re.DOTALL)


@click.group()
@click.version_option()
def cli():
    """
    Manipulate On Java 8 Markdown Files
    """


@cli.command()
def combine():
    """Combine markdown files for global editing"""
    combined = ""
    for md in exists(markdown_dir).glob("*.md"):
        combined += md.read_text(errors="backslashreplace") + "\n\n"
    combined_markdown.write_text(combined)
    print(f"{combined_markdown}")
    subprocess.Popen(["code", str(combined_markdown)])


def create_numbered_markdown_filename(header1, n):
    name = header1
    if "{#" in name:
        name = header1.split("{#")[0].strip()
    if "#" in name:
        name = name.split(maxsplit=1)[1]
    replacements = [
        (": ", "_"),
        (" ", "_"),
        ("&", "and"),
        ("?", ""),
        ("+", "P"),
        ("/", ""),
        ("-", "_"),
        ("(", ""),
        (")", ""),
        ("`", ""),
        (",", ""),
        ("!", ""),
    ]
    for replacement in replacements:
        name = name.replace(*replacement)
    return "%02d_" % n + name + ".md"


def strip_chapter(chapter_text):
    """Remove blank newlines at beginning and end, right-hand spaces on lines"""
    chapter_text = chapter_text.strip()
    lines = [line.rstrip() for line in chapter_text.splitlines()]
    stripped = "\n".join(lines)
    return stripped.strip()  # In case the previous line adds another newline


def disassemble_combined_markdown_file(target_dir=markdown_dir):
    """Turn assembled markdown file into a collection of chapter-based files"""
    chapters = re.compile(r"\n(-?# .+?)\n")
    with Path(combined_markdown).open(encoding="utf8") as combined:
        book = combined.read()
    parts = chapters.split(book)
    names = parts[1::2]
    bodies = parts[0::2]
    chaps = OrderedDict()
    chaps["Front"] = bodies[0]
    for i, nm in enumerate(names):
        chaps[nm] = bodies[i + 1].strip() + "\n"
    if not target_dir.exists():
        target_dir.mkdir()
    for i, p in enumerate(chaps):
        disassembled_file_name = create_numbered_markdown_filename(p, i)
        print(f"{disassembled_file_name}")
        dest = target_dir / disassembled_file_name
        with dest.open("w", encoding="utf8") as chp:
            if p != "Front":
                chp.write(f"{p}\n\n")
            chp.write(strip_chapter(chaps[p]) + "\n")
    if target_dir != markdown_dir:
        print("now run 'diff -r Markdown test'")
    return f"Successfully disassembled {combined_markdown}"


@cli.command()
def disassemble():
    """Disassemble combined markdown file"""
    click.echo(disassemble_combined_markdown_file())


class MDTitles:
    def __init__(self, path=markdown_dir):
        self.path = path
        self.md_files = sorted(path.glob("*.md"))
        self.sluglines = [(md, md.read_text().splitlines()[0]) for md in self.md_files]
        self.titles = [
            (slug[0].name, create_numbered_markdown_filename(slug[1], n))
            for n, slug in enumerate(self.sluglines)
        ]

    def rename_atoms(self):
        for title in reversed(self.titles):
            if title[0] != title[1]:
                old = self.path / title[0]
                new = self.path / title[1]
                print(f"renaming {old.name} to {new.name}")
                old.rename(new)

    def __str__(self):
        return "\n".join([title[0] + " : " + title[1] for title in self.titles])


@cli.command()
def renumber():
    """Renumber atoms and fix atom names"""
    MDTitles().rename_atoms()


@cli.group()
def z():
    """Things you only do sometimes"""


@z.command()
def extract_code_examples():
    """Extract code examples into directory tree"""
    erase(example_dir)
    example_dir.mkdir()
    for md in exists(markdown_dir).glob("*.md"):
        print(md.name)
        text = md.read_text()
        for example in java_example.findall(text):
            example = example.strip()
            slugline = example.splitlines()[0]
            if not (slugline.startswith("//") and slugline.endswith(".scala")):
                continue
            file_path = example_dir / Path(slugline.split(maxsplit=1)[1])
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(example + "\n")


def char_range():
    return map(chr, range(ord("a"), ord("g") + 1))

def two_char_range():
    for x in char_range():
        for y in char_range():
            yield f"{x}{y}"

@z.command()
def process_markdown_through_pandoc():
    """Use Pandoc to reformat markdown"""
    click.echo("Incomplete, performs undesirable conversions")
    return
    twocr = two_char_range()
    for md in exists(markdown_dir).glob("*.md"):
        # pandoc_cmd = f"pandoc -f markdown -t markdown-fenced_code_attributes -o {md}  {md} --markdown-headings=atx --wrap=preserve --id-prefix={next(twocr)}"
        pandoc_cmd = f"pandoc -f markdown -t markdown-fenced_code_attributes -o {md}  {md} --markdown-headings=atx --wrap=preserve"
        print(f"{pandoc_cmd}")
        os.system(pandoc_cmd)
        md.write_text(md.read_text().replace("{\#", "{#"))


if __name__ == "__main__":
    cli()
