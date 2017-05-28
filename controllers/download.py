#!/usr/bin/env python

"""Orchestrate download tasks"""

import sys

from utils import admin_tasks


def get_active_elements(elements):
    """Returns a dict of elements where value is not 'None'"""

    active_elements = {}
    for key, value in elements.iteritems():
        if value:
            active_elements[key] = value

    return active_elements


class DownloadController(object):
    """Download operations control flow"""

    def __init__(self, config, log):

        self.temp_dir = config['temp_dir']
        self.downloads = get_active_elements(config['downloads'])
        self.log = log
        self.files_downloaded = []

    def download_files(self):
        """Manages control flow to download files.
            If a download failure occurs, terminate program with a
            non-zero exit code.
        """

        total = len(self.downloads)

        for index, link in enumerate(self.downloads.itervalues()):
            self.log.info("Downloading %s of %s.." % (index+1, total))

            file_path = self.temp_dir + '/' + admin_tasks.get_filename(link)

            try:
                admin_tasks.download(link, self.temp_dir)
            except admin_tasks.AdminTasksError, e:
                self.log.error(str(e))
                sys.exit(1)
            else:
                self.files_downloaded.append(file_path)
                self.log.info("File details: %s " %
                              admin_tasks.get_file_details(file_path))

    def summary(self):
        """Download summary"""

        self.log.info("-- Download Summary --")
        for file_path in self.files_downloaded:
            self.log.info(admin_tasks.get_file_details(file_path))
