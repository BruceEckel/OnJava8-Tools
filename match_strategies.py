# Requires Python 3.5 or greater
from pathlib import Path
import sys
import re
import textwrap

datestamp1 = re.compile("(?:[MTWFS][a-z]{2} ){0,1}[JFMASOND][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2} [A-Z]{3} \d{4}")
datestamp2 = re.compile("[JFMASOND][a-z]{2} \d{1,2}, \d{4} \d{1,2}:\d{1,2}:\d{1,2} (:?AM|PM)")

def trim(block):
    trimmed = "\n".join([ln.rstrip() for ln in block.splitlines()])
    return trimmed.strip()

memlocation = re.compile("@[0-9a-z]{5,7}")
def ignore_memory_addresses(input_text):
    return trim(memlocation.sub("", input_text))

def ignore_digits(input_text):
    return trim(re.sub("-?\d", "", input_text))

def ignore_digits_and_memory_addresses(input_text):
    return ignore_memory_addresses(
        ignore_digits(input_text))

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
    ignore_memory_addresses,
    ignore_digits,
    ignore_digits_and_memory_addresses,
    sort_lines,
    sort_words,
    unique_lines,
    unique_words,
    words_only,
]

def find_strategy(code_output, generated_output):
    for strategy in chain_of_responsibility:
        if strategy(code_output) == strategy(generated_output):
            return strategy.__name__
    else:
        return None


if __name__ == '__main__':
    for strategy in chain_of_responsibility:
        print(strategy.__name__)

# match_adjustments = {
#     "ToastOMatic.java" : sort_lines,
#     "ThreadVariations.java" : sort_lines,
#     "ActiveObjectDemo.java" : [sort_lines, ignore_digits],
#     "Interrupting.java" : sort_lines,
#     "SyncObject.java" : sort_lines,
#     "UseCaseTracker.java" : sort_lines,
#     "AtUnitComposition.java" : sort_lines,
#     "AtUnitExample1.java" : sort_lines,
#     "AtUnitExample2.java" : sort_lines,
#     "AtUnitExample3.java" : sort_lines,
#     "AtUnitExample5.java" : sort_lines,
#     "AtUnitExternalTest.java" : sort_lines,
#     "HashSetTest.java" : sort_lines,
#     "StackLStringTest.java" : sort_lines,
#     "WaxOMatic2.java" : sort_lines,

#     "ForEach.java" : sort_words,
#     "PetCount4.java" : [RemoveCharacters("{}"), sort_words],

#     "CachedThreadPool.java" : words_only,
#     "FixedThreadPool.java" : words_only,
#     "MoreBasicThreads.java" : words_only,
#     "ConstantSpecificMethod.java" : words_only,

#     "BankTellerSimulation.java" : [words_only, unique_words],

#     "MapComparisons.java" : ignore_digits,
#     "ListComparisons.java" : ignore_digits,
#     "NotifyVsNotifyAll.java" : ignore_digits,
#     "SelfManaged.java" : ignore_digits,
#     "SimpleMicroBenchmark.java" : ignore_digits,
#     "SimpleThread.java" : ignore_digits,
#     "SleepingTask.java" : ignore_digits,
#     "ExchangerDemo.java" : ignore_digits,
#     "Compete.java" : ignore_digits,
#     "MappedIO.java" : ignore_digits,
#     "Directories.java" : ignore_digits,
#     "Find.java" : ignore_digits,
#     "PathAnalysis.java" : ignore_digits,
#     "TreeWatcher.java" : ignore_digits,
#     "Mixins.java" : ignore_digits,
#     "ListPerformance.java" : ignore_digits,
#     "MapPerformance.java" : ignore_digits,
#     "SetPerformance.java" : ignore_digits,
#     "SynchronizationComparisons.java" : ignore_digits,
#     "AtomicityTest.java" : ignore_digits,
#     "TypesForSets.java" : ignore_digits,
#     "PrintableLogRecord.java" : ignore_digits,
#     "LockingMappedFiles.java" : ignore_digits,


#     "Conversion.java" : IgnoreLines(27, 28),
#     "DynamicProxyMixin.java" : IgnoreLines(2),
#     "PreferencesDemo.java" : IgnoreLines(5),
#     "AtUnitExample4.java" : IgnoreLines(6, 9),

#     "SerialNumberChecker.java" : [ignore_digits, unique_lines],
#     "EvenSupplier.java" : [ignore_digits, unique_lines],

#     "FillingLists.java" : [ ignore_memory_addresses, sort_words ],

#     "SimpleDaemons.java" : [ ignore_memory_addresses, ignore_digits ],
#     "CaptureUncaughtException.java" : [
#         ignore_memory_addresses, ignore_digits, unique_lines ],

#     "CarBuilder.java" : [ ignore_digits, unique_lines ],
#     "CloseResource.java" : [ unique_lines ],

#     "SpringDetector.java" : [ ignore_digits, sort_words ],

#     "PipedIO.java" : [ unique_words ],

#     "CriticalSection.java" : ignore_digits,
#     "ExplicitCriticalSection.java" : ignore_digits,
# }


# translate_file_name = {
#     "ApplyTest.java": "Apply.java",
#     "FillTest.java": "Fill.java",
#     "Fill2Test.java": "Fill2.java",
#     "ClassInInterface$Test.java": "ClassInInterface.java",
#     "TestBed$Tester.java": "TestBed.java",
# }



# class RemoveCharacters(Strategy):
#     def __init__(self, chars_to_remove):
#         self.chars_to_remove = chars_to_remove
#     def filter(self, input_text):
#         for c in self.chars_to_remove:
#             input_text = input_text.replace(c, "")
#         return input_text


# class IgnoreLines(Strategy):
#     def __init__(self, *lines_to_ignore):
#         self.lines_to_ignore = lines_to_ignore
#     def filter(self, input_text):
#         lines = input_text.splitlines()
#         for ignore in sorted(list(self.lines_to_ignore), reverse=True):
#             ignore = ignore - 1 # Compensate for zero indexing
#             print("ignoring line %d: %s" % (ignore, lines[ignore]))
#             del lines[ignore]
#         return "\n".join(lines)


