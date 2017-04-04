#! /usr/bin/env python
import admin_tasks


class Process(object):

	def __init__(self,app_name,log):
		self.app_name = app_name
		self.log = log


	def get_process(self):
		self.log.debug('Getting application process data')
		cmd_output = admin_tasks.get_process(self.app_name)
		if cmd_output:
			self.log.info('Application process is running')
			print("Command output: \n" + cmd_output)
		else:
			self.log.info('Application process is not running')

	def shutdown(self):
		self.log.debug("Shutting down %s application" % self.app_name)
		cmd_output = admin_tasks.manage_service(self.app_name,'stop')
		if cmd_output:
				self.log.debug('Getting application process data')
				self.log.info('Application service has been shutdown')
				print("Command output: \n" + cmd_output)
		else:
				self.log.warning('Application service shutdown failed')		



if __name__ == '__main__':
	pass