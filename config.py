"""
Common program configuration variables for "On Java" tools
"""
from pathlib import Path
import sys

code_width = 60

tools_dir = Path(sys.path[0])
rootPath = tools_dir.parent

markdown_dir = rootPath / "Markdown"
build_dir = rootPath / "ebook_build"
epub_dir = build_dir / "epub_files"
github_code_dir = rootPath.parent / "OnJava-Examples"
example_dir = rootPath / "ExtractedExamples"
img_dir = markdown_dir / "images"
ebookResources = rootPath / "resources"
html_dir = build_dir / "html"
build_dir_images = build_dir / "images"

combined_markdown = build_dir / "onjava-assembled.md"
combined_markdown_html = build_dir / "onjava-assembled-html.md"
combined_markdown_pdf = build_dir / "onjava-assembled-pdf.md"

fonts = ebookResources / "fonts"
cover = ebookResources / "cover.jpg"
css = ebookResources / "onjava.css"
metadata = ebookResources / "metadata.yaml"
