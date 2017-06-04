#!/usr/bin/env python

"""Application behaviour"""

import logging
import sys

from core import cmd_options
from core import multi_logging
from core import settings
from controllers.backup import BackupController
from controllers.download import DownloadController
from controllers.process import ProcessController


LOG = logging.getLogger('atlassian-admin-tools')


def invoke():
    """App logic"""

    # Setup option parser
    parser = cmd_options.main()
    (options, args) = parser.parse_args()

    help_msg = "run 'sudo bin/run.py --help' to see detailed usage instructions"

    # Initialize logging to stdout and file
    multi_logging.main()

    if options.app:
        # Initialize if a valid app name is provided
        app_name = options.app

        if options.file:
            # Initialize if config file provided is valid
            try:
                config = settings.read_config_file(options.file)
            except settings.ConfigFileError, e:
                LOG.error(str(e))
                sys.exit(1)

            # Backup requires shutdown option
            if options.backup and options.shutdown:

                backup = BackupController(config['base_backup_dir'], config['backup'],
                                          config['CRQ'], LOG)
                backup.create_backup_dir()
                LOG.debug("Backup working directory is %s",
                          backup.backup_working_dir)

                ProcessController(LOG, app_name).shutdown()

                # Drop privileges to application user
                ProcessController(LOG).switch_to_app_user('proteus')

                backup.backup_app()
                backup.backup_config()
                backup.summary()

            elif options.download:

                download = DownloadController(config, LOG)
                download.download_files()
                download.summary()

            elif options.keep:

                backup = BackupController(config['base_backup_dir'], config['rollback'],
                                          config['CRQ'], LOG)
                backup.create_backup_dir()
                LOG.debug("Backup working directory is %s",
                          backup.backup_working_dir)

                if options.shutdown:
                    ProcessController(LOG, app_name).shutdown()

                # Drop privileges to application user
                ProcessController(LOG).switch_to_app_user('proteus')

                backup.backup_app()
                backup.summary()

            else:
                parser.error(help_msg)

        # Options that can run without config file

        elif options.process:
            ProcessController(LOG, app_name).get_process()

        elif options.shutdown:
            ProcessController(LOG, app_name).shutdown()

        # Error if app name and config file has been provided but no
        # switch
        else:
            parser.error(help_msg)

    elif options.disk_space:
        ProcessController(LOG).check_disk_space(options.disk_space)

    elif options.package_name:
        if args:
            ProcessController(LOG).package_info(
                options.package_name, args[0])
        else:
            # Error if package name has been provided but no repo
            parser.error(help_msg)
    elif options.file:
        parser.error(help_msg)

    # show help
    else:
        parser.print_help()
