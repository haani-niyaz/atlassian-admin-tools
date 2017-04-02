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



		backup_working_dir = config['base_backup_dir'] +'/'+ config['CRQ']
		temp_dir = config['temp_dir']
		
		if admin_tasks.make_dirs(backup_working_dir):
			admin_tasks.set_ownership(backup_working_dir)

		# Backup directories

		log.debug("Backup working directory is %s" % backup_working_dir)

		# Drop privileges to 'proteus' user
		admin_tasks.change_user()

		for backup_metadata in config['backups']:
			for data in backup_metadata.itervalues():
				
				dest_file = backup_working_dir + '/' + data['tar_file']
				tar_utility.create_tar(
					dest_file,
					data['parent_dir'],
					data['backup_dir'])
				
				log.info("File Details: %s " % admin_tasks.get_file_details(dest_file))

		# Drop privileges to 'root' user		
		# admin_tasks.change_user('root')		
				
		for download_metadata in config['downloads']:
			for link in download_metadata.itervalues():
				
				if link:
					file_path = config['temp_dir'] + '/' + 	admin_tasks.get_filename(link)
					admin_tasks.download(link,config['temp_dir'])				
					log.info("File details: %s " % admin_tasks.get_file_details(file_path))

		# Check process 
		ps_output = admin_tasks.get_process('sshd')

		if ps_output:
			log.debug('Getting application process data')
			log.info(ps_output)
			log.info('Application process is running')
		else:
			log.error('Application process is not running')


