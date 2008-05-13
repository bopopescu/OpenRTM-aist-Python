#!/usr/bin/env python
# -*- Python -*-

#
# \file test_Factory.py
# \brief test for RTComponent factory class
# \date $Date: $
# \author Shinji Kurihara
#
# Copyright (C) 2003-2005
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import sys
sys.path.insert(1,"../")

import OpenRTM
import unittest

from Factory import *

class testClass:
	def __init__(self,mgr):
		self.test(mgr)
		pass

	def test(self,mgr):
		print "testClass: ", mgr

class TestFactoryPython(unittest.TestCase):

	def setUp(self):
		#profile = OpenRTM.Properties()
		profile = None
		self.factory = FactoryPython(profile, testClass, OpenRTM.Delete)
		return

	def tearDown(self):
		del self
		return

	def test_create(self):
		self.factory.create(3)
	
	def destroy(self):
		pass

############### test #################
if __name__ == '__main__':
        unittest.main()
