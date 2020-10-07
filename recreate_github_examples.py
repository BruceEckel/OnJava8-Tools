#! Py -3
"Tools for updating Github example-code repository"
from pathlib import Path
import sys
import os
import shutil
import click
import config



@click.group()
@click.version_option()
def cli():
    """
    Tools for updating Github example-code repository
    """


def insert_copyright(lines):
    if "Copyright.txt" in lines[1]:
        return lines
    if lines[0][0] == "#":
        cmt = "#"
    else:
        cmt = "//"
    return [lines[0],
            cmt + " (c)2017 MindView LLC: see Copyright.txt\n",
            cmt + " We make no guarantees that this code is fit for any purpose.\n",
            cmt + " Visit http://OnJava8.com for more book information.\n",
            ] + lines[1:]


@cli.command()
def add_copyright():
    _add_copyright()


def _add_copyright():
    "Ensure copyright line is in all github example files"
    print("Ensuring copyright")
    candidates = \
        list(config.github_code_dir.rglob("*.java")) + \
        list(config.github_code_dir.rglob("*.py")) + \
        list(config.github_code_dir.rglob("*.cpp")) + \
        list(config.github_code_dir.rglob("*.go"))
    for c in candidates:
        with c.open() as code:
            lines = code.readlines()
        if lines[0].startswith("// ") or lines[0].startswith("# "):
            if "Copyright.txt" not in lines[1]:
                copyrighted = insert_copyright(lines)
                with c.open('w') as crighted:
                    crighted.writelines(copyrighted)


# exclude = [
#     "build.gradle",
#     "gradlew",
#     "gradlew.bat",
#     "gradle",
#     "appveyor.yml"
# ]

# @CmdLine('c')
# def clean_github_dir():
#     "Clean github example code directory"
#     print("Removing old github files >>>>>>>>>>>>")
#     for f in (
#             x for x in config.github_code_dir.glob("*")
#             if not x.stem.startswith(".")
#             and x.name not in exclude):
#         print("removing: ", f.name)
#         if f.is_dir():
#             shutil.rmtree(str(f))
#         else:
#             f.unlink()

@cli.command()
def clean_github_dir():
    _clean_github_dir()


def _clean_github_dir():
    "Clean github example code directory"
    print("Cleaning ...")
    try:
        for f in (
                x for x in config.github_code_dir.glob("*")
                if not x.stem.startswith(".")):
            print("removing: ", f.name)
            if f.is_dir():
                shutil.rmtree(str(f))
            else:
                f.unlink()
    except:
        print("Error removing files")
        sys.exit(1)


@cli.command()
def copy_examples():
    _copy_examples()

def _copy_examples():
    "Copy example tree into github example code directory"
    print("Copying new github files >>>>>>>>>>>>")
    for di in (x for x in config.example_dir.glob("*")):
        print(di.name)
        if di.is_dir():
            shutil.copytree(str(di), str(config.github_code_dir / di.name))
        else:
            shutil.copyfile(str(di), str(config.github_code_dir / di.name))


@cli.command()
def all():
    """
    Erase old github examples and copy new ones.
    YOU MUST run e extract_and_copy_build_files by hand first!!
    Ensure copyright info is on each file.
    """
    # run this by hand:
    # examples_cmd = config.tools_dir / "Examples.py"
    # os.system("python " + str(examples_cmd) + " -e" )
    _clean_github_dir()
    _copy_examples()
    _add_copyright()


if __name__ == '__main__':
    cli()
