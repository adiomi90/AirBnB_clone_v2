#!/usr/bin/python3
""" A module that generates and distributes an archive to your web server """
from fabric import task, Connection
from time import strftime
from os import path

@task
def do_pack(c):
    """ A fabric function to generate the archive content """
    timestamp = strftime("%Y%m%d%H%M%S")
    try:
        c.local("mkdir -p versions")
        c.local("tar -czvf versions/web_static_{}.tgz web_static/"
                .format(timestamp))

        return "versions/web_static_{}.tgz".format(timestamp)

    except Exception as err:
        return None

@task
def do_deploy(c, archive_path):
    """ A Fabric function to distribute the archive content"""
    if not path.exists(archive_path):
        return False
    try:
        arcfile = archive_path.split("/")[-1]
        fname = arcfile.split(".")[0]
        c.put(archive_path, '/tmp/')
        c.run("mkdir -p /data/web_static/releases/{}/".format(fname))
        c.run("tar -zxvf /tmp/{} -C /data/web_static/releases/{}/"
              .format(arcfile, fname))
        c.run("rm /tmp/{}".format(arcfile))
        c.run("mv /data/web_static/releases/{}/web_static/*"
              " /data/web_static/releases/{}/".format(fname, fname))
        c.run("rm -rf /data/web_static/releases/{}/web_static".format(fname))
        c.run("rm -rf /data/web_static/current")
        c.run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
              .format(fname))
        return True
    except Exception as err:
        return False

@task
def deploy(c):
    """ runs the 2 fabric functions """
    path = do_pack(c)
    if not path:
        return False
    return do_deploy(c, path)

