#! /usr/bin/env python

from utils import admin_tasks


class DownloadController(object):

    def __init__(self, config, log):
        self.temp_dir = config['temp_dir']
        self.downloads = self._get_active_elements(config['downloads'])
        self.log = log
        self.files_downloaded = []

    def _get_active_elements(self, list_dicts):
        """ Store dict objects where value is not None 
            Returns a dictionary 
        """
        active_elements = {}
        for dict_obj in list_dicts:
            for key, value in dict_obj.iteritems():
                if value:
                    active_elements[key] = value

        return active_elements

    def download_files(self):

        total = len(self.downloads)

        for index, link in enumerate(self.downloads.itervalues()):
            self.log.info("Downloading %s of %s.." % (index+1, total))
            file_path = self.temp_dir + '/' + \
                admin_tasks.get_filename(link)
            admin_tasks.download(link, self.temp_dir)
            self.files_downloaded.append(file_path)
            if self.log:
                self.log.info("File details: %s " %
                              admin_tasks.get_file_details(file_path))

    def summary(self):
        self.log.debug("-- Download Summary --")
        for file_path in self.files_downloaded:
            self.log.info(admin_tasks.get_file_details(file_path))


if __name__ == '__main__':
    pass
