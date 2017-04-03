#! /usr/bin/env python
import simplejson as json


def get_config(app_name):
	file_name = "/tmp/%s.json" % app_name
	# Nesting required to use finally prior python 2.5
	try:
		try:
			fh = open(file_name ,'r')
			config = json.load(fh)
			return config
		except IOError, e:
			log.error('Unable to read yaml file: ' + str(e))
	finally:
		fh.close()