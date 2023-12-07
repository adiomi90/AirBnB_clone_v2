#!/usr/bin/python3
# A fabfile to delete out-of-date archives.
import os
from fabric.api import *


env.hosts = ["54.173.130.243", "54.165.89.101"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_clean(number=0):
    """Delete outdated archives.
    If number is 0 or 1, keeps only the most recent archive.
    If number is 2, keeps the most and second-most recent archives, etc.

    Args:
        number (int): number of archives to keep.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
