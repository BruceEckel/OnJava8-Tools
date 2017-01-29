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
    recreate_build_dir(config.build_dir)

@CmdLine('s')
def edit_combined_files():
    """
    Put markdown files together and open result in editor
    """
    combine_markdown_files(config.markdown_dir, config.combined_markdown)
    os.system("subl {}".format(config.combined_markdown))


def copy_and_unzip_epub():
    """
    Create unpacked epub
    """
    shutil.copy(config.epub_file_name, config.base_name + ".zip")
    os.system("unzip " + config.base_name + ".zip -d epub_files")


def convert_to_epub_for_e_ink():
    """
    Pandoc markdown to black & white epub
    """
    os.chdir(str(config.build_dir))
    cmd = pandoc_epub_command(config.base_name + "-E-INK.epub") + " --no-highlight "
    print(cmd)
    os.system(cmd)


def convert_to_e_ink_mobi():
    """
    epub to e-ink kindle (mobi)
    """
    os.chdir(str(config.build_dir))
    cmd = "kindlegen " + config.base_name + "-E-INK.epub"
    print(cmd)
    os.system(cmd)


def convert_to_color_mobi():
    """
    epub to color kindle (mobi)
    """
    os.chdir(str(config.build_dir))
    cmd = "kindlegen " + config.epub_file_name
    print(cmd)
    os.system(cmd)


@CmdLine('e')
def create_fresh_epub():
    """
    Fresh conversion from Markdown
    """
    close_viewer()
    ensure_ebook_build_dir(config.build_dir)
    combine_markdown_files(config.markdown_dir, config.combined_markdown)
    convert_to_epub(config.build_dir, config.epub_file_name)
    # copy_and_unzip_epub()


@CmdLine('a')
def all():
    """
    Create fresh epub, epub for E-ink, and mobi for e-ink
    """
    close_viewer()
    ensure_ebook_build_dir(config.build_dir)
    combine_markdown_files(config.markdown_dir, config.combined_markdown)
    convert_to_epub(config.build_dir, config.epub_file_name)
    copy_and_unzip_epub()
    convert_to_epub_for_e_ink()
    convert_to_e_ink_mobi()
    convert_to_color_mobi()


if __name__ == '__main__':
    CmdLine.run()
