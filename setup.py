#! /usr/bin/env python

import cmd_options
import logging
import multi_logging
from utils import admin_tasks
import settings
from controllers import backup as bkp
from controllers import download as dl
from controllers import process


def main():

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
            config = settings.get_config(options.file)

            # backup, shutdown, process check can run if app_name and config file has been
            # initialized

            # Backup requires shutdown option
            if options.backup and options.shutdown:

                backup = bkp.BackupController(config, log)
                backup.create_backup_dir()
                log.debug("Backup working directory is %s" %
                          backup.backup_working_dir)
                is_shutdown = process.ProcessController(log, app_name).shutdown()
                if is_shutdown:
                    # Drop privileges to 'proteus' user
                    admin_tasks.change_user()

                    backup.backup_app()
                    backup.backup_config()
                    backup.summary()

            elif options.download:
                download = dl.DownloadController(config, log)
                download.download_files()
                download.summary()

            else:
                parser.print_help()

        # Options can run without config file
        elif options.process:
            process.ProcessController(log, app_name).get_process()

        elif options.shutdown:
            process.ProcessController(log, app_name).shutdown()

        # Show help if app name and config file has been provided but no
        # switch
        else:
            parser.print_help()

    elif options.disk_space:
        process.ProcessController(log).check_disk_space(options.disk_space)

    elif options.package_name:
        if args:
            process.ProcessController(log).package_info(options.package_name, args[0])
        else:
            parser.print_help()

    # show help if app name has been provied but no config file and/or switch
    # has been set
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
