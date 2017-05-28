#!/usr/bin/env python

"""Orchestrate OS-based tasks"""

import sys

from utils import admin_tasks


class ProcessController(object):
    """OS-based operations control flow"""

    def __init__(self, log, app_name=None):
        self.log = log
        self.app_name = app_name

    def get_process(self):
        """Report on process status"""

        self.log.debug('Getting application process data')
        cmd_output = admin_tasks.get_process(self.app_name)
        if cmd_output:
            self.log.info('Application process is running')
            print("Command output: \n" + cmd_output)
        else:
            self.log.error('Application process is not running')

    def shutdown(self):
        """Manages control flow to shut down application process.
            if shutdown fails, terminate with a non-zero exit code.
        """

        self.log.debug("Shutting down %s application" % self.app_name)
        cmd_output = admin_tasks.manage_service(self.app_name, 'stop')
        if cmd_output:
            self.log.debug('Getting application process data')
            self.log.info('Application service has been shutdown')
            print("Command output: \n" + cmd_output)
        else:
            self.log.error('Application service shutdown failed')
            sys.exit(1)

    def check_disk_space(self, required_disk_space, fs='/opt'):
        """Manages control flow to check if requires disk space 
            is available. If disk space required is unavailable, 
            terminate program with a non-zero exit code.
        """

        stats = admin_tasks.df_stats(fs)
        if stats:
            __, __, available = stats

            space_left = available - required_disk_space

            if space_left > 0.5:
                self.log.info("%.1fG of disk space is available from approximately %.1fG in %s" %
                              (required_disk_space, available, fs))
            elif space_left > 0 and space_left <= 0.5:
                self.log.warning("Low disk space. Only %.1fG will be free from approximately available space of %.1fG in %s." % (
                    space_left, available, fs))
            else:
                self.log.error("Not enough disk space. %.1fG is not available from approximately avaiable space of %.1fG in %s." % (
                    required_disk_space, available, fs))
                sys.exit(1)

    def package_info(self, package, repo):
        """Manages control flow to verify if package exists.
            If package is not found, termnate with a non-zero 
            exit code.
        """

        cmd_output = admin_tasks.yum_info(package, repo)
        if cmd_output:
            self.log.info("%s package exists" % package)
            print("Command output: \n" + cmd_output)
        else:
            self.log.error("%s package was not found" % package)
            sys.exit(1)

    def switch_to_app_user(self, user):
        """Manages control flow to switch user.
            If changing user fails, terminate with a non-zero exit
            code.
        """
        try:
            admin_tasks.change_user(user)
        except admin_tasks.AdminTasksError, e:
            self.log.error(str(e))
            sys.exit(1)
