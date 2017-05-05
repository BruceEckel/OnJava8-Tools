# py -3
"""
Tools for checking and fixing line widths within combined markdown file
"""
# from pathlib import Path
import os
import config
from pathlib import Path
import textwrap
from betools import CmdLine

assert config.build_dir.exists()
assert config.combined_markdown.exists(), "RUN b -s first"


@CmdLine("o")
def show_generated_output_too_wide():
    "Show all lines that exceed config.code_width in the gradlw-run .out files"
    for outfile in config.example_dir.rglob("*.out"):
        for n, line in enumerate(outfile.read_text(encoding="utf-8").splitlines()):
            if len(line) > config.code_width:
                print("{}({}) [{}]: {}".format(outfile.name, n, len(line), line))


@CmdLine("a")
def show_all_too_wide():
    "Show all lines that exceed config.code_width"
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
    "Open Sublime at first instance that exceeds config.code_width"
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
        result += textwrap.fill(line, width=config.code_width) + "\n"
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
    "Produce .p1 files that are formatted output"
    out_files = list(Path(".").rglob("*.out"))
    if len(out_files) < 10:
        print("Error: found less than 10 .out files")
        sys.exit(1)
    for outfile in out_files:
        out_text = adjust_lines(outfile.read_text())
        phase_1 = outfile.with_suffix(".p1")
        with phase_1.open('w') as phs1:
            phs1.write(fill_to_width(out_text) + "\n")
            errfile = outfile.with_suffix(".err")
            if errfile.exists():
                phs1.write("___[ Error Output ]___\n")
                phs1.write(fill_to_width(errfile.read_text()) + "\n")
            phs1.write("*/\n")


if __name__ == '__main__':
    CmdLine.run()
