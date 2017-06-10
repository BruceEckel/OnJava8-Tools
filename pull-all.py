import os
import sys
from pathlib import Path

if 'GIT_HOME' not in os.environ:
    print("You need to set 'GIT_HOME' as an environment variable")
    sys.exit(1)

gitdirs = [x for x in Path(os.environ['GIT_HOME']).iterdir() if x.is_dir()]

for gd in gitdirs:
    print(gd)
    os.chdir(gd)
    os.system("git pull")


