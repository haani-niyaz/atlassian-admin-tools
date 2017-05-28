#!/usr/bin/env python

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

    help_msg = "run 'sudo bin/run.py --help' to see detailed usage instructions"

    # Initialize logging to stdout and file
    multi_logging.main()

    log = logging.getLogger('atlassian-admin-tools')

    if options.file:
        parser.error(help_msg)

    elif options.app:
        # Initialize if a valid app name is provided
        app_name = options.app

        if options.file:
            # Initialize if config file provided is valid
            try:
                config = settings.read_config_file(options.file)
            except settings.ConfigFileError, e:
                log.error(str(e))
                sys.exit(1)

            # Backup requires shutdown option
            if options.backup and options.shutdown:

                backup = BackupController(config, log)
                backup.create_backup_dir()
                log.debug("Backup working directory is %s" %
                          backup.backup_working_dir)

                ProcessController(log, app_name).shutdown()

                # Drop privileges to application user
                ProcessController(log).switch_to_app_user('proteus')

                backup.backup_app()
                backup.backup_config()
                backup.summary()

            elif options.download:
                download = DownloadController(config, log)
                download.download_files()
                download.summary()

            else:
                parser.error(help_msg)

        # Options that can run without config file

        elif options.process:
            ProcessController(log, app_name).get_process()

        elif options.shutdown:
            ProcessController(log, app_name).shutdown()

        # Error if app name and config file has been provided but no
        # switch
        else:
            parser.error(help_msg)

    elif options.disk_space:
        ProcessController(log).check_disk_space(options.disk_space)

    elif options.package_name:
        if args:
            ProcessController(log).package_info(
                options.package_name, args[0])
        else:
            # Error if package name has been provided but no repo
            parser.error(help_msg)

    # show help
    else:
        parser.print_help()
