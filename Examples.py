#! py -3
"""
Extract code example_path from On Java Markdown files.
Creates Ant build.xml file for each subdirectory.
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
from collections import defaultdict
from betools import CmdLine


rootPath = Path(sys.path[0]).parent / "on-java"
markdown_path = rootPath / "Markdown"
example_path = rootPath / "ExtractedExamples"
example_resources = rootPath / "resources" / "Examples"

tools_to_copy = [ rootPath / "tools" / f for f in [
    "output_duet.py",
    "verify_output.py",
]]

#gh_example_repo = rootPath.parent / 'OnJava-Examples'

maindef = re.compile("public\s+static\s+void\s+main")

startBuild = """\
<?xml version="1.0" ?>

<project default="run">
  <property name="chapter" value="%s"/>
  <property name="excludedfiles" value="%s"/>
  <import file="../Ant-Common.xml"/>
  <import file="../Ant-Clean.xml"/>

  <target name="run" description="Compile and run" depends="build">
"""

endBuild = """\
  </target>

</project>
"""


@CmdLine("x")
def extractExamples():
    print("Extracting examples ...")
    if not example_path.exists():
        debug("creating {}".format(example_path))
        example_path.mkdir()
    for f in example_resources.iterdir():
        # print(f)
        if f.is_dir():
            shutil.copytree(str(f), str(example_path / f.name))
        if f.is_file():
            shutil.copy(str(f), str(example_path))

    for f in tools_to_copy:
        shutil.copy(str(f), str(example_path))

    if not markdown_path.exists():
        print("Cannot find", markdown_path)
        sys.exit()

    slugline = re.compile("^(//|#) .+?\.[a-z]+$", re.MULTILINE)

    for sourceText in markdown_path.glob("*.md"):
        debug("--- {} ---".format(sourceText.name))
        with sourceText.open("rb") as chapter:
            text = chapter.read().decode("utf-8", "ignore")
            for listing in re.findall("```(.*?)\n(.*?)\n```", text, re.DOTALL):
                title = listing[1].splitlines()[0]
                if slugline.match(title):
                    debug(title)
                    fpath = title.split()[1].strip()
                    target = example_path / fpath
                    debug("writing {}".format(target))
                    if not target.parent.exists():
                        target.parent.mkdir(parents=True)
                    with target.open("w", newline='') as codeListing:
                        codeListing.write(listing[1].strip())
                        codeListing.write("\n")
                        debug("\n".join(listing[1].splitlines()))


@CmdLine("c")
def clean():
    "Remove ExtractedExamples directory"
    print("Cleaning ...")
    if example_path.exists():
        shutil.rmtree(str(example_path))


def compareWithGithub(shortForm=True):
    "Compare files from Github repository to extracted examples"
    leader = len(str(gh_example_repo)) + 1
    githubfiles = [str(file)[leader:] for file in gh_example_repo.glob("**/*")]
    githubfiles = [ghf for ghf in githubfiles if not ghf.startswith(".git")]
    duplicates = {ghf for ghf in githubfiles if githubfiles.count(ghf) > 1}
    if duplicates:
        print("duplicates = ", duplicates)

    leader2 = len(str(example_path)) + 1
    destfiles = [str(file)[leader2:] for file in example_path.glob("**/*")]
    duplicates = {ghf for ghf in destfiles if destfiles.count(ghf) > 1}
    if duplicates:
        print("duplicates = ", duplicates)

    githubfiles = set(githubfiles)
    destfiles = set(destfiles)

    runOutput = re.compile("/\* Output:.*/", re.DOTALL)
    differ = difflib.Differ()

    def rstrip(lines):
        return [line.rstrip() for line in lines]

    def show(lines, sep="#"):
        sys.stdout.writelines(lines)
        print("\n" + sep * 80)

    inBoth = [f for f in destfiles.intersection(githubfiles) if f.endswith(".java")]
    for f in inBoth:
        with (gh_example_repo / f).open() as ghf:
            with (example_path / f).open() as dstf:
                ghblock = runOutput.sub("", ghf.read())
                dstblock = runOutput.sub("", dstf.read())
                if ghblock.strip() == dstblock.strip():
                    continue
                ghtext = ghblock.splitlines(keepends=True)
                dsttext = dstblock.splitlines(keepends=True)
                print("[[[", f, "]]]")
                if shortForm:
                    show([ln + "\n" for ln in difflib.context_diff(rstrip(ghtext), rstrip(dsttext))], sep="=")
                else:
                    show([ln + "\n" for ln in differ.compare(rstrip(ghtext), rstrip(dsttext))], sep="=")


class CodeFileOptions(object):
    """docstring for CodeFileOptions"""
    def __init__(self, codeFile):
        "Should probably use regular expressions for parsing instead"
        self.codeFile = codeFile
        self.msg = ""

        self.cmdargs = None
        if "{Args:" in self.codeFile.code:
            for line in self.codeFile.lines:
                if "{Args:" in line:
                    self.cmdargs = line.split("{Args:")[1].strip()
                    self.cmdargs = self.cmdargs.rsplit("}", 1)[0]

        self.validatebyhand = "{ValidateByHand}" in self.codeFile.code

        self.exclude = None
        if "{CompileTimeError}" in self.codeFile.code:
            self.exclude = self.codeFile.name + ".java"
            # Hack for this one case rather than generalizing:
            if self.exclude.endswith("Foreign.java"):
                self.exclude = "foreign/" + self.exclude
            # if self.codeFile.subdirs:
            #     self.exclude = '/'.join(self.codeFile.subdirs) + '/' + self.exclude
            # print("SUBDIRS:", self.codeFile.subdirs)
            # print("EXCLUDING:", self.exclude)

        self.continue_on_error = None
        if "{ThrowsException}" in self.codeFile.code:
            self.continue_on_error = True
            self.msg = "* Exception was Expected *"
        elif "{IgnoreReturnValue}" in self.codeFile.code:
            self.continue_on_error = True

        self.alternatemainclass = None
        if "{main: " in self.codeFile.code:
            for line in self.codeFile.lines:
                if "{main:" in line:
                    self.alternatemainclass = line.split("{main:")[1].strip()
                    self.alternatemainclass = self.alternatemainclass.rsplit("}", 1)[0]

        self.exec_command = None
        if "{Exec:" in self.codeFile.code:
            for line in self.codeFile.lines:
                if "{Exec:" in line:
                    self.exec_command = line.split("{Exec:")[1].strip()
                    self.exec_command = self.exec_command.rsplit("}", 1)[0]
                    self.exec_command = self.exec_command.strip()

        self.timeout = None
        if "{TimeOut:" in self.codeFile.code:
            for line in self.codeFile.lines:
                if "{TimeOut:" in line:
                    self.timeout = line.split("{TimeOut:")[1].strip()
                    self.timeout = self.timeout.rsplit("}", 1)[0]
                    self.continue_on_error = True
        elif "// ui/" in self.codeFile.code or "// swt/" in self.codeFile.code or "{TimeOutDuringTesting}" in self.codeFile.code:
            self.timeout = "4000"
            self.continue_on_error = True
            self.msg = "* Timeout for Testing *"

    def classFile(self):
        start = """    <jrun cls="%s" """
        if self.alternatemainclass:
            return start % self.alternatemainclass
        if self.codeFile.package:
            return start % (self.codeFile.packageName() + '.' + self.codeFile.name)
        return start % self.codeFile.name

    def dirPath(self):
        if self.codeFile.package:
            return """dirpath="%s" """ % self.codeFile.relpath
        return ""

    def arguments(self):
        if self.cmdargs:
            if '"' in self.cmdargs:
                return """arguments='%s' """ % self.cmdargs
            else:
                return """arguments="%s" """ % self.cmdargs
        return ""

    def failOnError(self):
        if self.continue_on_error:
            return """failOnError='false' """
        return ""

    def timeOut(self):
        if self.timeout:
            return """timeOut='%s' """ % self.timeout
        return ""

    def message(self):
        if self.msg:
            return """msg='%s' """ % self.msg
        return ""

    def createRunCommand(self):
        return self.classFile() + self.dirPath() + \
            self.arguments() + self.failOnError() + \
            self.timeOut() + self.message() + "/>\n"


class CodeFile:
    def __init__(self, javaFile, chapterDir):
        self.chapter_dir = chapterDir
        self.java_file = javaFile
        # self.subdirs = str(javaFile.parent).split("\\")[2:]
        with javaFile.open() as j:
            self.code = j.read()
        self.lines = self.code.splitlines()
        self.main = None
        if maindef.search(self.code):
            self.main = True
        self.package = None
        if "package " in self.code:
            for line in self.lines:
                if line.startswith("package ") and line.strip().endswith(";"):
                    self.package = line
                    break
        self.tagLine = self.lines[0].split()[1]
        self.relpath = '../' + '/'.join(self.tagLine.split('/')[:-1])
        # print("!$!", self.relpath)
        self.name = javaFile.name.split('.')[0]
        self.options = CodeFileOptions(self)

    def run_command(self):
        if not self.main:
            return ""
        return self.options.createRunCommand()

    def __repr__(self):
        result = self.tagLine
        if self.package:
            result += "\n" + self.package
        result += "\n"
        return result

    def packageName(self):
        return self.package.split()[1][:-1]

    def checkPackage(self):
        if not self.package:
            return True
        path = '.'.join(self.tagLine.split('/')[:-1])
        packagePath = self.packageName()
        return path == packagePath


class Chapter:
    def __init__(self, dir):
        self.dir = dir
        self.code_files = [CodeFile(javaFile, dir) for javaFile in dir.glob("**/*.java")]
        self.excludes = [cf.options.exclude for cf in self.code_files if cf.options.exclude]

    def __repr__(self):
        result = "-" * 80
        result += "\n" + str(self.dir) + "\n"
        result += "-" * 80
        result += "\n"
        for cf in self.code_files:
            result += str(cf.name) + "\n"
        return result

    def checkPackages(self):
        for cf in self.code_files:
            if not cf.checkPackage():
                print("BAD PACKAGE")
                print("\t", cf.tagLine)
                print("\t", cf.package)
                print("\n".join(cf.lines))

    def makeBuildFile(self):
        buildFile = startBuild % (self.dir.name, " ".join(self.excludes))
        for cf in self.code_files:
            if any([cf.name + ".java" in f for f in self.excludes]) or cf.options.validatebyhand:
                # print("Excluding {}".format(cf))
                continue
            buildFile += cf.run_command()
        buildFile += endBuild
        with (self.dir / "build.xml").open("w") as buildxml:
            buildxml.write(buildFile)

exec = """\
    <echo message="{}"/>
    <exec executable="cmd" dir=".">
      <arg line="/c {}" />
    </exec>
