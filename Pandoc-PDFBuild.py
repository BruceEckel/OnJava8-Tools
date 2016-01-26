# py -3
"""
Produce PDF
"""
from pathlib import Path
import os
import sys
import re
import shutil
from betools import CmdLine
from ebook_build import ensure_ebook_build_dir, combine_markdown_files, close_viewer
import config


@CmdLine('v')
def view():
    "Open PDF file in PDF viewer"
    os.chdir(str(config.build_dir))
    cmd = r'start BruceEckelOnJava.pdf'
    print(cmd)
    os.system(cmd)


@CmdLine('p')
def convert_to_pdf():
    """
    Convert Markdown to pdf
    """
    close_viewer()
    ensure_ebook_build_dir()
    os.chdir(str(config.build_dir))
    combine_markdown_files(config.combined_markdown_pdf)

    pandoc = "pandoc " + config.combined_markdown_pdf.name + " -o BruceEckelOnJava.pdf " + \
        " --template=onjava.tex " + \
        " --latex-engine=xelatex " + \
        ' -V geometry:"top=1.25in, bottom=0.85in, left=1.25in, right=1.25in" ' + \
        ""
    print(pandoc)
    os.system(pandoc)
    view()

    # " -V fontfamily=Fyra " + \
    # ' -V geometry:"margin=2in, paperheight=8.5in" ' + \
    # " --output=pdf_document(fig_caption=false) " + \
    # ' --title="On Java: Collected Writings" ' + \
    # " --variable mainfont=Georgia " + \
    # " --variable sansfont=Verdana " + \
    # ' --variable monofont="Ubuntu Mono" ' + \
    # " --variable fontsize=12pt " + \
    # " --toc " + \
    # ' -V geometry:"margin=1in" ' + \
    # ' -V geometry:"top=1in, bottom=1in" ' + \


if __name__ == '__main__':
    CmdLine.run()
