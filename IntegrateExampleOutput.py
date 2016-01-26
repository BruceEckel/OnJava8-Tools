#! py -3
"""
Replace existing output with newly-generated output and
replace example file in document.
"""
from pathlib import Path
import os
import sys
from betools import CmdLine
from java_main import JavaMain

rootPath = Path(sys.path[0]).parent / "on-java"
examplePath = rootPath / "ExtractedExamples"
markdown_dir = rootPath / "Markdown"


def __replaceOutput(jfp):
    """Replace existing output with new output"""
    javafilepath = Path(jfp)
    if not javafilepath.exists():
        print("Error: cannot find {}".format(javafilepath))
        sys.exit(1)
    j_main = JavaMain.create(javafilepath)
    if j_main:
        j_main.write_modified_file()
        print(j_main.new_code())


@CmdLine("r", num_args="+")
def replaceOutput():
    """Replace existing output with new output"""
    for jfp in sys.argv[2:]:
        __replaceOutput(jfp)
        # javafilepath = Path(jfp)
        # if not javafilepath.exists():
        #     print("Error: cannot find {}".format(javafilepath))
        #     sys.exit(1)
        # j_main = JavaMain.create(javafilepath)
        # if j_main:
        #     j_main.write_modified_file()
        #     print(j_main.new_code())


def insert_code_in_chapter(code, chapter):
    chapter = chapter.splitlines()
    header = code.splitlines()[0]
    in_code = False
    for i, line in enumerate(chapter):
        if header in line:
            start = i
            in_code = True
        if "```" in line and in_code:
            end = i
            break
    print("start: [{}]  {}".format(start, chapter[start]))
    print("end: [{}]  {}".format(end - 1, chapter[end - 1]))
    for n in range(start, end):
        print(chapter[n])
    chapter[start:end] = code.splitlines()
    for line in chapter[start - 10: end + 10]:
        try:
            print(line)
        except:
            print(line.encode("utf8"))
    return ("\n".join(chapter)).strip()


def __insert_updated_example(jfp):
    """Put example into its markdown file"""
    javafilepath = Path(jfp)
    if not javafilepath.exists():
        print("Error: cannot find {}".format(javafilepath))
        sys.exit(1)
    with javafilepath.open() as java_file:
        code = java_file.read()
    header = code.splitlines()[0]
    for md in markdown_dir.glob("[0-9][0-9]_*.md"):
        with md.open(encoding="utf8") as chapter:
            text = chapter.read()
        for line in text.splitlines():
            if header in line:
                print("{} found in {}".format(header[3:], md.name))
                text = insert_code_in_chapter(code, text)
                with md.open("w", encoding="utf8") as update:
                    update.write(text + "\n")
                os.system("subl {}".format(md))
                return


@CmdLine("p", num_args="+")
def insert_updated_example():
    """Put example into its markdown file"""
    for jfp in sys.argv[2:]:
        __insert_updated_example(jfp)
        # javafilepath = Path(jfp)
        # if not javafilepath.exists():
        #     print("Error: cannot find {}".format(javafilepath))
        #     sys.exit(1)
        # with javafilepath.open() as java_file:
        #     code = java_file.read()
        # header = code.splitlines()[0]
        # for md in markdown_dir.glob("[0-9][0-9]_*.md"):
        #     with md.open(encoding="utf8") as chapter:
        #         text = chapter.read()
        #     for line in text.splitlines():
        #         if header in line:
        #             print("{} found in {}".format(header[3:], md.name))
        #             text = insert_code_in_chapter(code, text)
        #             with md.open("w", encoding="utf8") as update:
        #                 update.write(text + "\n")
        #             os.system("subl {}".format(md))
        #             return


@CmdLine("u", num_args="+")
def update_and_integrate_example_output():
    """Update example with new output, then replace new example into its markdown file"""
    for jfp in sys.argv[2:]:
        __replaceOutput(jfp)
        __insert_updated_example(jfp)


if __name__ == '__main__':
    CmdLine.run()
