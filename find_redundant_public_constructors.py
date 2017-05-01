import config
import re, os, sys

exclude = [
  "StormyInning",
]

lines = list(enumerate(config.combined_markdown.read_text().splitlines()))

for n, ln in lines:
    if re.match("class\s+[A-Z]", ln.strip()):
        classname = ln.strip().split()[1].strip()
        if classname.endswith(":"):
            continue
        if classname in exclude:
            continue
        classname = classname.split("<")[0]
        for n2, ln2 in lines[n + 1:n + 100]:
            if ln2.strip().startswith("public %s(" % classname):
                os.system("subl {}:{}".format(str(config.combined_markdown), n2 + 1))
                sys.exit()
                # print(">>>> Class:", classname)
                # print(ln2)
