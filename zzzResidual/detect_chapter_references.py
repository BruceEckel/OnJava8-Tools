from pathlib import Path
import sys
import shutil
import config
import re
import os

def say(str):
    try:
        print(str)
    except:
        print(str.encode("utf-8"))


printed = []
def print_once(arg):
    if arg in printed:
        return
    printed.append(arg)
    print(arg)

pat = re.compile("\*[A-Z](?:(?:\w+)\s*)+?\*")

if __name__ == '__main__':
    flag = False
    print("starting")
    for md in config.markdown_dir.glob("[0-9][0-9]_*.md"):
        # if str(md).endswith("28_Patterns.md"):
        #     flag = True
        #     continue
        # if str(md).endswith("30_Appendix_Programming_Guidelines.md"):
        #     continue
        # if str(md).endswith("45_Appendix_Benefits_and_Costs_of_Static_Type_Checking.md"):
        #     continue
        # if not flag:
        #     continue
        # print(md)
        # for r in pat.findall(md.read_text(encoding="utf-8")):
        #     print(r)
        lines = md.read_text(encoding="utf-8").splitlines()
        for n, line in enumerate(lines):
            if "this appendix" in line or "This appendix" in line:
                continue
            if "appendix" in line:
                print_once(md.name)
                say(lines[n-1])
                say(lines[n])
                say(lines[n+1])
                print("=" * 60)
                os.system("subl {}:{}".format(md, n+1))


        # lines = md.read_text(encoding="utf-8")
        # .splitlines()
        # for n, line in enumerate(lines):
        #     try:
        #         if "* appendix" in line:
        #             print_once(md.name)
        #             # say(lines[n-1])
        #             # say(line)
        #             # say(lines[n+1])
        #             # print("=" * 60)
        #             os.system("subl {}:{}".format(md, n+1))
        #     except:
        #         continue
            # if re.match("={6,}", line) or re.match("-{6,}", line):
            #     if re.search("\d+", lines[n-1]):
            #         continue
            #     if not re.search("\w+", lines[n-1]):
            #         continue
            #     if len(line) != len(lines[n-1]):
            #         os.system("subl {}:{}".format(md, n))