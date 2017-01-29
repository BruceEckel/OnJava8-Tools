#! py -3
"""
Create abbreviated sample of On Java 8
"""
# import logging
# from logging import debug
# logging.basicConfig(filename= __file__.split('.')[0] + ".log", filemode='w', level=logging.DEBUG)
from pathlib import Path
import sys
import os
import re
import shutil
import pprint
import difflib
from enum import Enum
from betools import CmdLine
import config
from ebook_build import *

Include = Enum('Include', 'ALL')

cutoffs = {
"00_Front.md" : Include.ALL,
"01_Preface.md" : Include.ALL,
"02_Introduction.md" : Include.ALL,
"03_What_is_an_Object.md" : Include.ALL,
"04_Installing_Java_and_the_Book_Examples.md" : Include.ALL,
"05_Objects_Everywhere.md" : Include.ALL,
"06_Operators.md" :  Include.ALL,
"07_Control_Flow.md" : Include.ALL,

"08_Housekeeping.md" :
"""
No-arg Constructors
-------------------
""",

"09_Implementation_Hiding.md" :
"""
### Creating Unique Package Names
""",

"10_Reuse.md" :
"""
### Initializing the Base Class
""",

"11_Polymorphism.md" :
"""
### Forgetting the Object Type
""",

"12_Interfaces.md" :
"""
Interfaces
----------
""",

"13_Inner_Classes.md" :
"""
Using `.this` and `.new`
------------------------
""",

"14_Collections.md" :
"""
Adding Groups of Elements
-------------------------
""",

"15_Functional_Programming.md" :
"""
Method References
-----------------
""",

"16_Streams.md" :
"""
### Random Number Streams
""",

"17_Exceptions.md" :
"""
Creating Your Own Exceptions
----------------------------
""",

"18_Validating_Your_Code.md" :
"""
### The Illusion of Test Coverage
""",

"19_Files.md" :
"""
### Selecting Pieces of a `Path`
""",

"20_Strings.md" :
"""
Unintended Recursion
--------------------
""",

"21_Type_Information.md" :
"""
### Class Literals
""",

"22_Generics.md" :
"""
### A Stack Class
""",

"23_Arrays.md" :
"""
Arrays are First-Class Objects
------------------------------
""",

"24_Enumerations.md" :
"""
`enum`s in `switch` Statements
------------------------------
""",

"25_Annotations.md" :
"""
### Meta-Annotations
""",

"26_Concurrent_Programming.md" :
"""
Concurrency is for Speed
------------------------
""",

"27_Patterns.md" :
"""
### Classifying Patterns
""",

"28_Appendix_Supplements.md" : Include.ALL,

"29_Appendix_Programming_Guidelines.md" :
"""
Implementation
--------------
""",

"30_Appendix_Passing_and_Returning_Objects.md" :
"""
Making Local Copies
-------------------
""",

"31_Appendix_IO_Streams.md" :
"""
Types of `InputStream`
----------------------
""",

"32_Appendix_Standard_IO.md" :
"""
### Changing `System.out` to a `PrintWriter`
""",

"33_Appendix_New_IO.md" :
"""
Converting Data
---------------
""",

"34_Appendix_Understanding_equals_and_hashCode.md" :
"""
A Canonical `equals()`
----------------------
""",

"35_Appendix_Collection_Topics.md" :
"""
`List` Behavior
---------------
""",

"36_Appendix_Low_Level_Concurrency.md" :
"""
Catching Exceptions
-------------------
""",

"37_Appendix_Data_Compression.md" :
"""
Simple Compression with GZIP
----------------------------
""",

"38_Appendix_Object_Serialization.md" :
"""
Finding the Class
-----------------
""",

"39_Appendix_Preferences.md" : Include.ALL,

"40_Appendix_Network_Programming.md" :
"""
#### Testing Programs Without a Network
""",

"41_Appendix_Remote_Methods.md" :
"""
Implementing the Remote Interface
---------------------------------
""",

"42_Appendix_Benefits_and_Costs_of_Static_Type_Checking.md" :
"""
Static Type Checking vs. Testing
--------------------------------
""",

"43_Appendix_The_Positive_Legacy_of_CPP_and_Java.md" : Include.ALL,

"44_Appendix_Becoming_a_Programmer.md" :
"""
A Career in Computing
---------------------
""",

}


@CmdLine("c")
def clean():
    "Remove SampleBook directory"
    remove_dir(config.sample_book_dir)


@CmdLine("r")
def createRawMaterial():
    if not config.sample_book_original_dir.exists():
        config.sample_book_dir.mkdir(exist_ok=True)
        config.sample_book_original_dir.mkdir()

    if not config.markdown_dir.exists():
        print("Cannot find", config.markdown_dir)
        sys.exit()

    for sourceText in config.markdown_dir.glob("*.md"):
        #print("copying {}".format(sourceText.name))
        shutil.copy(sourceText, config.sample_book_original_dir)

    ensure_ebook_build_dir(config.sample_book_dir)


def extract_headings(text):
    result = ""
    lines = text.splitlines()
    for n, line in enumerate(lines):
        if re.match(r"^[=-]+$", line):
            heading = lines[n-1]
            highbound = len(heading) + 2
            lowbound = len(heading) - 2
            borderlen = len(line)
            if borderlen <= highbound and borderlen >= lowbound:
                result += "\n"
                result += heading + "\n"
                result += line + "\n"
        if re.match(r"^#{2,5} ", line):
            result += "\n"
            result += line + "\n"
    return result


@CmdLine("p")
def process():
    "Convert copied files"

    """
    1. Find specified subhead (don't need regexp for this)
    2. From that point on, strip everything except subheads
    3. Add message saying "End of sample for this chapter"
    """
    # changes = [c for c in config.sample_book_original_dir.glob("*.md")
    #             if cutoffs[c.name] is not Include.ALL]
    for chapter in config.sample_book_original_dir.glob("*.md"):
        if cutoffs[chapter.name] is Include.ALL:
            print("copying {}".format(chapter.name))
            shutil.copy(chapter, config.sample_book_dir)
            continue
        # if not cutoffs[chapter.name].strip():
        #     os.system("subl {}".format(chapter))
        #     sys.exit()
        print("modifying {}".format(chapter.name))
        divider = cutoffs[chapter.name]
        parts = chapter.read_text().split(divider)
        result = parts[0] + divider + extract_headings(parts[1])
        (config.sample_book_dir / chapter.name).write_text(result)


@CmdLine('f')
def fresh():
    "Create fresh sample book"
    clean()
    createRawMaterial()
    process()
    combine_markdown_files(config.sample_book_dir, config.combined_markdown_sample)
    convert_to_epub(config.sample_book_dir, config.epub_sample_file_name)


if __name__ == '__main__':
    CmdLine.run()
