#!/usr/bin/env python

import sys
import os

# Append project module path
sys.path.append(os.path.dirname(sys.path[0]))

import unittest
from utils import admin_tasks


class TestAdminTasks(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestAdminTasks, self).__init__(*args, **kwargs)
        self.dirs_exist = '/tmp/old'
        self.dirs_new = '/tmp/new'

    def setUp(self):
        if not os.path.exists(self.dirs_exist):
            os.makedirs(self.dirs_exist)

    def testMakeDirsIfExists(self):
        self.assertEqual(admin_tasks.make_dirs(self.dirs_exist), True)

    def testMakeNewDirs(self):
        self.assertEqual(admin_tasks.make_dirs(self.dirs_new), True)

    def teardown():
        os.rmdir(self.dirs_exist)
        os.rmdir(self.dirs_new)

if __name__ == '__main__':
    suite = unittest.makeSuite(TestAdminTasks)
    unittest.TextTestRunner(verbosity=2).run(suite)
