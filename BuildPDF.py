# py -3
# -*- coding: utf8 -*-
"""
Assemble individual markdown files together and produce PDF via wkhtmltopdf
"""
from pathlib import Path
import os
import sys
import shutil
import time
from betools import CmdLine
from ebook_build import ensure_ebook_build_dir, combine_markdown_files, close_viewer
import config


@CmdLine('v')
def view():
    "Open PDF file in PDF viewer"

    fn = 'BruceEckelOnJava.pdf'
    os.chdir(str(config.build_dir))
    cmd = r'start ' + fn
    if Path(fn).exists():
        os.system(cmd)
    else:
        print(fn, "not found")


def pandoc_html_command(output_name):
    return ("pandoc " + config.combined_markdown_html.name + " -t html5 -o {} " +
            " -f markdown-native_divs " +
            " --smart " +
            " --self-contained " +
            " --toc-depth=2 " +
            " --css=onjava.css ").format(output_name)


@CmdLine('t')
def convert_to_html():
    """
    Pandoc markdown to html
    """
    os.chdir(str(config.build_dir))
    cmd = pandoc_html_command("BruceEckelOnJava.html")
    print(cmd)
    os.system(cmd)


def wkhtmltopdf_command(input_name, output_name):
    return "" + \
        "wkhtmltopdf "  + \
        " --page-size Letter " + \
        " --margin-top 1.25in " + \
        " --margin-bottom 0.85in " + \
        " --margin-left 1.25in " + \
        " --margin-right 1.25in " + \
        " --header-line  " + \
        " --header-spacing 5 " + \
        " --header-left [section]  " + \
        " --header-right [subsection]  " + \
        ''' --header-font-name "Verdana Bold"  ''' + \
        " --header-font-size 10  " + \
        " --footer-line  " + \
        " --footer-spacing 5 " + \
        ''' --footer-left "Bruce Eckel"  ''' + \
        ''' --footer-center "On Java"  ''' + \
        " --footer-right [page]  " + \
        ''' --footer-font-name "Verdana Bold"  ''' + \
        " --footer-font-size 10  " + \
        " --disable-smart-shrinking  " + \
        input_name + " " + output_name

        # " --minimum-font-size 14 " + \


@CmdLine('p')
def convert_to_pdf():
    """
    HTML to PDF via wkhtmltopdf
    """
    close_viewer()
    os.chdir(str(config.build_dir))
    cmd = wkhtmltopdf_command("BruceEckelOnJava.html", "BruceEckelOnJava.pdf")
    print(cmd)
    os.system(cmd)
    view()


@CmdLine('a')
def all():
    """
    Fresh conversion from Markdown
    """
    close_viewer()
    ensure_ebook_build_dir()
    combine_markdown_files(config.combined_markdown_html)
    convert_to_html()
    os.system("start BruceEckelOnJava.html")
    # convert_to_pdf()


if __name__ == '__main__':
    CmdLine.run()

# pandoc onjava-assembled-html.md -t html5 -o BruceEckelOnJava.html  -f markdown-native_divs  --smart  --self-contained  --toc-depth=2  --css=onjava.css