"""


# @CmdLine("m")
def createAntFiles():
    "Make ant files"
    print("Creating Ant Files ...")
    chapters = [Chapter(fd) for fd in example_path.glob("*")
                if fd.is_dir()
                if not (fd / "build.xml").exists()]
    for chapter in chapters:
        chapter.checkPackages()
        chapter.makeBuildFile()



def generateAntClean():
    "Generate directives for Ant-Clean.xml"
    others = set([f.name for f in example_path.rglob("*") if not f.is_dir()
                  if not f.suffix == ".java"
                  if not f.suffix == ".class"
                  if not f.suffix == ".py"
                  if not f.suffix == ".cpp"
                  if not str(f).endswith("-output.txt")
                  if not str(f).endswith("-erroroutput.txt")
                  if f.name
                  ])
    for f in others:
        print("""        <exclude name="**/{}" />""".format(f))


def findTags(lines):
    tagRE = re.compile("{.*?}", re.DOTALL)
    topblock = []
    for line in lines:
        if line.startswith("//"):
            topblock.append(line)
        else:
            break
    topblock = [line[2:].strip() for line in topblock]
    tags = tagRE.findall(" ".join(topblock))
    return tags


@CmdLine('t')
def findAllCommentTags():
    "Find all '{}' comment tags in Java files"
    tagdict = defaultdict(list)
    for jf in [f for f in example_path.rglob("*.java")]:
        with jf.open() as code:
            lines = code.readlines()
            tags = findTags(lines)
            if tags:
                # head(jf.name)
                # print("\n".join(tags))
                for t in tags:
                    tagdict[t].append(jf.name)
    pprint.pprint(tagdict)


@CmdLine('d')
def dup_run_target():
    "Duplicate run target in all build.xml files; modify for jrunconsole"
    for build_xml in example_path.rglob("build.xml"):
        if build_xml.parent == example_path:
            continue # Skip root build.xml
        jrunconsole = []
        build_lines = build_xml.read_text().splitlines()
        inside_target = False
        for n, line in enumerate(build_lines):
            if '</target>' in line:
                jrunconsole.append(line)
                break
            if '<target name="run"' in line:
                inside_target = True
            if inside_target == True:
                new = line.replace("<jrun", "<jrunconsole")
                new = new.replace('<target name="run"', '<target name="runconsole"')
                jrunconsole.append(new)
        build_lines[n + 1 : n + 1] = [""] + jrunconsole + [""]
        build_xml.write_text("\n".join(build_lines))
        # os.system("subl {}".format(build_xml))


@CmdLine('e')
def extractAndCreateBuildFiles():
    "Clean, then extract examples from Markdown, build ant files"
    clean()
    extractExamples()
    createAntFiles()
    dup_run_target()
    os.chdir(str(example_path))
    with open("run.bat", 'w') as run:
        run.write(r"python ..\tools\Validate.py -p" + "\n")
        run.write(r"powershell .\runall.ps1" + "\n")
        run.write(r"python ..\tools\Validate.py -e" + "\n")


if __name__ == '__main__':
    CmdLine.run()
