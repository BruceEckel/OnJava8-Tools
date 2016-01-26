from pathlib import Path
import sys
import shutil
import config
import re
import os

oldlist = config.rootPath / "Checklist.txt"
newlist = config.rootPath / "new-Checklist.txt"

if __name__ == '__main__':
    with newlist.open('w') as checklist:
        for md in config.markdown_dir.glob("[0-9][0-9]_*.md"):
            item = md.name[3:-3]
            item = item.replace("Appendix_", "Appendix: ")
            item = item.replace("_", " ")
            item = "[ ]  " + item
            print(item, file=checklist)
    os.system("subl " + str(newlist))
    os.system("subl " + str(oldlist))