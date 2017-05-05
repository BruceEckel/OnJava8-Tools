#! py -3
# Requires Python 3.5
# Updates generated output into extracted Java programs in "On Java 8"
# NOTE: output comes from .p1 files, not from .out files
import sys
from pathlib import Path


def remove_output(javatext):
    result = ""
    for line in javatext.splitlines():
        if "/* Output:" not in line:
            result += line.rstrip() + "\n"
        else:
            return result


def update_file(outfile):
    print(str(outfile))
    javafile = outfile.with_suffix(".java")
    if not javafile.exists():
        print(str(outfile) + " has no javafile")
        sys.exit(1)
    javatext = javafile.read_text()
    if "/* Output:" not in javatext:
        print(str(javafile) + " has no /* Output:")
        sys.exit(1)
    new_output = outfile.read_text()
    new_javatext = remove_output(javatext) + new_output
    javafile.write_text(new_javatext)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        update_file(Path(sys.argv[1]))
    else:
        p1_files = list(Path(".").rglob("*.p1"))
        if len(p1_files) < 10:
            print("Error: found less than 10 .p1 files")
            sys.exit(1)
        for outfile in p1_files: # Note p1 files have been line-wrapped
            print(outfile)
            update_file(outfile)
