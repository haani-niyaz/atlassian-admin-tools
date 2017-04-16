#! /usr/bin/env python

from os import getuid
from sys import exit

if getuid() != 0:
    print("Invalid usage. Script must be executed as a privileged user i.e: sudo ./run.py <options>")
    exit(1)

import admin_tasks
import logging
import tar_utility
import multi_logging
import settings
from optparse import OptionParser, OptionGroup
from backup import Backup
from download import Download
from process 


if __name__ == '__main__':

    usage = """
    sudo ./%prog <option>
    sudo ./%prog <command> <option>
    sudo ./%prog <command>  <sub-command> <option>


examples:
    sudo ./%prog -u 1                                 # Check if 1GB of disk space is available in /opt
    sudo ./%prog --app jira -p                        # Check application process status          
    sudo ./%prog --app jira --file /tmp/jira.json -bs # Shutdown application and perform backup
    """

    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--space-required", dest="disk_space", type=float,
                      help="Check for free disk space. Specify in GBs. i.e: 1 for 1GB")
    parser.add_option("-i", "--package-info", 
                           dest="package_name", help="Specify rpm package name with REPO_NAME as an argument")

    app_options = OptionGroup(parser, 'Application operations',
                              'Format: sudo ./run --app <name> <option>')
    app_options.add_option("-a", "--app", dest="app", type='choice', choices=['jira', 'bitbucket', 'bamboo', 'crowd'],
                           help="Specify app name")
    app_options.add_option("-s", "--shut-down", action="store_true",
                           dest="shutdown", help="Shutdown application")
    app_options.add_option("-p", "--status", action="store_true", dest="process",
                           help="Check application process status")
    parser.add_option_group(app_options)

    config_file_options = OptionGroup(
        parser, 'Configuration file operations', 'Format: sudo ./run --app <name> --file <path> <option>')
    config_file_options.add_option("-f", "--file", dest="file",
                                   help="Specify config file path")
    config_file_options.add_option("-b", action="store_true", dest="backup",
                                   help="Backup application. Must use with shutdown option.")
    config_file_options.add_option("-d", action="store_true",
                                   dest="download", help="Download deployment files")

    parser.add_option_group(config_file_options)

    (options, args) = parser.parse_args()

    log = logging.getLogger('atlassian-admin-tools')

    if options.app:
        # Initialize if a valid app name is provided
        app_name = options.app

        if options.file:
            # Initialize if config file provided and valid
            config = settings.get_config(options.file)

            # backup, shutdown, process check can run if app_name and config file has been
            # initialized

            # Backup requires shutdown option
            if options.backup and options.shutdown:

                backup = Backup(config, log)
                backup.create_backup_dir()
                log.debug("Backup working directory is %s" %
                          backup.backup_working_dir)
                is_shutdown = Process(log, app_name).shutdown()
                if is_shutdown:
                    # Drop privileges to 'proteus' user
                    admin_tasks.change_user()

                    backup.backup_app()
                    backup.backup_config()
                    backup.summary()

            elif options.download:
                download = Download(config, log)
                download.download_files()
                download.summary()

            else:
                parser.print_help()

        # Options can run without config file
        elif options.process:
            Process(log, app_name).get_process()

        elif options.shutdown:
            Process(log, app_name).shutdown()

        # Show help if app name and config file has been provided but no switch
        else:
            parser.print_help()

    elif options.disk_space:
        Process(log).check_disk_space(options.disk_space)

    elif options.package_name:
        if args:
            Process(log).package_info(options.package_name,args[0])
        else:
            parser.print_help()

    # show help if app name has been provied but no config file and/or switch
    # has been set
    else:
        parser.print_help()
