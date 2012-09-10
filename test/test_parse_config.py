#!/usr/bin/env python

import unittest
import os
import logging
import sys

# Setup test files and logs
dir = os.path.dirname(__file__)
log_file = os.path.join(dir, 'unittest/unit-test.log')

# Logging setup
logging.basicConfig(filename=log_file, level=logging.DEBUG)


# TODO: use subprocess.Popen to suppress output instead of using janky os.system
class TestPatentConfig(unittest.TestCase):
    # Make sure that if os.environ['PATENTROOT'] is set, then we parse it correctly
    # if it is nonexistant/incorrect, then recover
    # if it is not set, then we default to /data/patentdata/patents

    def setUp(self):
        # make sure we can call parse.py using the os module
        # for the purpose of testing command line arguments
        current_directory = os.getcwd()
        if not current_directory.endswith('test'):
            logging.error('Please run from the patentprocessor/test directory')
        # need a default value for later tests
        self.assertTrue(os.environ.has_key('PATENTROOT'))
        os.chdir('..')

    def test_argparse_patentroot(self):
        # test that argparse is setting the variables correctly for patentroot
        exit_status = os.system('python parse.py --patentroot %s' % (os.getcwd() + '/test/unittest/fixtures'))
        # valid directory, but no xml files
        self.assertTrue(exit_status == 0)

        exit_status = os.system('python parse.py --patentroot /asdf')
        # specify invalid directory, should not have any files, but still pass
        self.assertTrue(exit_status == 0)

        # test a working, valid directory
        exit_status = os.system('python parse.py --patentroot %s' % (os.environ['PATENTROOT']))
        # this should pass
        self.assertTrue(exit_status == 0)

    def test_argparse_regex(self):
        # test that argparse is setting the regular expression correctly
        # test valid regex on unittest/fixtures folder
        exit_status = os.system("python parse.py --patentroot %s --xmlregex '2012_\d.xml'" % (os.getcwd() + '/test/unittest/fixtures'))
        self.assertTrue(exit_status == 0)

    def test_argparse_directory(self):
        # test that argparse is setting the variables correctly for directories
        # parse.py should not find any .xml files, but this should still pass
        exit_status = os.system('python parse.py --patentroot %s' % (os.getcwd() + '/test/unittest'))
        self.assertTrue(exit_status == 0)

        # parse.py should concatentate the correct directory and find xml files
        exit_status = os.system("python parse.py --patentroot %s --directory fixtures --xmlregex '2012_\d.xml'" % (os.getcwd() + '/test/unittest'))
        self.assertTrue(exit_status == 0)

        # TODO: make test for iterating through multiple directories

    def test_gets_environment_var(self):
        # sanity check for existing valid path
        logging.info("Testing getting valid env var PATENTROOT")
        self.assertTrue(os.environ.has_key('PATENTROOT'))

    def tearDown(self):
        os.chdir('test')

if __name__ == '__main__':

    open(log_file, 'w')
    unittest.main()
