#! /usr/bin/env python

'''
How to log to file and standard output
'''

import logging

logger = logging.getLogger('multi_logging')
logger.setLevel(logging.DEBUG)

# Create a file handler which logs DEBUG messages
file_handler = logging.FileHandler('sample.log')
file_handler.setLevel(logging.DEBUG)

# Create a console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Add formatter to handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


if __name__ == '__main__':

	# 'application' code
	logger.debug('debug message')
	logger.info('info message')
	logger.warn('warn message')
	logger.error('error message')
	logger.critical('critical message')