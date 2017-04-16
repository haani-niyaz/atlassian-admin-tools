#! /usr/bin/env python

# Append to module path
sys.path.append(os.path.join(
    os.path.dirname(sys.path[0]), 'utils'))

import cmd_options
import logging
import multi_logging
import admin_tasks
import settings
from backup import Backup
from download import Download
from process import Process


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

        # Show help if app name and config file has been provided but no
        # switch
        else:
            parser.print_help()

    elif options.disk_space:
        Process(log).check_disk_space(options.disk_space)

    elif options.package_name:
        if args:
            Process(log).package_info(options.package_name, args[0])
        else:
            parser.print_help()

    # show help if app name has been provied but no config file and/or switch
    # has been set
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
