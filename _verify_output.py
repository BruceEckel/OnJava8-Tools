#! py -3
# Requires Python 3.5
# Validates output from executable Java programs in "On Java 8."
# Use chain of responsibility to successively try strategies until one matches
import os
import re
import sys
import textwrap
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

from betools import CmdLine

import config


########### Chain of Responsibility Match Finder #######################

def exact_match(text): return text


memlocation = re.compile("@[0-9a-z]{5,7}")


def ignore_memory_addresses(text):
    return memlocation.sub("", text)


datestamp1 = re.compile(
    "(?:[MTWFS][a-z]{2} ){0,1}[JFMASOND][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2} [A-Z]{3} \d{4}")
datestamp2 = re.compile(
    "[JFMASOND][a-z]{2} \d{1,2}, \d{4} \d{1,2}:\d{1,2}:\d{1,2} (:?AM|PM)")


def ignore_dates(text):
    for pat in [datestamp1, datestamp2]:
        text = pat.sub("", text)
    return text


def ignore_digits(input_text):
    return re.sub("-?\d", "", input_text)


def sort_lines(input_text):
    return "\n".join(sorted(input_text.splitlines())).strip()


def sort_words(input_text):
    return "\n".join(sorted(input_text.split())).strip()


def unique_lines(input_text):
    return "\n".join(sorted(list(set(input_text.splitlines()))))


# Fairly extreme but will still reveal significant changes:
def unique_words(input_text):
    return "\n".join(sorted(set(input_text.split())))


# Fairly extreme but will still reveal significant changes:
word_only = re.compile("[A-Za-z]+")


def words_only(input_text):
    return "\n".join(
        sorted([w for w in input_text.split()
                if word_only.fullmatch(w)]))


def ratio(input_text):
    return True


def no_match(input_text): return True


# Chain of responsibility:
strategies = [
    # Filter                  # Retain result
    # for rest of chain
    (exact_match,               False),
    (ignore_dates,              True),
    (ignore_memory_addresses,   True),
    (sort_lines,                False),
    (ignore_digits,             False),
    (sort_words,                False),
    (unique_lines,              False),
    (unique_words,              False),
    (words_only,                False),
    (ratio,                     False),
    # (no_match,                  False),
]


class Validator(defaultdict):  # Map of lists
    compare_output = config.example_dir / "compare_output.bat"

    def __init__(self):
        super().__init__(list)
        # Erase the old results files:
        if Validator.compare_output.exists():
            Validator.compare_output.unlink()
        for strategy, retain in strategies:
            strat_batch = config.example_dir / (strategy.__name__ + ".bat")
            if strat_batch.exists():
                strat_batch.unlink()

    def find_output_match(self, javafile, embedded_output, generated_output):
        for strategy, retain in strategies:
            strategy_name = strategy.__name__
            if strategy_name is "ratio":
                print(strategy_name)

            def record_output(result=None):
                tfile = javafile.with_suffix("." + strategy_name)
                edit_command = "subl " + str(tfile) + "\n"
                with (config.example_dir / (strategy_name + ".bat")).open('a') as strat_batch:
                    strat_batch.write(edit_command)
                with Validator.compare_output.open('a') as batch:
                    batch.write(edit_command)
                with tfile.open('w') as trace_file:
                    trace_file.write(javafile.read_text() + "\n\n")
                    trace_file.write("// === Actual ===\n\n")
                    trace_file.write(str(generated_output))
                    if result:
                        trace_file.write("\n" + "*" * 55 + "\n")
                        trace_file.write(result + "\n")

            if strategy_name is "ratio":
                print("++++ " + strategy_name)
                ratio = SequenceMatcher(
                    None, embedded_output, generated_output).ratio()
                record_output("Ratio = %.2f" % ratio)
                return

            filtered_embedded_output = strategy(embedded_output)
            filtered_generated_output = strategy(generated_output)
            if filtered_embedded_output == filtered_generated_output:
                self[strategy_name].append(str(javafile.relative_to(config.example_dir)))
                if strategy_name is "exact_match":
                    return
                record_output()
                return
            if retain:
                embedded_output = filtered_embedded_output
                generated_output = filtered_generated_output

    def log_results(self):
        log = open("verified_output.txt", 'w')
        for strategy, retain in strategies:
            key = strategy.__name__
            # if key is "exact_match":
            #     for java in self[key]:
            #         print(java)
            # elif key in self:
            if key in self:
                log.write("\n" + (" " + key + " ").center(45, "=") + "\n")
                for java in self[key]:
                    log.write(java + "\n")
        log.close()


def validate_all():
    # Generate '.p1' files:
    config.reformat_runoutput_files()
    find_output = re.compile(r"/\* (Output:.*)\*/", re.DOTALL)
    validator = Validator()
    for outfile in config.example_dir.rglob("*.p1"):
        javafile = outfile.with_suffix(".java")
        if not javafile.exists():
            print(str(outfile) + " has no javafile")
            sys.exit(1)
        javatext = javafile.read_text()
        if "{VisuallyInspectOutput}" in javatext:
             # Do not test {VisuallyInspectOutput}
             print("Skipping {} because of {VisuallyInspectOutput} tag".format(
                javafile.relative_to(config.example_dir)))
            continue
        if "/* Output:" not in javatext:
            print(str(outfile) + " has no /* Output:")
            sys.exit(1)
        validator.find_output_match(
            javafile,
            find_output.search(javatext).group(0).strip(),
            outfile.read_text().strip())
    validator.log_results()


@CmdLine("a")
def verify_all_output():
    """
    Generate .p1 files and check against all matching strategies
    """
    validate_all()
    os.system("cat verified_output.txt")


@CmdLine("u")
def display_unmatched_output():
    """
    Generate .p1 files and display those that don't match any strategy
    """
    print("Verifying .out and .err files against embedded /* Output:")
    validate_all()
    print("[Displaying no_match.bat:]")
    os.system("cat no_match.bat")


if __name__ == '__main__':
    CmdLine.run()
