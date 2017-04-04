#! /usr/bin/env python

import admin_tasks
import logging
import tar_utility
import multi_logging
import settings
import sys
from optparse import OptionParser
from backup import Backup
from download import Download


if __name__ == '__main__':

	usage = '''
	%prog --app <jira|bamboo|bitbucket|crowd> --file <filename>.json [options] 

	Backup Example
	--------------
	%prog --app jira --config /tmp/jira.json -bs
	'''
	parser = OptionParser(usage=usage)

 	parser.add_option("-a", "--app", dest="app", type='choice', choices=['jira','bitbucket','bamboo','crowd'],
                  help="Specify app name")
	parser.add_option("-f", "--file", dest="file", help="Specify config file path")
	parser.add_option("-b", action="store_true", dest="backup",help="Backup application. Must use with shutdown flag.")
	parser.add_option("-p", action="store_true", dest="process",help="Check application process")
	parser.add_option("-s", action="store_true", dest="shutdown",help="Shutdown application")
	parser.add_option("-d", action="store_true", dest="download",help="Download deployment files")

	(options, args) = parser.parse_args()


	if options.app and options.file:
		app_name = options.app
		log 	 = logging.getLogger('atlassian-admin-tools')
		config   = settings.get_config(options.file)
		

		if options.backup and options.shutdown:

				backup   = Backup(config,log)
				backup.create_backup_dir()
				log.debug("Backup working directory is %s" % backup.backup_working_dir)
				log.debug("Shutting down %s application" % app_name)
				cmd_output = admin_tasks.manage_service(app_name,'stop')
				if cmd_output:
						log.debug('Getting application process data')
						log.info('Application service has been shutdown')
						print("Command output: \n" + cmd_output)
				else:
						log.info('Application service shutdown failed')

				# Drop privileges to 'proteus' user
				admin_tasks.change_user()

				backup.backup_app()
				backup.summary()
				

		elif options.download:
				download = Download(config,log)
				download.download_files()
				download.summary()

		

		elif options.process:
			log.debug('Getting application process data')
			cmd_output = admin_tasks.get_process(app_name)
			if cmd_output:
				log.info('Application process is running')
				print("Command output: \n" + cmd_output)
			else:
				log.info('Application process is not running')
		else:
			parser.print_help()




