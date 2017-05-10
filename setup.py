#! /usr/bin/env python

import logging
import sys

from core import cmd_options
from core import multi_logging
from core import settings
from utils import admin_tasks
from controllers.backup import BackupController
from controllers.download import DownloadController
from controllers.process import ProcessController


def invoke():

    # Setup option parser
    parser = cmd_options.main()
    (options, args) = parser.parse_args()

    # Initialize logging to stdout and file
    multi_logging.main()

    log = logging.getLogger('atlassian-admin-tools')

    if options.app:
        # Initialize if a valid app name is provided
        app_name = options.app

        if options.file:
            # Initialize if config file provided and valid
            try:
                config = settings.read_config_file(options.file)
            except settings.ConfigFileError, e:
                log.error(str(e))
                sys.exit(1)   

            # backup, shutdown, process check can run if app_name and config file has been
            # initialized

            # Backup requires shutdown option
            if options.backup and options.shutdown:

                backup = BackupController(config, log)
                backup.create_backup_dir()
                log.debug("Backup working directory is %s" %
                          backup.backup_working_dir)
                is_shutdown = ProcessController(
                    log, app_name).shutdown()
                if is_shutdown:
                    # Drop privileges to 'proteus' user
                    admin_tasks.change_user()

                    backup.backup_app()
                    backup.backup_config()
                    backup.summary()

            elif options.download:
                download = DownloadController(config, log)
                download.download_files()
                download.summary()

            else:
                parser.print_help()

        # Options can run without config file
        elif options.process:
            ProcessController(log, app_name).get_process()

        elif options.shutdown:
            ProcessController(log, app_name).shutdown()

        # Show help if app name and config file has been provided but no
        # switch
        else:
            parser.print_help()

    elif options.disk_space:
        ProcessController(log).check_disk_space(options.disk_space)

    elif options.package_name:
        if args:
            ProcessController(log).package_info(
                options.package_name, args[0])
        else:
            parser.print_help()

    # show help if app name has been provied but no config file and/or switch
    # has been set
    else:
        parser.print_help()


