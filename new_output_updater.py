# Requires Python 3.5 or greater
"""
Updates output for selected example, directly into markdown file.
"""
import sys
from pathlib import Path
from output_duet import Duet, Valid
import config

def say(str):
    return
    try:
        print(str)
    except:
        print(str, encoding="utf-8")

def new_replace_output(markdown, duet):
    lines = markdown.splitlines()

    def find_string(x, str):
        for ln in range(x, len(lines)):
            if lines[ln].startswith(str):
                say("line {}: {}".format(ln, lines[ln]))
                return ln

    slug_n = find_string(0, duet.java_slugline)
    fence = find_string(slug_n, "```")
    start = find_string(slug_n, "/* Output:") + 1
    end = find_string(start, "*/")
    assert end < fence
    lines[start:end] = duet.new.splitlines()
    return ("\n".join(lines)).strip()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: u output-file-to-update-with")
        sys.exit()
    assert sys.argv[1].endswith(".new")
    duet = Duet(Path(sys.argv[1]))
    if not duet.new:
        print("no duet.new in {}".format(sys.argv[1]))
        sys.exit()
    print(duet.java_slugline)
    for f in config.markdown_dir.glob("*.md"):
        contents = f.read_text(encoding="utf-8")
        if duet.java_slugline in contents:
            print("Found in", contents.splitlines()[0])
            contents = new_replace_output(contents, duet)
            f.write_text(contents + "\n", encoding="utf-8")
            break
    else:
        print("Not found!", duet.java_slugline)