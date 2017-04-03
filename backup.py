#! /usr/bin/env python
import admin_tasks
import tar_utility


class Backup(object):

	def __init__(self,config,log):
		self.backup_working_dir = config['base_backup_dir'] +'/'+ config['CRQ']
		self.temp_dir 			= config['temp_dir']
		self.backups 			= config['backups']
		self.downloads          = config['downloads']
		self.log 				= log


	def create_backup_dir(self):
		if admin_tasks.make_dirs(self.backup_working_dir):
			admin_tasks.set_ownership(self.backup_working_dir)	
			


	def backup_app(self):
		
		for backup_metadata in self.backups:
			for data in backup_metadata.itervalues():
				
				dest_file = self.backup_working_dir + '/' + data['tar_file']
				tar_utility.create_tar(
					dest_file,
					data['parent_dir'],
					data['backup_dir'])
				
				if self.log: self.log.info("File Details: %s " % admin_tasks.get_file_details(dest_file))		


	
	def download_files(self):

		for download_metadata in self.downloads:
			for link in download_metadata.itervalues():
			
				if link:
					file_path = self.temp_dir + '/' + admin_tasks.get_filename(link)
					admin_tasks.download(link,self.temp_dir)				
					if self.log: self.log.info("File details: %s " % admin_tasks.get_file_details(file_path))


if __name__ == '__main__':
	pass