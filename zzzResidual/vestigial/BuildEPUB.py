# py -3
# -*- coding: utf8 -*-
"""
Assemble individual markdown files together and produce epub book.
"""
from pathlib import Path
import os
import sys
import shutil
from betools import CmdLine
from ebook_build import *
import config


@CmdLine('c')
def clean_new_build_dir():
    """
    Delete and create basic book build directory
    """
    close_viewer()
    recreate_build_dir()

@CmdLine('s')
def edit_combined_files():
    """
    Put markdown files together and open result in editor
    """
    combine_markdown_files(config.combined_markdown)
    os.system("subl {}".format(config.combined_markdown))


def pandoc_epub_command(output_name):
    return (
        "pandoc onjava-assembled.md -t epub3 -o " + output_name +
        " -f markdown-native_divs "
        " --smart "
        " --epub-cover-image=cover.jpg "
        " --epub-embed-font=chapter.png "
        " --epub-embed-font=subhead.png "
        " --epub-embed-font=level-2.png "
        " --epub-embed-font=UbuntuMono-R.ttf "
        " --epub-embed-font=UbuntuMono-RI.ttf "
        " --epub-embed-font=UbuntuMono-B.ttf "
        " --epub-embed-font=UbuntuMono-BI.ttf "
        " --epub-embed-font=georgia.ttf "
        " --epub-embed-font=georgiab.ttf "
        " --epub-embed-font=georgiai.ttf "
        " --epub-embed-font=georgiaz.ttf "
        " --epub-embed-font=verdana.ttf "
        " --epub-embed-font=verdanab.ttf "
        " --epub-embed-font=verdanai.ttf "
        " --epub-embed-font=verdanaz.ttf "
        " --epub-embed-font=YuGothicUI-Semibold.ttf "
        " --toc-depth=2 "
        " --epub-stylesheet=onjava.css ")


def convert_to_epub():
    """
    Pandoc markdown to epub
    """
    os.chdir(str(config.build_dir))
    cmd = pandoc_epub_command("BruceEckelOnJava.epub")
    print(cmd)
    os.system(cmd)
    os.system("start BruceEckelOnJava.epub")
    os.system(r'copy /Y BruceEckelOnJava.epub "C:\Users\Bruce\Google Drive\ebooks"')
    os.system(r'copy /Y BruceEckelOnJava.epub "C:\Users\Bruce\Dropbox\__Ebooks"')


def copy_and_unzip_epub():
    """
    Create unpacked epub
    """
    shutil.copy("BruceEckelOnJava.epub", "BruceEckelOnJava.zip")
    os.system("unzip BruceEckelOnJava.zip -d epub_files")


def convert_to_epub_for_e_ink():
    """
    Pandoc markdown to black & white epub
    """
    os.chdir(str(config.build_dir))
    cmd = pandoc_epub_command("BruceEckelOnJava-E-INK.epub") + " --no-highlight "
    print(cmd)
    os.system(cmd)


def convert_to_e_ink_mobi():
    """
    epub to e-ink kindle (mobi)
    """
    os.chdir(str(config.build_dir))
    cmd = "kindlegen BruceEckelOnJava-E-INK.epub"
    print(cmd)
    os.system(cmd)


def convert_to_color_mobi():
    """
    epub to color kindle (mobi)
    """
    os.chdir(str(config.build_dir))
    cmd = "kindlegen BruceEckelOnJava.epub"
    print(cmd)
    os.system(cmd)


@CmdLine('e')
def create_fresh_epub():
    """
    Fresh conversion from Markdown
    """
    close_viewer()
    ensure_ebook_build_dir()
    combine_markdown_files(config.combined_markdown)
    convert_to_epub()
    copy_and_unzip_epub()


@CmdLine('a')
def all():
    """
    Create fresh epub, epub for E-ink, and mobi for e-ink
    """
    close_viewer()
    ensure_ebook_build_dir()
    combine_markdown_files(config.combined_markdown)
    convert_to_epub()
    copy_and_unzip_epub()
    convert_to_epub_for_e_ink()
    convert_to_e_ink_mobi()
    convert_to_color_mobi()


if __name__ == '__main__':
    CmdLine.run()
