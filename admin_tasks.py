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


if __name__ == '__main__':
	pass

