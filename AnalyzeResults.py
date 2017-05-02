#! py -3
"""
Append output and error files to Java files
"""
TODO = """
- Test to make sure that None files indeed have no output
- Collect all tests under single flag
"""
from pathlib import Path
import pprint
import os
import sys
import re
import io
from difflib import SequenceMatcher
from sortedcontainers import SortedSet
from betools import CmdLine, ruler
from java_main import JavaMain
import config


@CmdLine('t')
def outputTagTypes():
    """Show different output tag variations"""
    types = set()
    for jfp in config.example_dir.rglob("*.java"):
        # print(jfp)
        # jf = JavaMain.JFile.with_main(jfp)
        jf = JavaMain.create(jfp)
        # print(jf)
        if jf:
            if jf.j_file.output_line:
                types.add(jf.j_file.output_line)
    pprint.pprint(types)


@CmdLine('e')
def extractResults():
    """Test extraction of all results"""
    os.chdir(str(config.example_dir))
    with Path("AttachedResults.txt").open('w') as results:
        for jfp in Path(".").rglob("*.java"):
            j_main = JavaMain.create(jfp)
            if j_main:
                results.write(ruler(jfp))
                outline = j_main.j_file.output_line
                if outline:
                    results.write(outline + "\n")
                results.write(j_main.result)
    os.system("subl AttachedResults.txt")


# @CmdLine('n')
def noOutputFixup():
    """Attach "Output: (None)" lines to empty output files"""
    os.chdir(str(config.example_dir))
    # test = open("test.txt", 'w')
    for jfp in Path(".").rglob("*.java"):
        if "gui" in jfp.parts or "swt" in jfp.parts:
            continue
        jf = JavaMain.JFile.with_main(jfp)
        if jf is None:
            continue
        if "{ValidateByHand}" in jf.code:
            continue
        if not jf.output_line:
            if JavaMain.create(jfp):
                continue
            newcode = ""
            for line in jf.lines:
                if line == "}":  # This might not work every time. Might have to search for end of code.
                    newcode += "}\n/* Output: (None) */\n"
                else:
                    newcode += line + "\n"
            with jfp.open('w') as f:
                f.write(newcode)
            os.system("subl {}".format(jfp))
            # test.write(ruler(jfp))
            # test.write(newcode)


@CmdLine('v')
def viewAttachedFiles():
    """Sublime edit all files containing output in this directory and below"""
    for java in Path(".").rglob("*.java"):
        with java.open() as codefile:
            code = codefile.read()
            if "/* Output:" in code:
                if "/* Output: (None)" in code:
                    continue
                if "/* Output: (Execute to see)" in code:
                    continue
                for n, line in enumerate(code.splitlines()):
                    if "/* Output:" in line:
                        # os.system("subl {}:{}".format(java, n))
                        os.system("subl {}".format(java))
                        continue


@CmdLine('x')
def showNulBytesInOutput():
    """Look for NUL bytes in output files`"""
    for normal in config.example_dir.rglob("*-output.txt"):
        with normal.open() as codeFile:
            if "\0" in codeFile.read():
                os.system("subl {}".format(normal))
                print(normal)
    for errors in config.example_dir.rglob("*-erroroutput.txt"):
        with errors.open() as codeFile:
            if "\0" in codeFile.read():
                os.system("subl {}".format(errors))
                print(errors)


@CmdLine('s')
def showJavaFiles():
    """Sublime edit all java files in this directory and below"""
    for java in Path(".").rglob("*.java"):
        os.system("subl {}".format(java))


@CmdLine('b')
def blankOutputFiles():
    """Show java files with expected output where there is none"""
    find_output = re.compile(r"/\* Output:(.*)\*/", re.DOTALL)
    for java in config.example_dir.rglob("*.java"):
        with java.open() as codeFile:
            output = find_output.search(codeFile.read())
            if output:
                # print(output.group(1))
                if not output.group(1).strip():
                    print(java)


@CmdLine('u')
def unexpectedOutput():
    """Show java files with output where none was expected"""
    for java in config.example_dir.rglob("*.java"):
        with java.open() as codeFile:
            if "/* Output: (None) */" in codeFile.read():
                outfile = java.with_name(java.stem + "-output.txt")
                errfile = java.with_name(java.stem + "-erroroutput.txt")
                if outfile.exists():
                    if outfile.stat().st_size:
                        print("Unexpected output: {}".format(java))
                if errfile.exists():
                    if errfile.stat().st_size:
                        print("Unexpected error output: {}".format(java))


