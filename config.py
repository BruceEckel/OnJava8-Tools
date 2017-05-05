"""
Common program configuration variables for "On Java" tools
"""
import os
import sys
from pathlib import Path

base_name = "BruceEckelOnJava8"
epub_file_name = base_name + ".epub"
epub_sample_file_name = base_name + "Sample.epub"

code_width = 58

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
