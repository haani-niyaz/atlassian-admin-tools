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


def show_process(name):
	return subprocess.Popen(['ps', 'ww', '-fC', name], stdout=subprocess.PIPE).communicate()[0]


if __name__ == '__main__':
	pass

