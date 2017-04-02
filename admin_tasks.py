#! /usr/bin/env python

'''
Admin tasks to run as sudo
'''

import os
import errno
import urllib2
import logging
import subprocess
import pwd
import re

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
	

def change_user(user='proteus'):
	uid = pwd.getpwnam(user).pw_uid
	gid = pwd.getpwnam(user).pw_gid
	os.setegid(uid)
	os.seteuid(gid)
	log.debug("Running commands as %s" % user)


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


def get_process(name):
	p  = subprocess.Popen("ps -fC " + name,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output = p.communicate()[0]
	if re.search(name,output):
		return output
	return False

def get_file_details(path):
	return subprocess.Popen(['ls', '-lah', path], stdout=subprocess.PIPE).communicate()[0]


if __name__ == '__main__':
	pass

