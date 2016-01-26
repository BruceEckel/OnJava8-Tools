# py -3
"""
Open sublime text at line that is too wide
"""
# from pathlib import Path
import os
import config

assert config.build_dir.exists()
assert config.combined_markdown.exists(), "RUN b -s first"


def check_listing_widths():
    "Make sure listings don't exceed max width of %d" % config.code_width
    in_listing = False
    for n, line in enumerate(config.combined_markdown.read_text(encoding="utf-8").splitlines()):
        if line.startswith("```java"):
            in_listing = True
            continue
        if line.startswith("```"):
            in_listing = False
            continue
        if in_listing and len(line)  > config.code_width:
            print("{}: {}".format(n, line))
            os.system("subl {}:{}".format(config.combined_markdown, n + 1))
            return


if __name__ == '__main__':
    check_listing_widths()