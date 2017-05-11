# Check the .out files resulting from 'gradlew run'
import pprint
import os
from pathlib import Path

from betools import CmdLine

import config

untagged = "[Error Output] without {ThrowsException} or {ErrorOutputExpected}"
no_error = "{ThrowsException} or {ErrorOutputExpected} Without [Error Output]"

def discover_unmatched_errors_and_tags():
    result = []
    for java in config.example_dir.rglob("*.java"):
        code = java.read_text()
        if "___[ Error Output ]___" in code:
            if not ("{ThrowsException}" in code or "{ErrorOutputExpected}" in code):
                result.append((untagged, java))
        if "{ThrowsException}" in code or "{ErrorOutputExpected}" in code:
            if not "___[ Error Output ]___" in code:
                result.append((no_error, java))
    return result


@CmdLine("m")
def match_error_output_with_tags():
    """
    Find ___[ Error Output ]___ without {ThrowsException}
    or {ErrorOutputExpected}, and vice-versa
    """
    tag_names = "{ThrowsException} or {ErrorOutputExpected}"
    for err, java in discover_unmatched_errors_and_tags():
        print("{}:\n\t{}\n".format(java.relative_to(config.example_dir), err))


@CmdLine("e")
def edit_unmatched_error_output():
    """
    Find ___[ Error Output ]___ without {ThrowsException}
    or {ErrorOutputExpected}, and vice-versa
    """
    tag_names = "{ThrowsException} or {ErrorOutputExpected}"
    for err, java in discover_unmatched_errors_and_tags():
        os.system("subl {}".format(java))


@CmdLine("d")
def discover_unincluded_output():
    """
    Discover .out files and/or .err files that are not included
    in their respective .java files
    """
    def discover(extension, pattern):
        outfiles = config.check_for_existence("*" + extension)
        for outfile in outfiles:
            java = outfile.with_suffix(".java")
            java_rel = java.relative_to(config.example_dir)
            outfile_rel = outfile.relative_to(config.example_dir)
            print(".", end="")
            if not java.exists():
                print("\nNo {} for {}".format(java_rel, outfile_rel))
                continue
            if pattern not in java.read_text():
                print("\nNo /* Output: {} for {}".format(java_rel, outfile_rel))
        print("{} {} files".format(len(outfiles), extension))

    discover(".out", "/* Output:")
    discover(".err", "___[ Error Output ]___")

    def discover2(pattern, extension):
        java_files = list(config.example_dir.rglob("*.java"))
        for java in java_files:
            java_rel = java.relative_to(config.example_dir)
            outfile = java.with_suffix(extension)
            outfile_rel = outfile.relative_to(config.example_dir)
            if pattern in java.read_text():
                if not outfile.exists():
                    print("\nNo {} for {}".format(outfile_rel, java_rel))
                    continue

    discover2("/* Output:", ".out")
    discover2("___[ Error Output ]___", ".err")




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