exclude_files = [
    "HelloDate.java",
    r"concurrency\ActiveObjectDemo.java",
    r"concurrency\AtomicityTest.java",
    r"concurrency\CachedThreadPool.java",
    r"concurrency\CountDownLatchDemo.java",
    r"concurrency\DaemonFromFactory.java",
    r"concurrency\DeadlockingDiningPhilosophers.java",
    r"concurrency\FastSimulation.java",
    r"concurrency\FixedDiningPhilosophers.java",
    r"concurrency\FixedThreadPool.java",
    r"concurrency\MoreBasicThreads.java",
    r"concurrency\NIOInterruption.java",
    r"concurrency\SelfManaged.java",
    r"concurrency\SemaphoreDemo.java",
    r"concurrency\SimpleDaemons.java",
    r"concurrency\SleepingTask.java",
    r"concurrency\ThreadLocalVariableHolder.java",
    r"patterns\PaperScissorsRock.java",
    r"patterns\recyclea\RecycleA.java",
    r"patterns\visitor\BeeAndFlowers.java",
    r"concurrency\EvenGenerator.java",
    r"concurrency\GreenhouseScheduler.java",
    r"concurrency\OrnamentalGarden.java",
    r"concurrency\PipedIO.java",
    r"concurrency\SimplePriorities.java",
    r"concurrency\SimpleThread.java",
    r"concurrency\ThreadVariations.java",
    r"generics\DynamicProxyMixin.java",
    r"logging\LoggingLevelManipulation.java",
    r"logging\SimpleFilter.java",
    r"annotations\AtUnitExample4.java",
    r"concurrency\BankTellerSimulation.java",
    r"concurrency\CarBuilder.java",
    r"concurrency\ListComparisons.java",
    r"concurrency\MapComparisons.java",
    r"concurrency\ReaderWriterList.java",
    r"concurrency\restaurant2\RestaurantWithQueues.java",
    r"generics\Mixins.java",
    r"io\LockingMappedFiles.java",
    r"logging\ConfigureLogging.java",
    r"logging\LoggingLevels.java",
    r"operators\HelloDate.java",
    r"annotations\AtUnitComposition.java",
    r"annotations\AtUnitExample3.java",
    r"annotations\AtUnitExternalTest.java",
    r"annotations\HashSetTest.java",
    r"annotations\UseCaseTracker.java",
    r"concurrency\Interrupting.java",
    r"concurrency\SerialNumberChecker.java",
    r"concurrency\SimpleMicroBenchmark.java",
    r"concurrency\SynchronizationComparisons.java",
    r"concurrency\SyncObject.java",
    r"collections\ListPerformance.java",
    r"io\Logon.java",
    r"logging\CustomHandler.java",
    r"object\HelloDate.java",
    r"annotations\AtUnitExample1.java",
    r"annotations\AtUnitExample2.java",
    r"concurrency\ExchangerDemo.java",
    r"concurrency\ExplicitCriticalSection.java",
    r"concurrency\Restaurant.java",
    r"collections\MapPerformance.java",
    r"collections\SetPerformance.java",
    r"exceptions\LoggingExceptions.java",
    r"logging\InfoLogging.java",
    r"logging\InfoLogging2.java",
    r"logging\LogToFile.java",
    r"logging\LogToFile2.java",
    r"logging\MultipleHandlers.java",
    r"logging\MultipleHandlers2.java",
    r"annotations\AtUnitExample5.java",
    r"concurrency\Daemons.java",
    r"concurrency\HorseRace.java",
    r"concurrency\ToastOMatic.java",
    r"enums\ConstantSpecificMethod.java",
    r"exceptions\LoggingExceptions2.java",
    r"io\MakeDirectories.java",
    r"io\MappedIO.java",
    r"io\PreferencesDemo.java",
    r"logging\PrintableLogRecord.java",
    r"references\Compete.java",
    # Keep an eye on:
    r"strings\JGrep.java",
]

months = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
memlocation = re.compile("@[0-9a-z]{5,7}")
datestamp1 = re.compile("(?:[MTWFS][a-z]{2} ){0,1}[JFMASOND][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2} [A-Z]{3} \d{4}")
datestamp2 = re.compile("[JFMASOND][a-z]{2} \d{1,2}, \d{4} \d{1,2}:\d{1,2}:\d{1,2} (:?AM|PM)")


def showAndBlank(matchobj):
    print("stripped:", matchobj.group(0))
    return ""


def stripdates(text):
    text = datestamp1.sub(showAndBlank, text)
    text = datestamp2.sub(showAndBlank, text)
    return text


@CmdLine('z')
def test_regexp():
    "testing regular expressions"
    for jfp in config.example_dir.rglob("*.java"):
        if "gui" in jfp.parts or "swt" in jfp.parts:
            continue
        if jfp.name in exclude_files:
            continue
        generated = generated_output(jfp)
        if generated is None:
            continue
        # embedded = embedded_output(jfp)
        # for m in datestamp1.findall(embedded):
        #     mems.append(m)
        generated = stripdates(generated)
        for d in generated.splitlines():
            if "201" in d or "200" in d:
                if re.search(months, d):
                    print(d)
    # print("-" * 60)
    # for m in sorted(mems):
    #     print(m)


def generated_output(jfp):
    j_main = JavaMain.create(jfp)
    if not j_main:
        return None
    return j_main.result.strip()


def embedded_output(jfp):
    find_output = re.compile(r"/\* (Output:.*)\*/", re.DOTALL)
    with jfp.open() as java:
        output = find_output.search(java.read())
        assert output, "No embedded output: in {}".format(jfp)
        return "\n".join(output.group(1).strip().splitlines()[1:])


class LineCountDiff:
    """Checks for line count differences"""
    band = 2  # number of lines different before reporting
    line_count_report = config.example_dir / "LineCountReport.txt"

    def __init__(self):
        if LineCountDiff.line_count_report.exists():
            LineCountDiff.line_count_report.unlink()

    def compare(self, jfp, embedded, generated):
        emb = embedded.strip().splitlines()
        gen = generated.strip().splitlines()
        delta = abs(len(emb) - len(gen))
        if delta > LineCountDiff.band:
            report = io.StringIO()
            report.write("\n" + "*" * 60)
            report.write("\n" + ruler(jfp.relative_to(config.example_dir)))
            report.write("line count difference: {}\n".format(delta))
            report.write(ruler("Attached"))
            report.write(embedded)
            report.write("\n" + ruler("Generated"))
            report.write(generated)
            with LineCountDiff.line_count_report.open('a') as lcr:
                lcr.write(report.getvalue())


