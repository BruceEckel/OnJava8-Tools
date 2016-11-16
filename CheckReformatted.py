#! py -3
"""
Check results of Reformat.py to make sure nothing is lost
"""
TODO = """
"""
from pathlib import Path
import sys
import shutil
from betools import CmdLine
import config

# @CmdLine("c", num_args=1)
def checkOneFile():
    "Format a single file"
    _checkOneFile(sys.argv[2])


def _checkOneFile(arg):
    fname = Path(arg).name
    source_file = config.markdown_dir / fname
    # target = config.reformat_dir / fname
    target = config.markdown_dir / fname
    if not target.exists():
        print(str(fname) + " does not exist in " + str(config.reformat_dir))
        sys.exit(1)
    print("checking " + fname)
    original = source_file.read_text(encoding="utf-8").split()
    reformatted = target.read_text(encoding="utf8").split()
    compare(original, reformatted)


def compare(original, reformatted):
    for n, z in enumerate(zip(original, reformatted)):
        if z[0] != z[1]:
            print("n: %d" % n)
            print(z[0])
            print(z[1])
            original_context = ""
            reformatted_context = ""
            if n - 10 > 0 and n + 10 < len(original):
                for i in range(n - 10, n + 10):
                    original_context += original[i] + " "
                    reformatted_context += reformatted[i] + " "
            print("[original_context]\n" + original_context)
            print("[reformatted_context]\n" + reformatted_context)
            break
    if len(original) != len(reformatted):
        print("len(original): %d" % len(original))
        print("len(reformatted): %d" % len(reformatted))
        # sys.exit(1)


# @CmdLine("a")
def check_all():
    print("Checking all markdown files ...")
    for sourceText in config.markdown_dir.glob("*.md"):
        _checkOneFile(sourceText)


if __name__ == '__main__':
    CmdLine.run()
