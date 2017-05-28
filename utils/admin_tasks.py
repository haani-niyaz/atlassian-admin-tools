
#!/usr/bin/env python

"""System admin tasks
"""

import os
import errno
import urllib2
import logging
import subprocess
import pwd
from shutil import copyfile


LOG = logging.getLogger('atlassian-admin-tools')


class AdminTasksError(Exception):
    """An exception that occurs when performing administrative operations"""
    pass


def make_dirs(dirs):
    """Create directories recursively"""

    try:
        LOG.debug("Creating %s directory" % (dirs))
        os.makedirs(dirs)
    except OSError, e:
        if e.errno == errno.EEXIST:
            LOG.info("%s Directory already exists", dirs)
        else:
            raise AdminTasksError(
                "Backup directory creation failed with error %s" % str(e))


def change_user(user):
    """Chage to specified user"""

    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = pwd.getpwnam(user).pw_gid
        os.setegid(uid)
        os.seteuid(gid)
        LOG.debug("Running commands as %s user", user)
    except KeyError, e:
        raise AdminTasksError(
            "Changing to user \'%s\' failed with error %s" % (user, str(e)))


def set_ownership(path, user='proteus'):
    """Set ownership of file"""

    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = pwd.getpwnam(user).pw_gid

        LOG.debug("Setting %s ownership to %s:%s " % (path, user, user))
        os.chown(path, uid, gid)
    except KeyError, e:
        raise AdminTasksError(
            "Setting ownership failed with error %s", str(e))


def set_permissions(path, permissions):
    """Set file permissions

    Args:
        path         : Path to file
        permissions  : permissions are set as octal integer. Python automagically treats any
                       integer with a leading zero as octal.
    Returns:
        None
    Raises:
        AdminTaskError: Raise for OSError to be handled in controller
    """
    try:
        LOG.debug("Setting permissions %s for file %s" % (oct(permissions), path))
        os.chmod(path, permissions)
    except OSError, e:
        raise AdminTasksError(
            "Changing permissions failed with error %s" % str(e))


def get_filename(path):
    """Return the filename from given path"""
    return os.path.basename(path)


def download(url, path):
    """Download files to destination path from source url"""

    os.chdir(path)

    file_name = get_filename(url)

    if not os.path.exists(file_name):
        try:
            resp = urllib2.urlopen(url)
            try:
                fh = open(file_name, 'wb')
                fh.write(resp.read())
                LOG.info("Downloaded %s to %s" % (file_name, path))
            finally:
                fh.close()
        except (urllib2.URLError, urllib2.HTTPError), e:
            raise AdminTasksError("Download from \'%s\' failed with %s" % (url, str(e)))
    else:
        LOG.info("%s already exists", file_name)


def run_cmd(cmd):
    """Executed shell command

    Returns:
        STDOUT of successful command execution
    """

    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate()[0]
    # Wait for process to terminate before getting return code
    p.wait()
    if p.returncode == 0:
        return output.rstrip("\n")
    return False


def get_process(name):
    """Get application process output

    Returns:
        STDOUT
    """

    cmd = "/bin/bash -c \"ps -ef | grep -v grep | grep java | grep %s \" " % name
    return run_cmd(cmd)


def get_file_details(path):
    """List file details

    Returns:
        STDOUT
    """

    cmd = "ls -lah %s" % path
    return run_cmd(cmd)


def manage_service(name, operation):
    """Start/Status/Stop service

    Returns:
        STDOUT
    """

    cmd = "/bin/bash -c  \"/sbin/service %s %s \" " % (name, operation)
    return run_cmd(cmd)


def yum_clean(repo):
    """Clean yum repo

    Returns:
        STDOUT
    """
    if os.path.exists("/etc/yum.repos.d/%s.repo" % repo):
        cmd = "/bin/bash -c  \"yum --disablerepo=* --enablerepo=%s clean all\" " % repo
        return run_cmd(cmd)

    return False


def yum_info(package, repo):
    """Get RPM package info

    Returns:
        STDOUT
    """

    if yum_clean(repo):
        cmd = "/bin/bash -c  \"yum --disablerepo=* --enablerepo=%s  info %s\" " % (
            repo, package)
        return run_cmd(cmd)

    LOG.error('Yum clean failed. Please check repo and retry.')
    return False


def df_stats(fs):
    """Get volume size, used and available space

    Returns:
        List: volume size, used and available space
    """

    # Return output in KB
    # Why not get in GB? because it is rounded up i.e: instead of 5.5GB you
    # get 6GB.
    cmd = "df -B KB -P %s" % fs
    haystack = run_cmd(cmd)
    stats = haystack.split("\n")[1].split()[1:4]
    if stats:
        # Remove 'KB' from return values and convert to GB
        stats_in_gb = [float(stat[:-2])/1024**2 for stat in stats]
        return stats_in_gb
    return False


def copy_file(source_file, dest_file):
    """Copy file from source to destination"""

    if os.path.exists(dest_file):
        LOG.warn("%s already exists", dest_file)
    else:
        try:
            copyfile(source_file, dest_file)
            LOG.info("Backup of %s is done", dest_file)
        except OSError, e:
            raise AdminTasksError(
                "Copy operation failed with error %s" % str(e))
