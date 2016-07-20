# Check for .out files that don't contain an "/* Output:"" line
import config
base = "/* Output:"

if __name__ == '__main__':
    for md in config.example_dir.glob("**/*.out"):
        if(not md.read_text().splitlines()[0].startswith(base)):
            print(str(md.relative_to(config.example_dir)))
