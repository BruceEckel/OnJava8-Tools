#! py -3
# Requires Python 3.5
# Validates output from executable Java programs in "On Java 8."
# If direct comparison of actual output with output stored in Java file fails,
# Use chain of responsibility to successively try strategies until one matches
# or all fail
from pathlib import Path
import textwrap
import re
import sys
import os
import textwrap
from collections import defaultdict
WIDTH = 59 # Max line width

#################### Phase 1: Basic formatting #####################

def adjust_lines(text):
    text = text.replace("\0", "NUL")
    lines = text.splitlines()
    slug = lines[0]
    if "(First and Last " in slug:
        num_of_lines = int(slug.split()[5])
        adjusted = lines[:num_of_lines + 1] +\
            ["...________...________...________...________..."] +\
            lines[-num_of_lines:]
        return "\n".join(adjusted)
    elif "(First " in slug:
        num_of_lines = int(slug.split()[3])
        adjusted = lines[:num_of_lines + 1] +\
            ["                  ..."]
        return "\n".join(adjusted)
    else:
        return text

def fill_to_width(text):
    result = ""
    for line in text.splitlines():
        result += textwrap.fill(line, width = WIDTH) + "\n"
    return result.strip()

def phase1():
    """
    (0) Do first/last lines before formatting to width
    (1) Combine output and error (if present) files
    (2) Format all output to width limit
    (3) Add closing '*/'
    """
    for outfile in Path(".").rglob("*.out"):
        out_text = adjust_lines(outfile.read_text())
        phase_1 = outfile.with_suffix(".p1")
        with phase_1.open('w') as phs1:
            phs1.write(fill_to_width(out_text) + "\n")
            errfile = outfile.with_suffix(".err")
            if errfile.exists():
                phs1.write("___[ Error Output ]___\n")
                phs1.write(fill_to_width(errfile.read_text()) + "\n")
            phs1.write("*/\n")


########### Chain of Responsibility Match Finder #######################

memlocation = re.compile("@[0-9a-z]{5,7}")
datestamp1 = re.compile(
    "(?:[MTWFS][a-z]{2} ){0,1}[JFMASOND][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2} [A-Z]{3} \d{4}")
datestamp2 = re.compile(
    "[JFMASOND][a-z]{2} \d{1,2}, \d{4} \d{1,2}:\d{1,2}:\d{1,2} (:?AM|PM)")

def exact_match(text): return text

def ignore_memory_addresses_and_dates(text):
    for pat in [ memlocation, datestamp1, datestamp2 ]:
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

# Fairly extreme but will still reveal significant changes
def unique_words(input_text):
    return "\n".join(sorted(set(input_text.split())))

# Fairly extreme but will still reveal significant changes
word_only = re.compile("[A-Za-z]+")
def words_only(input_text):
    return "\n".join(
        sorted([w for w in input_text.split()
                if word_only.fullmatch(w)]))

def no_match(input_text): return True

# Chain of responsibility:
strategies = [
    # Filter                               Retain result for rest of chain
    (exact_match,                           False),
    (ignore_memory_addresses_and_dates,     True ),
    (ignore_digits,                         False),
    (sort_lines,                            False),
    (sort_words,                            False),
    (unique_lines,                          False),
    (unique_words,                          False),
    (words_only,                            False),
    (no_match,                              False),
]


class Validator(defaultdict): # Map of lists
    def __init__(self):
        super().__init__(list)

    def find_output_match(self, javafile, code_output, generated_output):
        def write_comparison_file(strat_name):
            with javafile.with_suffix("." + strat_name).open('w') as trace_file:
                trace_file.write(str(code_output) + "\n\n")
                trace_file.write("=== Actual ===\n\n")
                trace_file.write(str(generated_output))
        for strategy, retain in strategies:
            filtered_code_output = strategy(code_output)
            filtered_generated_output = strategy(generated_output)
            if filtered_code_output == filtered_generated_output:
                strat_name = strategy.__name__
                self[strat_name].append(str(javafile))
                if strat_name is "exact_match": return
                write_comparison_file(strat_name)
                return
            if retain:
                code_output = filtered_code_output
                generated_output = filtered_generated_output

    @staticmethod
    def header(id, log):
        if id is "exact_match": return
        log.write("\n" + (" " + id + " ").center(45, "=") + "\n")

    def display_results(self):
        log = open("verified_output.txt", 'w')
        for strategy, retain in strategies:
            key = strategy.__name__
            self.header(key, log)
            if key is "exact_match":
                for java in self[key]:
                    print(java)
            elif key in self:
                for java in self[key]:
                    log.write(java + "\n")
        log.close()


if __name__ == '__main__':
    phase1() # Generates '.p1' files
    find_output = re.compile(r"/\* (Output:.*)\*/", re.DOTALL)
    validator = Validator()
    for outfile in Path(".").rglob("*.p1"):
        javafile = outfile.with_suffix(".java")
        if not javafile.exists():
            print(str(outfile) + " has no javafile")
            sys.exit(1)
        javatext = javafile.read_text()
        if "/* Output:" not in javatext:
            print(str(outfile) + " has no /* Output:")
            sys.exit(1)
        validator.find_output_match(javafile,
            find_output.search(javatext).group(0).strip(),
            outfile.read_text().strip())
    validator.display_results()
    os.system("more verified_output.txt")
