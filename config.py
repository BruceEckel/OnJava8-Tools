"""
Common program configuration variables for "On Java" tools
"""
from pathlib import Path
import sys

code_width = 58

tools_dir = Path(sys.path[0])
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
