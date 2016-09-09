#! py -3
"""
Extract code example_path from On Java Markdown files.
Configures for Gradle build by copying from OnJava-Examples.
"""
TODO = """
incorporate exec_command into build.xml
"""
import logging
from logging import debug
# logging.basicConfig(filename= __file__.split('.')[0] + ".log", level=logging.DEBUG)
from pathlib import Path
import sys
import os
import re
import shutil
import pprint
import difflib
from betools import CmdLine


rootPath = Path(sys.path[0]).parent / "on-java"
markdown_path = rootPath / "Markdown"
example_path = rootPath / "ExtractedExamples"
example_resources = Path(sys.path[0]) / "example-resources"
repo_examples = Path(sys.path[0]).parent / "OnJava-Examples"


@CmdLine("t")
def copyTestFiles():
    print("Copying Test Files ...")
    for test_path in list(repo_examples.rglob("tests/*")):
        dest = example_path / test_path.relative_to(repo_examples)
        if(test_path.is_file()):
            if(not dest.parent.exists()):
                print("creating " + str(dest.parent))
                os.makedirs(str(dest.parent))
            print("copy " + str(test_path.relative_to(repo_examples.parent)) + " " + str(dest.relative_to(example_path)))
            shutil.copy(str(test_path), str(dest))


tools_to_copy = [ Path(sys.path[0]) / f for f in [
    "_verify_output.py",
    "update_extracted_example_output.py", # For Development
    "check.bat", # For development
    "gg.bat", # Short for gradlew
]]

maindef = re.compile("public\s+static\s+void\s+main")

@CmdLine("x")
def extractExamples():
    print("Extracting examples ...")
    if not example_path.exists():
        debug("creating {}".format(example_path))
        example_path.mkdir()
    copyTestFiles()
    # for f in example_resources.iterdir():
    #     if f.is_dir():
    #         shutil.copytree(str(f), str(example_path / f.name))
    #     if f.is_file():
    #         shutil.copy(str(f), str(example_path))

    for f in tools_to_copy:
        shutil.copy(str(f), str(example_path))

    if not markdown_path.exists():
        print("Cannot find", markdown_path)
        sys.exit()

    slugline = re.compile("^(//|#) .+?\.[a-z]+$", re.MULTILINE)
    xmlslug  = re.compile("^<!-- .+?\.[a-z]+ +-->$", re.MULTILINE)

    for sourceText in markdown_path.glob("*.md"):
        debug("--- {} ---".format(sourceText.name))
        with sourceText.open("rb") as chapter:
            text = chapter.read().decode("utf-8", "ignore")
            for group in re.findall("```(.*?)\n(.*?)\n```", text, re.DOTALL):
                listing = group[1].splitlines()
                title = listing[0]
                if slugline.match(title) or xmlslug.match(title):
                    debug(title)
                    fpath = title.split()[1].strip()
                    target = example_path / fpath
                    debug("writing {}".format(target))
                    if not target.parent.exists():
                        target.parent.mkdir(parents=True)
                    with target.open("w", newline='') as codeListing:
                        debug(group[1])
                        if slugline.match(title):
                            codeListing.write(group[1].strip() + "\n")
                        elif xmlslug.match(title): # Drop the first line
                            codeListing.write("\n".join(listing[1:]))


@CmdLine("g")
def copyGradleFiles():
    print("Copying Gradle Files ...")
    for gradle_path in list(repo_examples.rglob("*gradle*")) + \
                       list(repo_examples.rglob("*.xml")) + \
                       list(repo_examples.rglob("*.yml")) + \
                       list(repo_examples.rglob("*.md")):
        dest = example_path / gradle_path.relative_to(repo_examples)
        if(gradle_path.is_file()):
            if(not dest.parent.exists()):
                print("creating " + str(dest.parent))
                os.makedirs(str(dest.parent))
            print("copy " + str(gradle_path.relative_to(repo_examples.parent)) + " " + str(dest.relative_to(example_path)))
            shutil.copy(str(gradle_path), str(dest))


@CmdLine("c")
def clean():
    "Remove ExtractedExamples directory"
    print("Cleaning ...")
    try:
        if example_path.exists():
            shutil.rmtree(str(example_path))
    except:
        print("Old path removal failed")
        raise RuntimeError()

go_bat = """\
gradlew --parallel --daemon run > output.txt 2> errors.txt
START /min "C:\Program Files\Windows Media Player\wmplayer.exe" %windir%\media\Alarm07.wav
rem find . -size 0 -type f
"""

@CmdLine('e')
def extractAndCopyBuildFiles():
    "Clean, then extract examples from Markdown, build ant files"
    clean()
    extractExamples()
    copyGradleFiles()
    os.chdir(str(example_path))
    with open("go.bat", 'w') as run:
        run.write(go_bat)

    # os.chdir(str(example_path))
    # with open("run.bat", 'w') as run:
    #     run.write(r"python ..\tools\Validate.py -p" + "\n")
    #     run.write(r"powershell .\runall.ps1" + "\n")
    #     run.write(r"python ..\tools\Validate.py -e" + "\n")


if __name__ == '__main__':
    CmdLine.run()
