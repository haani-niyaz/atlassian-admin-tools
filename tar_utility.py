#! /usr/bin/env python

import tarfile, os
import logging


def log():
	logger = logging.getLogger('atlassian-admin-tools')
	return logger


def check_if_exists(tarfile_dest):
	return os.path.isfile(tarfile_dest)

'''
Example:
Create tar files from:
1. Install directory /opt/atlassian/jira
2. Home directory /mnt/jira/jira-home
3. Temp directory /mnt/jira/jira-temp
'''


def create_tar(tarfile_dest, root_dir, tar_file):
	'''
	Create a tar file
	'''

	if check_if_exists(tarfile_dest):
		log_str = '{} already exists'.format(tarfile_dest)
		log().warn(log_str)
		# print log_str
		return None

	
	log().info('Creating tar file for {} in root dir {} and store in {}'.format(tar_file, root_dir, tarfile_dest))		
	with tarfile.open(tarfile_dest, 'w:gz') as tar:
		os.chdir(root_dir)
		try:
			tar.add(tar_file)
			log.info('Tar file creation successful')		
		except OSError as e:
			log().error('Tar file creation failed with error: ' + str(e))
			log()
			print e



def extract_tar(root_dir, tar_file):
	'''
	Extract tar file inside root dir
	'''

	try:
		log().info('Extract tar file {} into {} directory'.format(tar_file, root_dir))	
		tar = tarfile.open(tar_file)
		tar.extractall(path=root_dir)
		tar.close()
	except OSError as e:
		print e
	except IOError as e:
		print e


if __name__ == '__main__':

	# Test with fake directory
	# create_tar('/tmp/jira-installdir.tar.gz','/opt/atlassian','bogus')

	tar_utility.create_tar('/tmp/jira-installdir.tar.gz','/opt/atlassian','jira')

	# extract_tar('/var/tmp', '/tmp/jira-installdir.tar.gz')








