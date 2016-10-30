#! py -3
"""
Reformat Markdown files to preserve non-space following dashes.
"""
TODO = """
"""
import logging
from logging import debug
# logging.basicConfig(filename= __file__.split('.')[0] + ".log", level=logging.DEBUG)
from pathlib import Path
import sys
import shutil
from betools import CmdLine
import config
from reformat_markdown import ReformatMarkdownDocument

@CmdLine("c")
def clean():
    "Remove 'Reformatted' directory"
    print("Cleaning ...")
    try:
        if config.reformat_dir.exists():
            shutil.rmtree(str(config.reformat_dir))
    except:
        print("Old path removal failed")
        raise RuntimeError()


@CmdLine("m")
def make_reformatted_directory():
    "Create 'Reformatted' directory"
    if not config.reformat_dir.exists():
        print("Creating 'Reformatted' directory")
        debug("creating {}".format(config.reformat_dir))
        config.reformat_dir.mkdir()


@CmdLine("f", num_args=1)
def formatOneFile():
    "Format a single file"
    _formatOneFile(sys.argv[2])


def _formatOneFile(arg):
    make_reformatted_directory()
    fname = Path(arg).name
    source_file = config.markdown_dir / fname
    if not source_file.exists():
        print(str(fname) + " does not exist in " + str(config.markdown_dir))
        sys.exit()
    print("formatting " + fname)
    shutil.copy(str(source_file), str(config.reformat_dir))
    original = config.reformat_dir / fname
    assert original.exists()
    markdown = original.read_text(encoding="utf-8")
    target = config.reformat_dir / (Path(arg).stem + ".rf")
    reformatted = ReformatMarkdownDocument(markdown).reformat()
    target.write_text(reformatted, encoding="utf8")


@CmdLine("a")
def reformat_all():
    print("Reformatting all markdown files ...")
    for sourceText in config.markdown_dir.glob("*.md"):
        _formatOneFile(sourceText)

    # slugline = re.compile("^(//|#) .+?\.[a-z]+$", re.MULTILINE)
    # xmlslug  = re.compile("^<!-- .+?\.[a-z]+ +-->$", re.MULTILINE)
    # for group in re.findall("```(.*?)\n(.*?)\n```", text, re.DOTALL):


if __name__ == '__main__':
    CmdLine.run()
