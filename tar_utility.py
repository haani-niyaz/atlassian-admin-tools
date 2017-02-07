#! /usr/bin/env python

import tarfile, os, logging





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
		logging.info(log_str)
		print log_str
		return None

	
	logging.info('Creating tar file for {} in root dir {} and stre in {}'.format(tar_file, root_dir, tarfile_dest))		
	with tarfile.open(tarfile_dest, 'w:gz') as tar:
		os.chdir(root_dir)
		try:
			tar.add(tar_file)	
		except OSError as e:
			logging.error('Tar file creation faile with error: ' + str(e))
			print e



def extract_tar(root_dir, tar_file):
	'''
	Extract tar file inside root dir
	'''

	try:
		logging.info('Extract tar file {} into {} directory'.format(tar_file, root_dir))	
		tar = tarfile.open(tar_file)
		tar.extractall(path=root_dir)
		tar.close()
	except OSError as e:
		print e
	except IOError as e:
		print e



if __name__ == '__main__':

	logging.basicConfig(filename='tar_events.log', level=logging.DEBUG)

	# Test with fake directory
	# create_tar('/tmp/jira-installdir.tar.gz','/opt/atlassian','bogus')

	# create_tar('/tmp/jira-installdir.tar.gz','/opt/atlassian','jira')


	extract_tar('/var/tmp', '/tmp/jira-installdir.tar.gz')







