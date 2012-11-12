#! /usr/bin/env python

import unittest
import re
import os
import sys
import logging
from claim_driver import *

# Have 3 test files, with one, ten, hundred patents.

test_patent_one = "pg020507one.xml"
test_patent_ten = "pg020507ten.xml"
test_patent_hundred = "pg020507hundred.xml"


class TestClaimDriver(unittest.TestCase):
    
    def setUp(self):
        self.c = Claims()
        self.claim_list = []

    def test_claims_init(self):
        # Tests init of Claims() works as intended
        # Namely, to see if c.XMLs == []
        assert(not self.c.XMLs)

    def test_claims_parse(self):
        self.c.handle_file(test_patent_one)
   

        




if __name__ == '__main__':
    unittest.main()