floatnum = re.compile(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')


class WordContentDiff:
    """Checks for differences in the content"""
    content_report = config.example_dir / "ContentReport.txt"

    def __init__(self):
        if WordContentDiff.content_report.exists():
            WordContentDiff.content_report.unlink()

    def compare(self, jfp, embedded, generated):
        def remove_numbers(lst):
            lst = [w for w in lst if not re.match("\d+", w)]
            lst = [w for w in lst if not floatnum.match(w)]
            return lst
        emb = SortedSet(remove_numbers(re.split('\W+', embedded)))
        gen = SortedSet(remove_numbers(re.split('\W+', generated)))
        delta = emb ^ gen
        if len(delta) > 1:
            report = io.StringIO()
            report.write("\n" + "*" * 60)
            report.write("\n" + ruler(jfp.relative_to(config.example_dir)))
            for d in delta:
                report.write(" {} ".format(d))
            report.write("\n" + ruler("Attached"))
            report.write(embedded)
            report.write("\n" + ruler("Generated"))
            report.write(generated)
            with WordContentDiff.content_report.open('a') as lcr:
                lcr.write(report.getvalue())


@CmdLine('c')
def compare_output():
    """Compare attached and newly-generated output"""
    TODO = """
      - Strip out date/time information using regex before comparing
      - Make it possible to compare/append on a single file
      - Could also compare number of lines
    """
    ratio_target = 1.0
    memlocation = re.compile("@[0-9a-z]{5,7}")
    reports = list()
    line_count_diff = LineCountDiff()
    word_content_diff = WordContentDiff()
    output_comparison = config.example_dir / "OutputComparisons.txt"
    # This is support to make it easy to add to exclude_files:
    compare_exclusions = config.example_dir / "CompareExclusions.txt"

    for jfp in config.example_dir.rglob("*.java"):
        if "gui" in jfp.parts or "swt" in jfp.parts:
            continue
        if jfp.name in exclude_files:
            continue
        generated = generated_output(jfp)
        if generated is None:
            continue
        embedded = embedded_output(jfp)

        line_count_diff.compare(jfp, embedded, generated)

        gen_stripped = memlocation.sub("", generated)
        gen_stripped = stripdates(gen_stripped)
        emb_stripped = memlocation.sub("", embedded)
        emb_stripped = stripdates(emb_stripped)
        word_content_diff.compare(jfp, emb_stripped, gen_stripped)
        comp = SequenceMatcher(None, emb_stripped, gen_stripped)
        ratio = comp.ratio()
        if ratio < ratio_target:
            print(jfp.relative_to(config.example_dir))
            print("ratio: {}\n".format(ratio))
            report = io.StringIO()
            report.write("\n" + "*" * 60)
            report.write("\n" + ruler(jfp.relative_to(config.example_dir)))
            report.write("ratio: {}\n".format(ratio))
            report.write(ruler("Attached"))
            report.write(embedded)
            report.write("\n" + ruler("Generated"))
            report.write(generated)
            result = (ratio, report.getvalue(), str(jfp.relative_to(config.example_dir)))
            reports.append(result)

    reports = sorted(reports)

    with output_comparison.open('w') as comparisons:
        for report in reports:
            comparisons.write(report[1])

    with compare_exclusions.open('w') as exclusions:
        for report in reports:
            exclusions.write('r"' + report[2] + "\",\n")

    if compare_exclusions.exists():
        os.system("subl {}".format(compare_exclusions))
    if output_comparison.exists():
        os.system("subl {}".format(output_comparison))
    if LineCountDiff.line_count_report.exists():
        os.system("subl {}".format(LineCountDiff.line_count_report))
    if WordContentDiff.content_report.exists():
        os.system("subl {}".format(WordContentDiff.content_report))


@CmdLine('a')
def attachFiles():
    """Attach standard and error output to all files"""
    os.chdir(str(config.example_dir))
    test = open("AllFilesWithOutput.txt", 'w')
    longOutput = open("LongOutput.txt", 'w')
    for jfp in Path(".").rglob("*.java"):
        if "gui" in jfp.parts or "swt" in jfp.parts:
            continue
        j_main = JavaMain.create(jfp)
        if j_main:
            j_main.write_modified_file()
            test.write(ruler())
            test.write(j_main.new_code())
            if j_main.long_output:
                longOutput.write(ruler())
                longOutput.write(j_main.new_code())
    # os.system("subl AllFilesWithOutput.txt")
    # os.system("subl LongOutput.txt")


if __name__ == '__main__':
    CmdLine.run()


# @CmdLine('o')
# def allOutputTagLines():
#     """Shows all lines starting with /*"""
#     allvariations = set()
#     os.chdir(str(config.example_dir))
#     for jfp in Path(".").rglob("*.java"):
#         with jfp.open() as code:
#             for line in code.readlines():
#                 if line.startswith("/*"):
#                     allvariations.add(line)
#     pprint.pprint(allvariations)

# @CmdLine('w')
# def boldWords():
#     """
#     Create list of bolded words to be used as a Word dictionary
#     """
#     from bs4 import BeautifulSoup
#     import codecs
#     import string
#     clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
#     def flense(word):
#         word = clean(word)
#         word = word.split('(')[0]
#         word = word.split('[')[0]
#         return word.strip()

#     os.chdir(str(config.example_dir / ".."))
#     spelldict = SortedSet()
#     with codecs.open(str(Path("OnJava.htm")),'r', encoding='utf-8', errors='ignore') as book:
#         soup = BeautifulSoup(book.read())
#         for b in soup.find_all("b"):
#             text = (" ".join(b.text.split())).strip()
#             if " " in text:
#                 continue
#             text = flense(text)
#             if text:
#                 spelldict.add(text)

#     with Path("BoldedWords.txt").open('w') as boldwords:
#         for word in spelldict:
#             if len(word):
#                 if word[0] in string.ascii_letters:
#                     boldwords.write(word + "\n")
