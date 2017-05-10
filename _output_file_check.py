# Check the .out files resulting from 'gradlew run'
import pprint
from pathlib import Path

from betools import CmdLine

import config


@CmdLine("e")
def match_error_output_with_tags():
    """
    Find ___[ Error Output ]___ without {ThrowsException} 
    or {ErrorOutputExpected}, and vice-versa
    """
    tag_names = "{ThrowsException} or {ErrorOutputExpected}"
    for java in config.example_dir.rglob("*.java"):
        code = java.read_text()
        short_path = java.relative_to(config.example_dir)
        if "___[ Error Output ]___" in code:
            if not ("{ThrowsException}" in code or "{ErrorOutputExpected}" in code):
                print("{}:\n\t[Error Output] without {}\n".format(
                    short_path, tag_names))
        if "{ThrowsException}" in code or "{ErrorOutputExpected}" in code:
            if not "___[ Error Output ]___" in code:
                print("{}:\n\t{} without [Error Output]\n".format(
                    short_path, tag_names))


@CmdLine("o")
def show_comment_output_tag_lines():
    "Show /* Output: (*) in gradlw-run .out files"
    output_lines = set()
    base = "/* Output:"
    for md in config.example_dir.rglob("*.out"):
        output_ln = md.read_text().splitlines()[0]
        output_lines.add(output_ln)
        if(not output_ln.startswith(base)):
            print(str(md.relative_to(config.example_dir)))
        if output_ln.strip() != base:
            print(str(md.relative_to(config.example_dir)))
            print(output_ln)
    pprint.pprint(output_lines)


if __name__ == '__main__':
    CmdLine.run()
