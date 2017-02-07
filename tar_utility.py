#! /usr/bin/env python

import tarfile, os, logging




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
	
	logging.info('Creating tar file for {} in root dir {} and stre in {}'.format(tar_file, root_dir, tarfile_dest))		
	with tarfile.open(tarfile_dest, 'w:gz') as tar:
		os.chdir(root_dir)
		try:
			tar.add(tar_file)	
		except OSError as e:
			logging.error('Tar file creation faile with error: ' + str(e))
			print e



if __name__ == '__main__':

	logging.basicConfig(filename='tar_events.log', level=logging.DEBUG)

	# Test with fake directory
	# create_tar('/tmp/jira-installdir.tar.gz','/opt/atlassian','bogus')











