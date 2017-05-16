# Make sure all subdirectories can be compiled independently (that the gradle dependencies are
# correct). Runs gradlew clean, then gradle subdirectory:compileJava for each subdirectory.
import os
import sys
from subprocess import call
from pathlib import Path
import config

assert config.example_dir.exists() 

exclude = [
    ".gradle",
    "gradle",
    "buildSrc",
]


def gradle(arg):
    leader_length = 10
    leader = "*" * leader_length
    cmd = "gradlew {}".format(arg)
    print("{} Running {} {}".format(leader, cmd, leader))
    if os.system(cmd) != 0:
        print("{} {} FAILED {}".format(leader, cmd, leader))
        sys.exit(1)
    print("{} {} Succeeded {}".format(leader, cmd, leader))

# Look in base directory only:
for dir in [d for d in config.example_dir.glob("*") if d.is_dir() and d.name not in exclude]:
    os.chdir(config.example_dir)
    gradle('clean')
    gradle("{}:compileJava".format(dir.name))
        