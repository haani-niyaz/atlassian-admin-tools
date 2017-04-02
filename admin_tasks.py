#! /usr/bin/env python

import os
import errno
import urllib2
import logging
import subprocess
import pwd

log = logging.getLogger('atlassian-admin-tools')

def make_dirs(dirs):
	try:
		if not os.path.exists(dirs):
			log.info("Creating %s directory " % dirs)
			os.makedirs(dirs)
			return True
	except 	OSError, e:
		if e.errno != errno.EEXIST:
			raise

	return False

def set_ownership(path,user='proteus'):
	uid = pwd.getpwnam(user).pw_uid
	gid = pwd.getpwnam(user).pw_gid

	log.info("Setting %s ownership to %s:%s " % (path,user,user))
	os.chown(path,uid,gid)


if __name__ == '__main__':
	pass

