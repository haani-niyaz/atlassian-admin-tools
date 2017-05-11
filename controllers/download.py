#!/usr/bin/env python

import sys

from utils import admin_tasks


class DownloadController(object):
    """Controller responsible for handling all download operations"""

    def __init__(self, config, log):

        self.temp_dir = config['temp_dir']
        self.downloads = self._get_active_elements(config['downloads'])
        self.log = log
        self.files_downloaded = []

    def _get_active_elements(self, elements):
        """Returns a dict of elements where value is not None"""

        active_elements = {}
        for key, value in elements.iteritems():
            if value:
                active_elements[key] = value

        return active_elements

    def download_files(self):

        total = len(self.downloads)

        for index, link in enumerate(self.downloads.itervalues()):
            self.log.info("Downloading %s of %s.." % (index+1, total))
            file_path = self.temp_dir + '/' + admin_tasks.get_filename(link)
            if admin_tasks.download(link, self.temp_dir):
                self.files_downloaded.append(file_path)
                self.log.info("File details: %s " %
                              admin_tasks.get_file_details(file_path))
            else:
                sys.exit(1)

    def summary(self):
        self.log.debug("-- Download Summary --")
        for file_path in self.files_downloaded:
            self.log.info(admin_tasks.get_file_details(file_path))
