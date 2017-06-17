import os
import sys
from pathlib import Path
import click

if 'GIT_HOME' not in os.environ:
    print("You need to set 'GIT_HOME' as an environment variable")
    sys.exit(1)

gitdirs = [x for x in Path(os.environ['GIT_HOME']).iterdir() if x.is_dir()]

def git_command(cmd):
    for gd in gitdirs:
        print(gd)
        os.chdir(gd)
        os.system("git " + cmd)


@click.group()
def cli():
    """Git-all
    Performs various commands on all repositories in your local directory
    """

@cli.command()
def pull():
    "Pull on all repos"
    git_command("pull")


@cli.command()
def status():
    "Get status of all repos"
    git_command("status -s")

if __name__ == '__main__':
    cli()
