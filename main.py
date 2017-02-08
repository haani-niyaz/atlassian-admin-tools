#! /usr/bin/env python

import multi_logging
import tar_utility


if __name__ == '__main__':

	# Test with fake directory
	# create_tar('/tmp/jira-installdir.tar.gz','/opt/atlassian','bogus')

	tar_utility.create_tar('/tmp/jira-installdir.tar.gz','/opt/atlassian','jira')

	# extract_tar('/var/tmp', '/tmp/jira-installdir.tar.gz')