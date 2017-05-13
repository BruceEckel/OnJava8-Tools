"""
Common program configuration variables for "On Java" tools
"""
import os
import sys
from pathlib import Path
import textwrap

base_name = "BruceEckelOnJava8"
epub_file_name = base_name + ".epub"
epub_sample_file_name = base_name + "Sample.epub"

code_width = 56

try:
    tools_dir = Path(os.environ['ONJAVA_TOOLS'])
except:
    print("Error: need to set ONJAVA_TOOLS")
    sys.exit(1)

rootPath = tools_dir.parent / "on-java"

markdown_dir = rootPath / "Markdown"

example_dir = rootPath / "ExtractedExamples"

github_code_dir = rootPath.parent / "OnJava8-Examples"

build_dir = rootPath / "ebook_build"
html_dir = build_dir / "html"
build_dir_images = build_dir / "images"
epub_dir = build_dir / "epub_files"
combined_markdown = build_dir / "onjava-assembled.md"
combined_markdown_html = build_dir / "onjava-assembled-html.md"
combined_markdown_pdf = build_dir / "onjava-assembled-pdf.md"
stripped_for_style = build_dir / "onjava-stripped-for-style.md"
stripped_for_spelling = build_dir / "onjava-stripped-for-spelling.md"

ebookResources = rootPath / "resources"
img_dir = ebookResources / "images"
fonts = ebookResources / "fonts"
cover = ebookResources / "cover.jpg"
css = ebookResources / "onjava.css"
metadata = ebookResources / "metadata.yaml"

reformat_dir = rootPath / "Reformatted"

sample_book_dir = rootPath / "SampleBook"
sample_book_original_dir = rootPath / "SampleBook" / "Original"
combined_markdown_sample = sample_book_dir / "onjava-assembled.md"


def check_for_existence(extension):
    files_with_extension = list(example_dir.rglob(extension))
    if len(files_with_extension) < 1:
        print("Error: no " + extension + " files found")
        sys.exit(1)
    return files_with_extension


# Format output:
# (0) Do first/last lines before formatting to width
# (1) Combine output and error (if present) files
# (2) Format all output to width limit
# (3) Add closing '*/'


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


def fill_to_width(text):
    result = ""
    for line in text.splitlines():
        result += textwrap.fill(line, width=code_width - 1) + "\n"
    return result.strip()


def reformat_runoutput_files():
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
