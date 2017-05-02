# Check for .out files that don't contain an "/* Output:"" line
import config
import pprint
base = "/* Output:"

if __name__ == '__main__':
    output_lines = set()
    for md in config.example_dir.glob("**/*.out"):
        output_ln = md.read_text().splitlines()[0]
        output_lines.add(output_ln)
        if(not output_ln.startswith(base)):
            print(str(md.relative_to(config.example_dir)))
        if output_ln.strip() != base:
            print(str(md.relative_to(config.example_dir)))
            print(output_ln)
    pprint.pprint(output_lines)
