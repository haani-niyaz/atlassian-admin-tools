#! /usr/bin/env python

import admin_tasks
import logging
import tar_utility
import simplejson as json
import multi_logging

if __name__ == '__main__':

	log = logging.getLogger('atlassian-admin-tools')

	try:
		fh = open('/tmp/jira.json','r')
		config = json.load(fh)
		fh.close()

	except IOError, e:
		log.error('Unable to read yaml file: ' + str(e))
	else:

		# Create backup path

		backup_working_dir = config['base_backup_dir'] +'/'+ config['CRQ']
		
		if admin_tasks.make_dirs(backup_working_dir):
			admin_tasks.set_ownership(backup_working_dir)

		# Backup directories

		log.debug("Backup working directory is %s" % backup_working_dir)


		for backup_metadata in config['backups']:
			for data in backup_metadata.itervalues():
				
				dest_file = backup_working_dir + '/' + data['tar_file']
				tar_utility.create_tar(
					dest_file,
					data['parent_dir'],
					data['backup_dir'])


		for download_metadata in config['downloads']:
			for link in download_metadata.itervalues():
				
				if link:
					file_path = config['temp_dir'] + '/' + 	admin_tasks.get_filename(link)

					if admin_tasks.download(link,config['temp_dir']):				
						admin_tasks.set_ownership(file_path)

		# Check process 
		ps_result = admin_tasks.get_process('sshd')

		if ps_result:
			log.debug('Getting application process data')
			print(ps_result)
			log.info('Application prcoess is running')
		else:
			log.error('Application process is not running')



