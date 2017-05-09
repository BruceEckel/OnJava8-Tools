# Requires Python 3.5 or greater
from pathlib import Path
import sys
import re
import textwrap

memlocation = re.compile("@[0-9a-z]{5,7}")
datestamp1 = re.compile("(?:[MTWFS][a-z]{2} ){0,1}[JFMASOND][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2} [A-Z]{3} \d{4}")
datestamp2 = re.compile("[JFMASOND][a-z]{2} \d{1,2}, \d{4} \d{1,2}:\d{1,2}:\d{1,2} (:?AM|PM)")

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

chain_of_responsibility = [
    # Filter                               Retain result for rest of chain
    (exact_match,                           False),
    (ignore_memory_addresses_and_dates,     True ),
    (ignore_digits,                         False),
    (sort_lines,                            False),
    (sort_words,                            False),
    (unique_lines,                          False),
    (unique_words,                          False),
    (words_only,                            False),
]


def find_match(code_output, generated_output):
    for strategy, retain in chain_of_responsibility:
        filtered_code_output = strategy(code_output)
        filtered_generated_output = strategy(generated_output)
        if filtered_code_output == filtered_generated_output:
            return strategy.__name__
        if retain:
            code_output = filtered_code_output
            generated_output = filtered_generated_output
    else:
        return None
