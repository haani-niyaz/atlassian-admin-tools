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
from process import Process


if __name__ == '__main__':

    usage = '''
    sudo %prog --app <jira|bamboo|bitbucket|crowd> --file <filename>.json [options] 

    Backup Example
    --------------
    sudo %prog --app jira --file /tmp/jira.json -bs
    '''
    parser = OptionParser(usage=usage)

    parser.add_option("-a", "--app", dest="app", type='choice', choices=['jira','bitbucket','bamboo','crowd'],
                  help="Specify app name")
    parser.add_option("-f", "--file", dest="file", help="Specify config file path")
    parser.add_option("-r", "--repo", dest="repo", help="Specify yum repo")
    parser.add_option("-b", action="store_true", dest="backup",help="Backup application. Must use with shutdown flag.")
    parser.add_option("-p", action="store_true", dest="process",help="Check application process")
    parser.add_option("-s", action="store_true", dest="shutdown",help="Shutdown application")
    parser.add_option("-d", action="store_true", dest="download",help="Download deployment files")


    (options, args) = parser.parse_args()


    if options.app:
        # Initialize if a valid app name is provided
        app_name = options.app
        log      = logging.getLogger('atlassian-admin-tools')

        if options.file:
            # Initialize if config file provided and valid
            config  = settings.get_config(options.file)
        
            # backup, shutdown, process check can run if app_name and config file has been
            # initialized

            # Backup requires shutdown option
            if options.backup and options.shutdown:

                    backup = Backup(config,log)
                    backup.create_backup_dir()
                    log.debug("Backup working directory is %s" % backup.backup_working_dir)
                    is_shutdown = Process(app_name,log).shutdown()
                    if is_shutdown:
                        # Drop privileges to 'proteus' user
                        admin_tasks.change_user()

                        backup.backup_app()
                        backup.summary()

            elif options.download:
                download = Download(config,log)
                download.download_files()
                download.summary()
            
            elif options.process:
                Process(app_name,log).get_process()

            elif options.repo:
                Process(app_name,log).clean_repo(options.repo)

            else:
                parser.print_help()

        # Process check can run without config file     
        elif options.process:
            Process(app_name,log).get_process()
        

        elif options.repo:
            Process(app_name,log).clean_repo(options.repo)


        elif options.capacity:
            Process(app_name,log).check_disk_capacity(options.capacity)
            
        # Show help if app name and config file has been provided but no switch 
        else:
            parser.print_help()

    # show help if app name has been provied but no config file and/or switch 
    # has been set
    else:
        parser.print_help()




