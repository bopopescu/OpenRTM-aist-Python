#!/usr/bin/env python

import os,os.path,sys, string, commands
from distutils import core
from distutils import cmd
from distutils import log
from distutils import util
from distutils import errors
from distutils import version
from distutils.command import config
from distutils.command import build


core.DEBUG = False
modules = ["BasicDataType", "DataPort", "OpenRTM", "RTC", "SDOPackage"]
sample_modules = ["MyService"]

if os.sep == '/':
	sitedir = os.path.join("lib", "python" + sys.version[:3], "site-packages")
elif os.sep == ':':
	sitedir = os.path.join("lib", "site-packages")
else:
	if sys.version_info[0:3] >= (2, 2, 0):
		sitedir = os.path.join("lib", "site-packages")
	else:
		sitedir = "."


def compile_idl(cmd, pars, files):
	"""
	Put together command line for python stubs generation.
	"""
	cmdline = cmd +' '+ string.join(pars) +' '+ string.join(files)
	log.info(cmdline)
	status, output = commands.getstatusoutput(cmdline)
	log.info(output)
	if status != 0:
		raise errors.DistutilsExecError("Return status of %s is %d" %
						(cmd, status))


def gen_idl_name(dir, name):
	"""
	Generate name of idl file from directory prefix and IDL module name.
	"""
	return os.path.join(dir, name + ".idl")


class Build_idl (cmd.Command):
	"""
	This class realizes a subcommand of build command and is used for building
	IDL stubs.
	"""

	description = "Generate python stubs from IDL files"

	user_options = [
			("omniidl=", "i", "omniidl program used to build stubs"),
			("idldir=",  "d", "directory where IDL files reside")
			]

	def initialize_options(self):
		self.idldir  = None
		self.omniidl = None
		self.omniidl_params = ["-bpython"]
		self.idlfiles = ["BasicDataType", "DataPort", "OpenRTM", "RTC", "SDOPackage"]

	def finalize_options(self):
		if not self.omniidl:
			self.omniidl = "omniidl"
		if not self.idldir:
			self.idldir = os.path.join(os.getcwd(),"OpenRTM","RTM_IDL")

	def run(self):
		global modules

		#self.omniidl_params.append("-Wbpackage=OpenRTM.RTM_IDL")
		self.omniidl_params.append("-COpenRTM/RTM_IDL")
		util.execute(compile_idl,
			(self.omniidl, self.omniidl_params,
				[ gen_idl_name(self.idldir, module) for module in modules ]),
				"Generating python stubs from IDL files")

		self.idldir = os.path.join(os.getcwd(),"OpenRTM","examples","SimpleService")
		self.idlfiles = ["MyService"]
		self.omniidl_params[-1]=("-COpenRTM/examples/SimpleService")
		util.execute(compile_idl,
			(self.omniidl, self.omniidl_params,
				[ gen_idl_name(self.idldir, module) for module in sample_modules ]),
				"Generating python sample stubs from IDL files")


class Build (build.build):
	"""
	This is here just to override default sub_commands list of build class.
	We added 'build_idl' item.
	"""
	def has_pure_modules (self):
		return self.distribution.has_pure_modules()

	def has_c_libraries (self):
		return self.distribution.has_c_libraries()

	def has_ext_modules (self):
		return self.distribution.has_ext_modules()

	def has_scripts (self):
		return self.distribution.has_scripts()

	def has_idl_files (self):
		return True

	sub_commands = [('build_idl',     has_idl_files),
			('build_py',      has_pure_modules),
			('build_clib',    has_c_libraries),
			('build_ext',     has_ext_modules),
			('build_scripts', has_scripts)
			]

try:
	core.setup(name = "OpenRTM-aist-Python",
		   version = "0.4.1",
		   description = "Python modules for OpenRTM-aist-0.4.1",
		   author = "Shinji Kurihara",
		   author_email = "shinji.kurihara@aist.go.jp",
		   url = "http://www.is.aist.go.jp/rt/OpenRTM-aist/html/",
		   long_description = "OpenRTM-aist is a reference implementation of RT-Middleware,\
		   which is now under standardization process in OMG (Object Management Group).\
		   OpenRTM-aist is being developed and distributed by\
		   Task Intelligence Research Group,\
		   Intelligent Systems Research Institute,\
		   National Institute of Advanced Industrial Science and Technology (AIST), Japan.\
		   Please see http://www.is.aist.go.jp/rt/OpenRTM-aist/html/ for more detail.",
		   license = "LGPL",
		   cmdclass = { "build":Build, "build_idl":Build_idl },
		   packages = ["OpenRTM",
			       "OpenRTM.RTM_IDL",
			       "OpenRTM.RTM_IDL.RTC",
			       "OpenRTM.RTM_IDL.RTC__POA",
			       "OpenRTM.RTM_IDL.SDOPackage",
			       "OpenRTM.RTM_IDL.SDOPackage__POA",
			       "OpenRTM.rtc-template",
			       "OpenRTM.rtm-naming"],
		   data_files = [(sitedir,['OpenRTM.pth']),
				 (os.path.join(sitedir,'OpenRTM/RTM_IDL'),['OpenRTM/RTM_IDL/OpenRTM.pth']),
				 (os.path.join(sitedir,'OpenRTM/RTM_IDL'),['OpenRTM/RTM_IDL/BasicDataType.idl']),
				 (os.path.join(sitedir,'OpenRTM/RTM_IDL'),['OpenRTM/RTM_IDL/DataPort.idl']),
				 (os.path.join(sitedir,'OpenRTM/RTM_IDL'),['OpenRTM/RTM_IDL/OpenRTM.idl']),
				 (os.path.join(sitedir,'OpenRTM/RTM_IDL'),['OpenRTM/RTM_IDL/RTC.idl']),
				 (os.path.join(sitedir,'OpenRTM/RTM_IDL'),['OpenRTM/RTM_IDL/SDOPackage.idl'])])
	
except Exception, e:
	log.error("Error: %s", e)
