#!/usr/bin/env python

"""Orchestrate backup tasks"""

import sys

from utils import admin_tasks
from utils import tar_utility


class BackupController(object):
    """Backup operations control flow"""

    def __init__(self, base_backup_dir, backup_items, crq, log):

        self.backup_working_dir = base_backup_dir + '/' + crq
        self.backup_dirs = backup_items['dirs']
        self.backup_files = backup_items['files']
        self.log = log
        self.files_downloaded = []
        self.files_backed_up = []

    def create_backup_dir(self):
        """Create backup directory and set ownership to default user
            If a failure occurs, termnaite program with a non-zero exit
            code.
        """

        try:
            admin_tasks.make_dirs(self.backup_working_dir)
            admin_tasks.set_ownership(self.backup_working_dir)
        except admin_tasks.AdminTasksError, e:
            self.log.error(str(e))
            sys.exit(1)

    def backup_app(self):
        """Manages control flow to backup application (install) directory
            and sets file permissions. If a failure occurs,
            termnaite program with a non-zero exit code.
        """

        for index, backup_metadata in enumerate(self.backup_dirs):
            for data in backup_metadata.itervalues():
                self.log.info("Backing up directory %s of %s.." %
                              (index+1, len(self.backup_dirs)))

                dest_file = self.backup_working_dir + '/' + data['tar_file']

                try:
                    tar_utility.create_tar(
                        dest_file,
                        data['parent_dir'],
                        data['backup_dir'])
                except tar_utility.TarUtilityError, e:
                    self.log.error(str(e))
                    sys.exit(1)

                try:
                    admin_tasks.set_permissions(dest_file, 0400)
                except admin_tasks.AdminTasksError, e:
                    self.log.error(str(e))
                    sys.exit(1)

                # Create a list for output summary
                self.files_backed_up.append(dest_file)
                self.log.info("File Details: %s " %
                              admin_tasks.get_file_details(dest_file))

    def backup_config(self):
        """Manages control flow to backup sensitive config files
            and sets file permissions. If a failure occurs,
            termnaite program with a non-zero exit code.
        """

        for index, files_metadata in enumerate(self.backup_files):
            for file_name, source_path in files_metadata.iteritems():

                dest_file = self.backup_working_dir + '/' + file_name
                self.log.info("Backing up config file %s of %s.." %
                              (index+1, len(self.backup_files)))

                try:
                    admin_tasks.copy_file(source_path, dest_file)
                    admin_tasks.set_permissions(dest_file, 0400)
                except admin_tasks.AdminTasksError, e:
                    self.log.error(str(e))
                    sys.exit(1)
                else:
                    # Create a list for output summary
                    self.files_backed_up.append(dest_file)
                    self.log.info("File Details: %s " %
                                  admin_tasks.get_file_details(dest_file))

    def summary(self):
        """Backup summary"""

        self.log.info("-- Backup Summary --")
        for file_path in self.files_backed_up:
            self.log.info(admin_tasks.get_file_details(file_path))
