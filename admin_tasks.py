#! /usr/bin/env python

'''
System admin tasks
'''

import os
import errno
import urllib2
import logging
import subprocess
import pwd
import re
from shutil import copyfile

log = logging.getLogger('atlassian-admin-tools')

def make_dirs(dirs):
    try:
        if not os.path.exists(dirs):
            log.info("Creating %s directory " % dirs)
            os.makedirs(dirs)
            return True
    except  OSError, e:
        if e.errno != errno.EEXIST:
            raise

    return False
    
def change_user(user='proteus'):
    uid = pwd.getpwnam(user).pw_uid
    gid = pwd.getpwnam(user).pw_gid
    os.setegid(uid)
    os.seteuid(gid)
    log.debug("Running commands as %s user" % user)

def set_ownership(path,user='proteus'):
    uid = pwd.getpwnam(user).pw_uid
    gid = pwd.getpwnam(user).pw_gid

    log.info("Setting %s ownership to %s:%s " % (path,user,user))
    os.chown(path,uid,gid)


def set_permissions(path,permissions):
    '''
    Set file permissions

    Args:
    @path        : Path to file
    @permissions : permissions are set as octal integer. Python automagically treats any 
                   integer with a leading zero as octal.
    '''
    
    if os.path.exists(path):
        log.info("Setting permissions %s for file %s" % (oct(permissions),path))
        os.chmod(path,permissions)
        return True
    else:
        log.error("File does not exist.")
        return False

def get_filename(url):
    return os.path.basename(url)

def download(url,path):
    
    os.chdir(path)  
    file_name = get_filename(url)
    if not os.path.exists(file_name):
        try:        
            resp = urllib2.urlopen(url)

            try:
                fh = open(file_name,'wb')
                fh.write(resp.read())
                log.info("Downloaded %s to %s", file_name, path)
                return True
            finally:
                fh.close()
        except (urllib2.URLError, urllib2.HTTPError), e:
            log.error("Failed to download %s with error: %s" % (url,str(e)))

    else:
        log.warn("%s already exists." % file_name)

    return False

def run_cmd(cmd):
    p  = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE) 
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
    cmd  = "ls -lah %s" % path
    return run_cmd(cmd)

def manage_service(name,operation):
    cmd = "/bin/bash -c  \"/sbin/service %s %s \" " % (name,operation)
    return run_cmd(cmd)

def yum_clean(repo):
    if os.path.exists("/etc/yum.repos.d/%s.repo" % repo):
        cmd = "/bin/bash -c  \"yum --disablerepo=* --enablerepo=%s clean all\" " % repo
        return run_cmd(cmd)
    else:
        return False

def df_stats(fs):
    cmd  = "df -h -P %s" % fs
    haystack = run_cmd(cmd)
    needle = r'(\d+\.\d+G)'
    stats = re.findall(needle,haystack)
    if stats:
        return stats
    return False

def copy_file(source,dest):
    if os.path.exists(dest):
        log.warn("%s already exists" % dest)
        return None
    elif os.path.exists(source):
        copyfile(source,dest)
        return True
    
    return False

if __name__ == '__main__':
    pass

