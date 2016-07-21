# Find .out files that also have .err files
import config

if __name__ == '__main__':
    for md in config.example_dir.glob("**/*.out"):
        errfile = md.with_suffix(".err")
        if errfile.exists():
            print("=" * 50)
            print(str(md.relative_to(config.example_dir)))
            print(md.read_text())
            print("-" * 50)
            print(str(errfile.relative_to(config.example_dir)))
            print(errfile.read_text())

