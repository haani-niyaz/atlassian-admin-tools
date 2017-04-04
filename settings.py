#! /usr/bin/env python
import simplejson as json


def get_config(file):
	# Nesting required to use finally prior python 2.5
	try:
		try:
			fh = open(file ,'r')
			config = json.load(fh)
			return config
		except IOError, e:
			log.error('Unable to read yaml file: ' + str(e))
	finally:
		fh.close()