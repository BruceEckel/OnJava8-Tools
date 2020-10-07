#! py -3
# Extract code config.example_dir from On Java Markdown files.
# Configures for Gradle build by copying from OnJava-Examples.
import logging
import os
import re
import shutil
import sys
from logging import debug
from pathlib import Path

import click

import config

logging.basicConfig(filename=__file__.split(
    '.')[0] + ".log", filemode='w', level=logging.DEBUG)

# For Development:
tools_to_copy = [Path(sys.path[0]) / f for f in [
    "__tests.bat",
    "_check_markdown.bat",
    "_output_file_check.bat",
    "_verify_output.bat",
    "_update_extracted_example_output.bat",
    "_capture_gradle.bat",
    "chkstyle.bat",  # Run checkstyle, capturing output
    # "gg.bat", # Short for gradlew
]]


@click.group()
@click.version_option()
def cli():
    """
    Extract code to config.example_dir from On Java Markdown files
    """



def copyTestFiles():
    print("Copying Test Files ...")
    for test_path in list(config.github_code_dir.rglob("tests/*")):
        dest = config.example_dir / \
            test_path.relative_to(config.github_code_dir)
        if(test_path.is_file()):
            if(not dest.parent.exists()):
                debug("creating " + str(dest.parent))
                os.makedirs(str(dest.parent))
            debug("copy " + str(test_path.relative_to(config.github_code_dir.parent)
                                ) + " " + str(dest.relative_to(config.example_dir)))
            shutil.copy(str(test_path), str(dest))


@cli.command()
def copy_test_files():
    copyTestFiles()


maindef = re.compile("public\s+static\s+void\s+main")


def extractExamples():
    print("Extracting examples ...")
    if not config.example_dir.exists():
        debug("creating {}".format(config.example_dir))
        config.example_dir.mkdir()
    copyTestFiles()

    for f in tools_to_copy:
        shutil.copy(str(f), str(config.example_dir))

    if not config.markdown_dir.exists():
        print("Cannot find", config.markdown_dir)
        sys.exit()

    slugline = re.compile("^(//|#) .+?\.[a-z]+$", re.MULTILINE)
    xmlslug = re.compile("^<!-- .+?\.[a-z]+ +-->$", re.MULTILINE)

    for sourceText in config.markdown_dir.glob("*.md"):
        debug("--- {} ---".format(sourceText.name))
        with sourceText.open("rb") as chapter:
            text = chapter.read().decode("utf-8", "ignore")
            for group in re.findall("```(.*?)\n(.*?)\n```", text, re.DOTALL):
                listing = group[1].splitlines()
                title = listing[0]
                if slugline.match(title) or xmlslug.match(title):
                    debug(title)
                    fpath = title.split()[1].strip()
                    target = config.example_dir / fpath
                    debug("writing {}".format(target))
                    if not target.parent.exists():
                        target.parent.mkdir(parents=True)
                    with target.open("w", newline='') as codeListing:
                        debug(group[1])
                        if slugline.match(title):
                            codeListing.write(group[1].strip() + "\n")
                        elif xmlslug.match(title):  # Drop the first line
                            codeListing.write("\n".join(listing[1:]))


@cli.command()
def extract_examples():
    extractExamples()


def copyGradleFiles():
    print("Copying Gradle Files ...")
    if not config.github_code_dir.exists():
        print("Doesn't exist: %s" % config.github_code_dir)
        sys.exit(1)
    for gradle_path in list(config.github_code_dir.rglob("*gradle*")) + \
            list(config.github_code_dir.rglob("*.xml")) + \
            list(config.github_code_dir.rglob("*.yml")) + \
            list(config.github_code_dir.rglob("*.md")) + \
            list((config.github_code_dir / "buildSrc").rglob("*")):
        dest = config.example_dir / \
            gradle_path.relative_to(config.github_code_dir)
        if gradle_path.is_file():
            if(not dest.parent.exists()):
                debug("creating " + str(dest.parent))
                os.makedirs(str(dest.parent))
            debug("copy " + str(gradle_path.relative_to(config.github_code_dir.parent)
                                ) + " " + str(dest.relative_to(config.example_dir)))
            shutil.copy(str(gradle_path), str(dest))


@cli.command()
def copy_gradle_files():
    copyGradleFiles()


def make_task(task_name, package_name = None):
    if package_name:
        main = "{}.{}".format(package_name, task_name)
    else:
        main = task_name
    return task_name, f"""
task {task_name}(type: JavaExec) {{
    classpath javaClassPath
    main = '{main}'
}}
"""


@cli.command()
def createTasks():
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
        if not re.search("public\s+static\s+void\s+main", text):
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
    tasks = tasks[:-1] # Strip last comma
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
    "Remove ExtractedExamples directory"
    print("Cleaning ...")
    try:
        if config.example_dir.exists():
            shutil.rmtree(str(config.example_dir))
    except:
        print("Old path removal failed")
        raise RuntimeError()

@cli.command()
def clean():
    _clean()

@cli.command()
def all():
    "Clean, then extract examples from Markdown, copy gradle files from OnJava-Examples"
    print("Extracting ...")
    _clean()
    extractExamples()
    copyGradleFiles()


if __name__ == '__main__':
    cli()
