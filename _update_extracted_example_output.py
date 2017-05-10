#! py -3
# Requires Python 3.5
# Updates generated output into extracted Java programs in "On Java 8"
# Also provides tools to reformat the .out files produced by 'gradlew run'
# NOTE: Incorporated output comes from .p1 files, not from .out files
import os
import sys
import textwrap
from pathlib import Path

from betools import CmdLine

import config

assert config.build_dir.exists()
if not config.combined_markdown.exists():
    print("Error: cannot find {}".format(config.combined_markdown))
    print("RUN b -s first")
    sys.exit(1)


def check_for_existence(extension):
    files_with_extension = list(Path(".").rglob(extension))
    if len(files_with_extension) < 1:
        print("Error: no " + extension + " files found")
        sys.exit(1)
    return files_with_extension


def checkwidth(extension):
    check_for_existence(extension)
    for outfile in config.example_dir.rglob(extension):
        for n, line in enumerate(outfile.read_text(encoding="utf-8").splitlines()):
            if len(line) > config.code_width:
                print("{}({}) [{}]: {}".format(
                    outfile.name, n, len(line), line))


@CmdLine("o")
def show_generated_output_too_wide():
    "Show all lines that exceed config.code_width in the gradlw-run .out files"
    checkwidth("*.out")


@CmdLine("p")
def show_formatted_output_too_wide():
    "Show all lines that exceed config.code_width in the .p1 files"
    checkwidth("*.p1")


@CmdLine("m")
def show_all_too_wide():
    "Show all lines in combined_markdown that exceed config.code_width"
    in_listing = False
    for n, line in enumerate(config.combined_markdown.read_text(encoding="utf-8").splitlines()):
        if line.startswith("```java"):
            in_listing = True
            continue
        if line.startswith("```"):
            in_listing = False
            continue
        if in_listing and len(line) > config.code_width:
            print("{}: {}".format(n, line))


@CmdLine("e")
def check_listing_widths():
    "Open Sublime at first instance of combined_markdown that exceeds config.code_width"
    in_listing = False
    for n, line in enumerate(config.combined_markdown.read_text(encoding="utf-8").splitlines()):
        if line.startswith("```java"):
            in_listing = True
            continue
        if line.startswith("```"):
            in_listing = False
            continue
        if in_listing and len(line) > config.code_width:
            print("{}: {}".format(n, line))
            os.system("subl {}:{}".format(config.combined_markdown, n + 1))
            return


# Format output:
# (0) Do first/last lines before formatting to width
# (1) Combine output and error (if present) files
# (2) Format all output to width limit
# (3) Add closing '*/'

def fill_to_width(text):
    result = ""
    for line in text.splitlines():
        result += textwrap.fill(line, width=config.code_width - 1) + "\n"
    return result.strip()


def adjust_lines(text):
    text = text.replace("\0", "NUL")
    lines = text.splitlines()
    slug = lines[0]
    if "(First and Last " in slug:
        num_of_lines = int(slug.split()[5])
        adjusted = lines[:num_of_lines + 1] +\
            ["...________...________...________...________..."] +\
            lines[-num_of_lines:]
        return "\n".join(adjusted)
    elif "(First " in slug:
        num_of_lines = int(slug.split()[3])
        adjusted = lines[:num_of_lines + 1] +\
            ["                  ..."]
        return "\n".join(adjusted)
    else:
        return text


@CmdLine("f")
def reformat_runoutput_files():
    "Produce formatted .p1 files from the .out files produced by gradlew run"
    for outfile in check_for_existence("*.out"):
        java = outfile.with_suffix(".java")
        if java.exists():
            if "{VisuallyInspectOutput}" in java.read_text():  # Don't create p1 file
                print("{} Excluded".format(java.name))
                continue
        out_text = adjust_lines(outfile.read_text())
        phase_1 = outfile.with_suffix(".p1")
        with phase_1.open('w') as phs1:
            phs1.write(fill_to_width(out_text) + "\n")
            errfile = outfile.with_suffix(".err")
            if errfile.exists():
                phs1.write("___[ Error Output ]___\n")
                phs1.write(fill_to_width(errfile.read_text()) + "\n")
            phs1.write("*/\n")


def remove_output(javatext):
    result = ""
    for line in javatext.splitlines():
        if "/* Output:" not in line:
            result += line.rstrip() + "\n"
        else:
            return result


def update_file(outfile):
    print(str(outfile))
    javafile = outfile.with_suffix(".java")
    if not javafile.exists():
        print(str(outfile) + " has no javafile")
        sys.exit(1)
    javatext = javafile.read_text()
    if "/* Output:" not in javatext:
        print(str(javafile) + " has no /* Output:")
        sys.exit(1)
    new_output = outfile.read_text()
    new_javatext = remove_output(javatext) + new_output
    javafile.write_text(new_javatext)


@CmdLine("j")
def update_output_in_java_files():
    "Insert formatted .p1 files into their associated .java files"
    # if len(sys.argv) > 1:
    #     update_file(Path(sys.argv[1]))
    # else:
    # Note p1 files have been line-wrapped
    for outfile in check_for_existence("*.p1"):
        print(outfile)
        update_file(outfile)


"""
Final Step: Insert the examples back into combined_markdown
"""


def insert_code_in_book(code):
    codelines = code.splitlines()
    header = codelines[0]
    book = config.combined_markdown.read_text(encoding="utf8").splitlines()
    in_code = False
    for i, line in enumerate(book):
        if header in line:
            print("Replacing {}".format(header[3:]))
            start = i
            in_code = True
        if "```" in line and in_code:
            end = i
            break
    else:
        print("Couldn't find {}".format(header[3:]))
        sys.exit(1)
    book[start:end] = codelines
    config.combined_markdown.write_text(
        ("\n".join(book)).strip(), encoding="utf8")


def insert_new_version_of_example(javafilepath):
    if not javafilepath.exists():
        print("Error: cannot find {}".format(javafilepath))
        sys.exit(1)
    insert_code_in_book(javafilepath.read_text())


@CmdLine("i")
def insert_examples_into_combined_markdown():
    """
    Take all (presumably updated) java files and insert them
    back into the combined_markdown file.
    """
    # if len(sys.argv) > 1:
    #     insert_new_version_of_example(Path(sys.argv[1]))
    # else:
    for new_version in config.example_dir.rglob("*.java"):
        insert_new_version_of_example(new_version)


@CmdLine("a")
def fix_up_and_include_all_new_output():
    """
    Performs all tasks to take new output from 'gradlew run' to
    incorporation into combined_markdown file
    """
    reformat_runoutput_files()
    update_output_in_java_files()
    insert_examples_into_combined_markdown()


if __name__ == '__main__':
    CmdLine.run()
