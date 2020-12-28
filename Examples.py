#! py -3
"""
Extract code to config.example_dir from On Java 8 Markdown files.
Configures for Gradle build by copying from OnJava8-Examples.
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


def initialize_example_dir(example_dir_path):
    if example_dir_path.exists():
        debug(f"Already exists: {example_dir_path}")
        return
    debug(f"initializing {example_dir_path}")
    example_dir_path.mkdir()
    print(f"Copying Test Files to {example_dir_path}")
    for test_path in list(config.github_code_dir.rglob("tests/*")):
        destination = example_dir_path / test_path.relative_to(config.github_code_dir)
        if test_path.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            debug(f"{test_path.relative_to(config.github_code_dir.parent)}" +
                  f"\n\t-> {destination.relative_to(example_dir_path)}")
            shutil.copy(str(test_path), str(destination))
    for f in tools_to_copy:
        shutil.copy(str(f), str(example_dir_path))


@cli.command()
def copy_test_files():
    initialize_example_dir(config.example_dir)


maindef = re.compile(r"public\s+static\s+void\s+main")
slugline = re.compile(r"^(//|#) .+?\.[a-z]+$", re.MULTILINE)
xmlslug = re.compile(r"^<!-- .+?\.[a-z]+ +-->$", re.MULTILINE)


def extract_examples_to_path(example_dir_path):
    print("Extracting examples ...")
    initialize_example_dir(example_dir_path)
    exists(config.markdown_dir.exists)

    for sourceText in config.markdown_dir.glob("*.md"):
        debug(f"--- {sourceText.name} ---")
        with sourceText.open("rb") as chapter:
            text = chapter.read().decode("utf-8", "ignore")
            for group in re.findall("```(.*?)\n(.*?)\n```", text, re.DOTALL):
                listing = group[1].splitlines()
                title = listing[0]
                if slugline.match(title) or xmlslug.match(title):
                    debug(title)
                    fpath = title.split()[1].strip()
                    target = example_dir_path / fpath
                    debug(f"writing {target}")
                    if not target.parent.exists():
                        target.parent.mkdir(parents=True)
                    with target.open("w", newline="") as codeListing:
                        debug(group[1])
                        if slugline.match(title):
                            codeListing.write(group[1].strip() + "\n")
                        elif xmlslug.match(title):  # Drop the first line
                            codeListing.write("\n".join(listing[1:]))


@cli.command()
def extract_examples():
    extract_examples_to_path(config.example_dir)


def init_gradle_files():
    print("Copying Gradle Files ...")
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
        print(f"{gradle_path.relative_to(config.rootPath.parent)}" +
              f"\n\t-> {destination.relative_to(config.example_dir)}")
        # shutil.copy(str(gradle_path), str(destination))


@cli.command()
def copy_gradle_files():
    init_gradle_files()


def make_task(task_name, package_name=None):
    if package_name:
        main = f"{package_name}.{task_name}"
    else:
        main = task_name
    return (
        task_name,
        f"""
task {task_name}(type: JavaExec) {{
    classpath javaClassPath
    main = '{main}'
}}
""",
    )


@cli.command()
def create_tasks():
    tasks = """
def javaClassPath = sourceSets.main.runtimeClasspath

"""
    task_dict = {}
    print("Creating tasks.gradle ...")
    print(config.example_dir)
    if not config.example_dir.exists():
        print("Cannot find", config.example_dir)
        sys.exit()
    for java_file in config.example_dir.rglob("*.java"):
        text = java_file.read_text()
        lines = text.splitlines()
        if not re.search(r"public\s+static\s+void\s+main", text):
            continue
        package_name = None
        for line in lines:
            if line.startswith("package "):
                package_name = line.split()[1][:-1]
        k, v = make_task(java_file.stem, package_name)
        task_dict[k] = v
    for k in sorted(task_dict):
        tasks += task_dict[k]
    tasks += """
task run (dependsOn: [
"""
    for k in sorted(task_dict):
        tasks += f"    '{k}',\n"
    tasks = tasks[:-1]  # Strip last comma
    tasks += """
    ]) {
    doLast {
        println '*** run complete ***'
    }
}
"""
    (config.example_dir / "gradle" / "tasks.gradle").write_text(tasks)
    print(f"{len(task_dict)} tasks")


def _clean():
    """Remove Examples Directories"""
    print(erase(config.example_dir))
    print(erase(config.java11_dir))


@cli.command()
def clean():
    _clean()


@cli.command()
def all_regenerate():
    """Clean, extract Markdown examples, copy gradle files from OnJava-Examples"""
    print("Extracting ...")
    _clean()
    extract_examples_to_path(config.example_dir)
    init_gradle_files()


if __name__ == "__main__":
    cli()
