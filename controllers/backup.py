#! /usr/bin/env python

import sys
import os
from utils import admin_tasks
from utils import tar_utility


class BackupController(object):

    def __init__(self, config, log):
        self.backup_working_dir = config[
            'base_backup_dir'] + '/' + config['CRQ']
        self.temp_dir           = config['temp_dir']
        self.backup_dirs        = config['backup']['dirs']
        self.backup_files       = config['backup']['files']
        self.downloads          = config['downloads']
        self.log                = log
        self.files_downloaded   = []
        self.files_backed_up    = []

    def create_backup_dir(self):
        if admin_tasks.make_dirs(self.backup_working_dir):
            admin_tasks.set_ownership(self.backup_working_dir)

    def backup_app(self):

        for index, backup_metadata in enumerate(self.backup_dirs):
            for data in backup_metadata.itervalues():
                self.log.info("Backing up directory %s of %s.." %
                              (index+1, len(self.backup_dirs)))

                dest_file = self.backup_working_dir + '/' + data['tar_file']
                tar_utility.create_tar(
                    dest_file,
                    data['parent_dir'],
                    data['backup_dir'])

                admin_tasks.set_permissions(dest_file, 0400)
                # Create a list to output summary
                self.files_backed_up.append(dest_file)
                self.log.info("File Details: %s " %
                              admin_tasks.get_file_details(dest_file))

    def backup_config(self):
        for index, files_metadata in enumerate(self.backup_files):
            for file_name, source_path in files_metadata.iteritems():

                dest_file = self.backup_working_dir + '/' + file_name
                self.log.info("Backing up config file %s of %s.." %
                              (index+1, len(self.backup_files)))

                if admin_tasks.copy_file(source_path, dest_file):
                    self.log.info("Backup of %s is done" % dest_file)

                admin_tasks.set_permissions(dest_file, 0400)
                # Create a list to output summary
                self.files_backed_up.append(dest_file)
                self.log.info("File Details: %s " %
                              admin_tasks.get_file_details(dest_file))

    def summary(self):
        self.log.debug("-- Backup Summary --")
        for file_path in self.files_backed_up:
            self.log.info(admin_tasks.get_file_details(file_path))


if __name__ == '__main__':
    pass
