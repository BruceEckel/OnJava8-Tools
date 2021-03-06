#! py -3
"""
Reformat Markdown files to preserve non-space following dashes.
"""
TODO = """
"""
from pathlib import Path
import sys
import shutil
from betools import CmdLine
import config
from reformat_markdown import ReformatMarkdownDocument
from CheckReformatted import compare

WIDTH = 80

# @CmdLine("c")
def clean():
    "Remove 'Reformatted' directory"
    print("Cleaning ...")
    try:
        if config.reformat_dir.exists():
            shutil.rmtree(str(config.reformat_dir))
    except:
        print("Old path removal failed")
        sys.exit(1)


# @CmdLine("d")
def create_reformatted_directory():
    "Create 'Reformatted' directory"
    if not config.reformat_dir.exists():
        print("creating {}".format(config.reformat_dir))
        config.reformat_dir.mkdir()


@CmdLine("f", num_args=1)
def formatOneFile():
    "Format a single file"
    _formatOneFile(sys.argv[2])


def _formatOneFile(arg):
    # create_reformatted_directory()
    fname = Path(arg).name
    source_file = config.markdown_dir / fname
    if not source_file.exists():
        print(str(fname) + " does not exist in " + str(config.markdown_dir))
        sys.exit(1)
    print("formatting " + fname)
    #shutil.copy(str(source_file), str(config.reformat_dir))
    #original = config.reformat_dir / fname
    #assert original.exists()
    markdown = source_file.read_text(encoding="utf-8")
    # target = config.reformat_dir / fname # (Path(arg).stem + "-reformatted.md")
    target = config.markdown_dir / fname
    reformatted = ReformatMarkdownDocument(fname, markdown, WIDTH).reformat()
    target.write_text(reformatted + "\n", encoding="utf8")
    print("Checking result")
    compare(markdown, reformatted)


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
