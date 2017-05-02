# Check the .out files resulting from 'gradlew run'
'''
Intended to be copied into the ExtractedExamples directory,
thus it doesn't use config.py
'''
import pprint
from pathlib import Path

base = "/* Output:"
example_dir = Path(".")

if __name__ == '__main__':
    output_lines = set()
    for md in example_dir.glob("**/*.out"):
        output_ln = md.read_text().splitlines()[0]
        output_lines.add(output_ln)
        if(not output_ln.startswith(base)):
            print(str(md.relative_to(example_dir)))
        if output_ln.strip() != base:
            print(str(md.relative_to(example_dir)))
            print(output_ln)
    pprint.pprint(output_lines)
