import os, sys
from pathlib import Path

def create_run_file():
    arg = sys.argv[1]
    # if arg.endswith(".class") or arg.endswith(".java") or arg.endswith(".out"):
    #     base = arg.rsplit('.')[0]
    # else:
    #     print("Argument must be a .class or .java file name")
    #     sys.exit()
    base = arg.rsplit('.')[0]
    print(base)
    Path("run.bat").write_text("java %s | tee %s" % (base, base + ".out"))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: runjava PublicClassName")
        sys.exit()
    create_run_file()