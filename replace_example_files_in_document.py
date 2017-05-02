#! py -3
"""
Replace example files in onjava-assembled.md
"""
import sys
from pathlib import Path
import config


def insert_code_in_book(code):
    codelines = code.splitlines()
    header = codelines[0]
    book = config.combined_markdown.read_text(encoding="utf8").splitlines()
    in_code = False
    for i, line in enumerate(book):
        if header in line:
            print("Replacing {}".format(header[3:]))
            start = i
            in_code = True
        if "```" in line and in_code:
            end = i
            break
    else:
        print("Couldn't find {}".format(header[3:]))
        sys.exit(1)
    book[start:end] = codelines
    config.combined_markdown.write_text(
        ("\n".join(book)).strip(), encoding="utf8")


def insert_new_version_of_example(javafilepath):
    if not config.combined_markdown.exists():
        print("Error: cannot find {}".format(config.combined_markdown))
        sys.exit(1)
    if not javafilepath.exists():
        print("Error: cannot find {}".format(javafilepath))
        sys.exit(1)
    insert_code_in_book(javafilepath.read_text())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        insert_new_version_of_example(Path(sys.argv[1]))
    else:
        for new_version in config.example_dir.rglob("*.java"):
            insert_new_version_of_example(new_version)
