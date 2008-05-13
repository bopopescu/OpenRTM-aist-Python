#!/usr/bin/env python
# -*- Python -*- 

#
# \file test_ConfigAdmin.py
# \brief test for Configuration Administration classes
# \date $Date: 2007/09/04$
# \author Shinji Kurihara
#
# Copyright (C) 2007
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import sys
sys.path.insert(1,"../")

import unittest

import OpenRTM
from ConfigAdmin import *

configsample_spec = ["implementation_id", "ConfigSample",
					 "type_name",         "ConfigSample",
					 "description",       "Configuration example component",
					 "version",           "1.0",
					 "vendor",            "Shinji Kurihara, AIST",
					 "category",          "example",
					 "activity_type",     "DataFlowComponent",
					 "max_instance",      "10",
					 "language",          "C++",
					 "lang_type",         "compile",
					 # Configuration variables
					 "conf.default.int_param0", "0",
					 "conf.default.int_param1", "1",
					 "conf.default.double_param0", "0.11",
					 "conf.default.double_param1", "9.9",
					 "conf.default.str_param0", "hoge",
					 "conf.default.str_param1", "dara",
					 "conf.default.vector_param0", "0.0,1.0,2.0,3.0,4.0",
					 ""]

configsample_mode_spec = ["conf.default.int_param0", "10",
						  "conf.default.int_param1", "11",
						  "conf.default.double_param0", "0.22",
						  "conf.default.double_param1", "9999.9",
						  "conf.default.str_param0", "hogehoge",
						  "conf.default.str_param1", "daradaradata",
						  "conf.default.vector_param0", "0.1,1.1,2.1,3.1,4.1",
						  ""]

configsample_add_spec = ["conf.mode0.int_param0", "10",
						 "conf.mode0.int_param1", "11",
						 "conf.mode0.double_param0", "0.22",
						 "conf.mode0.double_param1", "9999.9",
						 "conf.mode0.str_param0", "hogehoge",
						 "conf.mode0.str_param1", "daradaradata",
						 "conf.mode0.vector_param0", "0.1,1.1,2.1,3.1,4.1",
						 ""]

class TestConfigAdmin(unittest.TestCase):
	def setUp(self):
		prop = OpenRTM.Properties(defaults_str=configsample_spec)
		self._ca = ConfigAdmin(prop.getNode("conf"))

	
	def test_bindParameter(self):
		self.int_param0    = [0]
		self.int_param1    = [0]
		self.double_param0 = [0.0]
		self.double_param1 = [0.0]
		self.str_param0    = [""]
		self.str_param1    = [""]
		self.vector_param0 = [[0.0,0.0,0.0,0.0,0.0]]

		self._ca.bindParameter("int_param0", self.int_param0, "0")
		self._ca.bindParameter("int_param1", self.int_param1, "1")
		self._ca.bindParameter("double_param0", self.double_param0, "0.11")
		self._ca.bindParameter("double_param1", self.double_param1, "9.9")
		self._ca.bindParameter("str_param0", self.str_param0, "hoge")
		self._ca.bindParameter("str_param1", self.str_param1, "dara")
		self._ca.bindParameter("vector_param0", self.vector_param0, "0.0,1.0,2.0,3.0,4.0")


	def test_update(self):
		self._ca.update(config_set="default")
		self._ca.update("default","int_param0")
		self._ca.update()


	def test_isChanged(self):
		self.assertEqual(self._ca.isChanged(),False)
	

	def test_getActiveId(self):
		self.assertEqual(self._ca.getActiveId(),"default")


	def test_haveConfig(self):
		self.assertEqual(self._ca.haveConfig("default"),True)
		# Failure pattern
		# self.assertEqual(self._ca.haveConfig("int_param0"),True)


	def test_isActive(self):
		self.assertEqual(self._ca.isActive(),True)


	def test_getConfigurationSets(self):
		self.assertEqual(self._ca.getConfigurationSets()[0].name,"default")


	def test_getConfigurationSet(self):
		self.assertEqual(self._ca.getConfigurationSet("default").name, "default")

	def test_setConfigurationSetValues(self):
		prop = OpenRTM.Properties(defaults_str=configsample_mode_spec)
		self.assertEqual(self._ca.setConfigurationSetValues("default",prop.getNode("conf.default")),True)
		print self._ca.getConfigurationSet("default")
	
	def test_getActiveConfigurationSet(self):
		self.assertEqual(self._ca.getActiveConfigurationSet().getName(),"default")
	
	def test_addConfigurationSet(self):
		prop = OpenRTM.Properties(defaults_str=configsample_add_spec)
		self.assertEqual(self._ca.addConfigurationSet(prop.getNode("conf.mode0")),True)

	def test_removeConfigurationSet(self):
		prop = OpenRTM.Properties(defaults_str=configsample_add_spec)
		self.assertEqual(self._ca.addConfigurationSet(prop.getNode("conf.mode0")),True)
		self._ca.removeConfigurationSet("mode0")
		self.assertEqual(self._ca.getConfigurationSet("mode0"),self._ca._emptyconf)

	
	def test_activateConfigurationSet(self):
		prop = OpenRTM.Properties(defaults_str=configsample_add_spec)
		self.assertEqual(self._ca.addConfigurationSet(prop.getNode("conf.mode0")),True)
		self.assertEqual(self._ca.activateConfigurationSet("mode0"),True)
		self.assertEqual(self._ca.activateConfigurationSet("default"),True)
		self.assertEqual(self._ca.activateConfigurationSet("mode0"),True)
		# Failure pattern
		# self.assertEqual(self._ca.activateConfigurationSet("mode1"),True)


    
############### test #################
if __name__ == '__main__':
        unittest.main()