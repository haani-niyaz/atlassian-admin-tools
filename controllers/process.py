#!/usr/bin/env python

import sys

from utils import admin_tasks


class ProcessController(object):
    """Controller responsible for handling all OS process operations"""

    def __init__(self, log, app_name=None):
        self.log = log
        self.app_name = app_name

    def get_process(self):
        self.log.debug('Getting application process data')
        cmd_output = admin_tasks.get_process(self.app_name)
        if cmd_output:
            self.log.info('Application process is running')
            print("Command output: \n" + cmd_output)
        else:
            self.log.error('Application process is not running')

    def shutdown(self):
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
        stats = admin_tasks.df_stats(fs)
        if stats:
            size, used, available = stats
            # Remove metric from output
            available = float(available[:-1])
            space_left = available - required_disk_space

            if space_left > 0.5:
                self.log.info("%sG of disk space is available from %sG in %s" %
                              (required_disk_space, available, fs))
            elif space_left >= 0 and space_left <= 0.5:
                self.log.warning("Low disk space. Only %sG will be free from available space of %sG in %s." % (
                    space_left, available, fs))
            else:
                self.log.error("Not enough disk space. %sG is not available from avaiable space of %sG in %s." % (
                    required_disk_space, available, fs))
                sys.exit(1)

    def package_info(self, package, repo):
        cmd_output = admin_tasks.yum_info(package, repo)
        if cmd_output:
            self.log.info("%s package exists" % package)
            print("Command output: \n" + cmd_output)
        else:
            self.log.error("%s package was not found" % package)
            sys.exit(1)
