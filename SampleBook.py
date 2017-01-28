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
from betools import CmdLine
import config

cutoffs = {
"00_Front.md" :
"",

"01_Preface.md" :
"",

"02_Introduction.md" :
"",

"03_What_is_an_Object.md" :
"",

"04_Installing_Java_and_the_Book_Examples.md" :
"",

"05_Objects_Everywhere.md" :
"",

"06_Operators.md" :
"",

"07_Control_Flow.md" :
"",

"08_Housekeeping.md" :
"",

"09_Implementation_Hiding.md" :
"",

"10_Reuse.md" :
"",

"11_Polymorphism.md" :
"",

"12_Interfaces.md" :
"",

"13_Inner_Classes.md" :
"",

"14_Collections.md" :
"",

"15_Functional_Programming.md" :
"",

"16_Streams.md" :
"",

"17_Exceptions.md" :
"",

"18_Validating_Your_Code.md" :
"",

"19_Files.md" :
"",

"20_Strings.md" :
"",

"21_Type_Information.md" :
"",

"22_Generics.md" :
"",

"23_Arrays.md" :
"",

"24_Enumerations.md" :
"",

"25_Annotations.md" :
"",

"26_Concurrent_Programming.md" :
"",

"27_Patterns.md" :
"",

"28_Appendix_Supplements.md" :
"",

"29_Appendix_Programming_Guidelines.md" :
"",

"30_Appendix_Passing_and_Returning_Objects.md" :
"",

"31_Appendix_IO_Streams.md" :
"",

"32_Appendix_Standard_IO.md" :
"",

"33_Appendix_New_IO.md" :
"",

"34_Appendix_Understanding_equals_and_hashCode.md" :
"",

"35_Appendix_Collection_Topics.md" :
"",

"36_Appendix_Low_Level_Concurrency.md" :
"",

"37_Appendix_Data_Compression.md" :
"",

"38_Appendix_Object_Serialization.md" :
"",

"39_Appendix_Preferences.md" :
"",

"40_Appendix_Network_Programming.md" :
"",

"41_Appendix_Remote_Methods.md" :
"",

"42_Appendix_Benefits_and_Costs_of_Static_Type_Checking.md" :
"",

"43_Appendix_The_Positive_Legacy_of_CPP_and_Java.md" :
"",

"44_Appendix_Being_a_Programmer.md" :
"",

}


@CmdLine("c")
def clean():
    "Remove SampleBook directory"
    print("Cleaning ...")
    try:
        if config.sample_book.exists():
            shutil.rmtree(str(config.sample_book))
    except:
        print("Error: could not remove {}".format(config.sample_book))
        sys.exit(1);


@CmdLine("x")
def copyRawMaterial():
    if not config.sample_book.exists():
        # debug("creating {}".format(config.sample_book))
        config.sample_book.mkdir()

    if not config.markdown_dir.exists():
        print("Cannot find", config.markdown_dir)
        sys.exit()

    for sourceText in config.markdown_dir.glob("*.md"):
        print("copying {}".format(sourceText.name))
        shutil.copy(sourceText, config.sample_book)


@CmdLine("p")
def process():
    "Convert copied files"

    """
    1. Find specified subhead (don't need regexp for this)
    2. From that point on, strip everything except subheads
    3. Add message saying "End of sample for this chapter"
    """


@CmdLine('f')
def fresh():
    "Create fresh sample book"
    clean()
    copyRawMaterial()


if __name__ == '__main__':
    CmdLine.run()
