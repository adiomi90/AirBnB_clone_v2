#!/usr/bin/python3
""" A module that distributes an archive to your web server """
from fabric.api import put, run, env
from os import path


env.hosts = ["54.90.63.173", "52.91.134.31"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_deploy(archive_path):
    """ A Fabric function to distribute the archive content"""

    if not path.exists(archive_path):
        return False
    try:
        arcfile = archive_path.split("/")[-1]
        fname = arcfile.split(".")[0]
        put(archive_path, '/tmp/')
        run("mkdir -p /data/web_static/releases/{}/".format(fname))
        run("tar -zxvf /tmp/{} -C /data/web_static/releases/{}/"
            .format(arcfile, fname))
        run("rm /tmp/{}".format(arcfile))
        run("mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".format(fname, fname))
        run("rm -rf /data/web_static/releases/{}/web_static".format(fname))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(fname))
        return True
    except Exception as err:
        return False
