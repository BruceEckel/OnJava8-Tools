#! py -3
# Requires Python 3.5
# Updates generated output into extracted Java programs in "On Java 8"
# Also provides tools to reformat the .out files produced by 'gradlew run'
# NOTE: Incorporated output comes from .p1 files, not from .out files
import os
import sys
from pathlib import Path
import click
import config


@click.group()
@click.version_option()
def cli():
    """
    Updates generated output into Java programs in "On Java 8"
    """


def update_java_file(p1_file):
    def remove_output(javatext):
        result = ""
        for line in javatext.splitlines():
            if "/* Output:" not in line:
                result += line.rstrip() + "\n"
            else:
                return result  # Result doesn't include /* Ouput: or subsequent lines

    base_dir = p1_file.parent.parent
    javafile = p1_file.with_suffix(".java")
    print(f"{p1_file.parent.relative_to(base_dir)}: {p1_file.name} -> {javafile.name}")
    if not javafile.exists():
        print(str(p1_file) + " has no javafile")
        sys.exit(1)
    javatext = javafile.read_text()
    if "/* Output:" not in javatext:
        print(str(javafile) + " has no /* Output:")
        sys.exit(1)
    new_output = p1_file.read_text()
    new_javatext = remove_output(javatext) + new_output
    javafile.write_text(new_javatext)


def update_output_in_java_files():
    """
    Produce formatted .p1 files from the .out files produced by gradlew run
    Insert formatted .p1 files into their associated .java files
    """
    config.reformat_runoutput_files()
    for p1_file in config.require_existence("*.p1"):
        update_java_file(p1_file)


@cli.command()
def update_example_output():
    "(For testing)"
    update_output_in_java_files()


def insert_example_in_book(javafilepath):
    if not javafilepath.exists():
        print(f"Error: cannot find {javafilepath}")
        sys.exit(1)
    example = javafilepath.read_text()
    if "/* Output:" not in example:
        return # Doesn't need replacing
    codelines = example.splitlines()
    header = codelines[0]
    def find_chapter_with_example():
        nonlocal header
        for chapter_path in config.markdown_dir.glob("*.md"):
            chapter = chapter_path.read_text(encoding="utf8")
            if header in chapter:
                return (chapter_path, chapter)
        print(f"Error: cannot locate file containing {header}")
        sys.exit(1)
    chapter_path, chapter = find_chapter_with_example()
    print(f"{header} in {chapter_path.name}")
    chapter_lines = chapter.splitlines()
    start = chapter_lines.index(header)
    end = chapter_lines.index("```", start)
    print(f"{start}: {header}, {end}: '```'")
    # chapter_lines[start:end] = codelines
    # chapter_path.write_text(("\n".join(chapter)).strip(), encoding="utf8")


@cli.command()
def format_and_include_new_output():
    """
    Format new output from 'gradlew run' to Java files, then
    incorporate new Java files into book
    """
    update_output_in_java_files()
    for new_version in config.example_dir.rglob("*.java"):
        insert_example_in_book(new_version)


if __name__ == "__main__":
    cli()
