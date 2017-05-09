from pathlib import Path
import sys
import config
import os

command = "start /B linkchecker --check-extern -F text /{}-linkcheck.txt {}.xhtml"

def check_links_batch_file():
    bat = config.epub_dir / "check_links.bat"
    with bat.open("w") as batfile:
      for xhtml in config.epub_dir.glob("*.xhtml"):
          print(command.format(xhtml.stem,xhtml.stem))
          print(command.format(xhtml.stem,xhtml.stem), file=batfile)

if __name__ == '__main__':
    check_links_batch_file()