"""
Common program configuration variables for "On Java" tools
"""
from pathlib import Path
import sys

code_width = 60

tools_dir = Path(sys.path[0])
rootPath = tools_dir.parent / "on-java"

markdown_dir = rootPath / "Markdown"
img_dir = markdown_dir / "images"

example_dir = rootPath / "ExtractedExamples"

github_code_dir = rootPath.parent / "OnJava-Examples"

build_dir = rootPath / "ebook_build"
html_dir = build_dir / "html"
build_dir_images = build_dir / "images"
epub_dir = build_dir / "epub_files"
combined_markdown = build_dir / "onjava-assembled.md"
combined_markdown_html = build_dir / "onjava-assembled-html.md"
combined_markdown_pdf = build_dir / "onjava-assembled-pdf.md"

ebookResources = rootPath / "resources"
fonts = ebookResources / "fonts"
cover = ebookResources / "cover.jpg"
css = ebookResources / "onjava.css"
metadata = ebookResources / "metadata.yaml"

reformat_dir = rootPath / "Reformatted"
