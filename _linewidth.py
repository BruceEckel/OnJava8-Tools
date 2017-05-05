# py -3
"""
Tools for checking and fixing line widths within combined markdown file
"""
# from pathlib import Path
import os
import config
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


if __name__ == '__main__':
    CmdLine.run()
