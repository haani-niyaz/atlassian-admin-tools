#! /usr/bin/env python

import tarfile, os, logging




'''
Example:
Create tar files from:
1. Install directory /opt/atlassian/jira
2. Home directory /mnt/jira/jira-home
3. Temp directory /mnt/jira/jira-temp
'''


def create_tar(tarfile_dest, root_dir, tar_dir):
	'''
	Create a tar file
	'''
	
	with tarfile.open(tarfile_dest, 'w:gz') as tar:
		os.chdir(root_dir)
		try:
			tar.add(tar_dir)	
		except OSError as e:
			print e




if __name__ == '__main__':

	logging.basicConfig(filename='tar_events.log', level=logging.DEBUG)












