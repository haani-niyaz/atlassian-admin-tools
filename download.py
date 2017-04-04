#! /usr/bin/env python
import admin_tasks


class Download(object):

	def __init__(self,config,log):
		self.temp_dir 			= config['temp_dir']
		self.downloads          = config['downloads']
		self.log 				= log
		self.files_downloaded   = []

	def count_active_download_items(self,download_list):				
		count = 0
		for items in download_list:
			for val in items.itervalues():
				if val:
					count += 1
		return count

	def download_files(self):
		count = self.count_active_download_items(self.downloads)

		for index, download_metadata in enumerate(self.downloads):
			for link in download_metadata.itervalues():
				if link:
					self.log.info("Downloading %s of %s.." % (index+1,count))
					file_path = self.temp_dir + '/' + admin_tasks.get_filename(link)
					admin_tasks.download(link,self.temp_dir)
					self.files_downloaded.append(file_path)				
					if self.log: self.log.info("File details: %s " % admin_tasks.get_file_details(file_path))

	def summary(self):
		self.log.debug("-- Download Summary --")
		count = self.count_active_download_items(self.downloads)
		for file_path in self.files_downloaded:
			self.log.info(admin_tasks.get_file_details(file_path))
				

if __name__ == '__main__':
	pass