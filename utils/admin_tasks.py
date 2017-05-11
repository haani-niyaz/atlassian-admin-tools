#! /usr/bin/env python

"""
System admin tasks
"""

import os
import errno
import urllib2
import logging
import subprocess
import pwd
import re
from shutil import copyfile


log = logging.getLogger('atlassian-admin-tools')


class AdminTasksError(Exception):
    """An error that occurs when performing administrative operations"""
    pass


def make_dirs(dirs):
    """Create directories recursively"""

    try:
        log.debug("Creating %s directory" % dirs)
        os.makedirs(dirs)
    except OSError, e:
        if e.errno == errno.EEXIST:
            log.info("%s Directory already exists" % dirs)
        else:
            raise AdminTasksError(
                "Backup directory creation failed with error %s" % str(e))


def change_user(user='deploy'):

    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = pwd.getpwnam(user).pw_gid
        os.setegid(uid)
        os.seteuid(gid)
        self.log.debug("Running commands as %s user" % user)
    except KeyError, e:
        raise AdminTasksError(
            "Changing to user \'%s\' failed with error %s" % (user,str(e)) )


def set_ownership(path, user='proteus'):

    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = pwd.getpwnam(user).pw_gid

        log.debug("Setting %s ownership to %s:%s " % (path, user, user))
        os.chown(path, uid, gid)
    except KeyError, e:
        raise AdminTasksError(
            "Setting ownership failed with error %s" % str(e))


def set_permissions(path, permissions):
    """Set file permissions

    Args:
        path         : Path to file
        permissions  : permissions are set as octal integer. Python automagically treats any 
                        integer with a leading zero as octal.
    Returns:
        None
    Raises:
        OSError: If file does not exist
    """
    try:
        log.debug("Setting permissions %s for file %s" %
                  (oct(permissions), path))
        os.chmod(path, permissions)
    except OSError, e:
        raise AdminTasksError(
            "Changing permissions failed with error %s" % str(e))


def get_filename(url):
    return os.path.basename(url)


def download(url, path):
    os.chdir(path)
    file_name = get_filename(url)

    if not os.path.exists(file_name):
        try:
            resp = urllib2.urlopen(url)
            try:
                fh = open(file_name, 'wb')
                fh.write(resp.read())
                log.info("Downloaded %s to %s", file_name, path)
                return True
            finally:
                fh.close()
        except (urllib2.URLError, urllib2.HTTPError), e:
            log.error("Failed to download %s with error: %s" % (url, str(e)))
    else:
        log.warn("%s already exists" % file_name)
        return True

    return False


def run_cmd(cmd):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate()[0]
    # Wait for process to terminate before getting return code
    p.wait()
    if p.returncode == 0:
        return output.rstrip("\n")
    return False


def get_process(name):
    cmd = "/bin/bash -c \"ps -ef | grep -v grep | grep java | grep %s \" " % name
    return run_cmd(cmd)


def get_file_details(path):
    cmd = "ls -lah %s" % path
    return run_cmd(cmd)


def manage_service(name, operation):
    cmd = "/bin/bash -c  \"/sbin/service %s %s \" " % (name, operation)
    return run_cmd(cmd)


def yum_clean(repo):
    if os.path.exists("/etc/yum.repos.d/%s.repo" % repo):
        cmd = "/bin/bash -c  \"yum --disablerepo=* --enablerepo=%s clean all\" " % repo
        return run_cmd(cmd)
    else:
        return False


def yum_info(package, repo):
    if yum_clean(repo):
        cmd = "/bin/bash -c  \"yum --disablerepo=* --enablerepo=%s  info %s\" " % (
            repo, package)
        return run_cmd(cmd)
    else:
        log.error('Yum clean failed. Please check repo and retry.')
        return False


def df_stats(fs):
    cmd = "df -h -P %s" % fs
    haystack = run_cmd(cmd)
    needle = r'(\d+\.\d+G)'
    stats = re.findall(needle, haystack)
    if stats:
        return stats
    return False


def copy_file(source_file, dest_file):

    if os.path.exists(dest_file):
        log.warn("%s already exists" % dest_file)
    else:
        try:
            copyfile(source_file, dest_file)
            log.info("Backup of %s is done" % dest_file)
        except OSError, e:
            raise AdminTasksError(
                "Copy operation failed with error %s" % str(e))
