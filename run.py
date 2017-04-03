#! /usr/bin/env python

import admin_tasks
import logging
import tar_utility
import multi_logging
import settings
import sys
import backup


if __name__ == '__main__':

	log 	= logging.getLogger('atlassian-admin-tools')
	config  = settings.get_config('jira')
	backup  = backup.Backup(config,log)
	

	backup.create_backup_dir()
	log.debug("Backup working directory is %s" % backup.backup_working_dir)

	# Drop privileges to 'proteus' user
	admin_tasks.change_user()

	backup.backup_app()
	backup.download_files()

	# Check process 
	ps_output = admin_tasks.get_process('jira')

	if ps_output:
		log.debug('Getting application process data')
		log.info('Application process is running')
		print("Process output: \n" + ps_output)
	else:
		log.error('Application process is not running')

	log.debug(" [SUMMARY] ")
	for file_path in backup.files_downloaded:
		log.info(admin_tasks.get_file_details(file_path))

	for file_path in backup.files_backed_up:
		log.info(admin_tasks.get_file_details(file_path))




