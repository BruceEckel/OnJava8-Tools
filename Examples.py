#! py -3
"""
Extract code to config.example_dir from On Java 8 Markdown files.
Configures for Gradle build by copying from OnJava8-Examples.
Creates a special directory for the Java 11 Chapter, which requires JDK11.
"""
import logging
import re
import shutil
import sys
from logging import debug
from pathlib import Path

import click

import config
from directories import exists, erase

logging.basicConfig(
    filename=__file__.split(".")[0] + ".log", filemode="w", level=logging.DEBUG
)

# For Development:
tools_to_copy = [
    Path(sys.path[0]) / f
    for f in [
        "__tests.bat",
        "_check_markdown.bat",
        "_output_file_check.bat",
        "_verify_output.bat",
        "_update_extracted_example_output.bat",
        "_capture_gradle.bat",
        "chkstyle.bat",  # Run checkstyle, capturing output
        # "gg.bat", # Short for gradlew
    ]
]


@click.group()
@click.version_option()
def cli():
    pass


cli.help = __doc__


def create_dir(example_dir_path):
    if example_dir_path.exists():
        debug(f"Already exists: {example_dir_path}")
        return
    example_dir_path.mkdir()


def initialize_example_dir():
    create_dir(config.example_dir)
    print(f"Copying Test Files to {config.example_dir}")
    for test_path in list(config.github_code_dir.rglob("tests/*")):
        destination = config.example_dir / test_path.relative_to(config.github_code_dir)
        if test_path.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            debug(f"{test_path.relative_to(config.github_code_dir.parent)}" +
                  f"\n\t-> {destination.relative_to(config.example_dir)}")
            shutil.copy(str(test_path), str(destination))
    for f in tools_to_copy:
        shutil.copy(str(f), str(config.example_dir))


maindef = re.compile(r"public\s+static\s+void\s+main")
slugline = re.compile(r"^(//|#) .+?\.[a-z]+$", re.MULTILINE)
xmlslug = re.compile(r"^<!-- .+?\.[a-z]+ +-->$", re.MULTILINE)


def extract_examples_from_chapter(chapter: Path, destination: Path):
    print(f"{chapter.name} Examples ...")
    with chapter.open("rb") as chapter:
        text = chapter.read().decode("utf-8", "ignore")
        for group in re.findall("```(.*?)\n(.*?)\n```", text, re.DOTALL):
            listing = group[1].splitlines()
            title = listing[0]
            if slugline.match(title) or xmlslug.match(title):
                debug(title)
                fpath = title.split()[1].strip()
                target = destination / fpath
                debug(f"writing {target}")
                if not target.parent.exists():
                    target.parent.mkdir(parents=True)
                with target.open("w", newline="") as codeListing:
                    debug(group[1])
                    if slugline.match(title):
                        codeListing.write(group[1].strip() + "\n")
                    elif xmlslug.match(title):  # Drop the first line
                        codeListing.write("\n".join(listing[1:]))


def extract_all_examples():
    exists(config.markdown_dir)
    exists(config.github_code_dir)
    initialize_example_dir()  # Doesn't erase
    create_dir(config.java11_dir)

    for chapter in config.markdown_dir.glob("*.md"):
        if "_Java_11" in chapter.name:
            extract_examples_from_chapter(chapter, config.java11_dir)
        else:
            extract_examples_from_chapter(chapter, config.example_dir)


def init_example_dir_gradle_files():
    print(f"Copying Gradle Files to {config.example_dir}")
    source = config.github_code_dir
    exists(source)

    def sources_generator():
        paths = [
            (source, "*gradle*"),
            (source, "*.xml"),
            (source, "*.yml"),
            (source, "*.md"),
            (source / "buildSrc", "*")
        ]
        for base, pattern in paths:
            yield [path for path in base.rglob(pattern) if path.is_file()]

    for gradle_path in [path for source in sources_generator() for path in source]:  # Flatten
        destination = config.example_dir / gradle_path.relative_to(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        debug(f"{gradle_path.relative_to(config.rootPath.parent)}" +
              f"\n\t-> {destination.relative_to(config.example_dir)}")
        print(f"{gradle_path.name}...", end="")
        shutil.copy(str(gradle_path), str(destination))
    print("\n---")


def init_java11_dir_gradle_files():
    print(f"Copying Gradle Files to {config.java11_dir}")
    source = config.java11_resources
    destination = config.java11_dir
    exists(source)
    exists(destination)
    shutil.copytree(source, destination, dirs_exist_ok=True)


def remove_examples_directories():
    print(erase(config.example_dir))
    print(erase(config.java11_dir))


@cli.command()
def clean():
    """Remove Examples Directories"""
    remove_examples_directories()


@cli.command()
def all():
    """Clean, extract Markdown examples, copy gradle files from OnJava-Examples"""
    print("Extracting ...")
    remove_examples_directories()
    extract_all_examples()
    init_example_dir_gradle_files()
    init_java11_dir_gradle_files()


if __name__ == "__main__":
    cli()
