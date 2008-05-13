#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file ManagerConfig.py
 \brief RTC manager configuration
 \date $Date: $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2003-2005
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import sys
import os
import re
import getopt
import platform

import OpenRTM

  
  
class ManagerConfig :
	"""
	\if jp

	\class ManagerConfig
	\brief Manager configuration ���饹

	Manager �Υ���ե�����졼������Ԥ������ޥ�ɥ饤������������ꡢ
	(���뤤�ϰ����ʤ���)���󥹥��󥹲�����롣��Manager �Υץ�ѥƥ���������
	��Ԥ�

	����(�ե�����)�λ���ζ����ϰʲ��ΤȤ���Ǥ��롣
	�夬��äȤ⶯����������äȤ�夤��
	<OL>
	<LI>���ޥ�ɥ饤�󥪥ץ���� "-f"
	<LI>�Ķ��ѿ� "RTC_MANAGER_CONFIG"
	<LI>�ǥե��������ե����� "./rtc.conf"
	<LI>�ǥե��������ե����� "/etc/rtc.conf"
	<LI>�ǥե��������ե����� "/etc/rtc/rtc.conf"
	<LI>�ǥե��������ե����� "/usr/local/etc/rtc.conf"
	<LI>�ǥե��������ե����� "/usr/local/etc/rtc/rtc.conf"
	<LI>�����ߥ���ե�����졼�������
	</OL>
	�����������ޥ�ɥ饤�󥪥ץ���� "-d" �����ꤵ�줿���ϡ�
	(���Ȥ� -f ������ե��������ꤷ�Ƥ�)�����ߥ���ե�����졼�������
	�����Ѥ���롣

	\else

	\brief

	\endif
	"""
  
	# The list of default configuration file path.
	config_file_path = ["./rtc.conf",
						"/etc/rtc.conf",
						"/etc/rtc/rtc.conf",
						"/usr/local/etc/rtc.conf",
						"/usr/local/etc/rtc/rtc.conf",
						None]

	# Environment value to specify configuration file
	config_file_env = "RTC_MANAGER_CONFIG"


	def __init__(self, argc=None, argv=None):
		"""
        \if jp

        \brief ManagerConfig ���󥹥ȥ饯��

        Ϳ����줿�����ˤ��������Ʊ���ˤ��륳�󥹥ȥ饯����

        \param argc ���ޥ�ɥ饤������ο�
        \param argv ���ޥ�ɥ饤�����

        \else

        \brief ManagerConfig constructor

        The constructor that performs initialization at the same time with
        given arguments.

        \param argc The number of command line arguments
        \param argv The command line arguments

        \endif
		"""
		self._configFile = ""
		if argc != None and argv != None:
			self.init(argc,argv)


	def __del__(self):
		"""
        \if jp
        \brief ManagerConfig �ǥ��ȥ饯��
        \else
        \brief ManagerConfig destructor
        \endif
		"""
		pass


	def init(self, argc, argv):
		"""
        \if jp
        \brief �����

        ���ޥ�ɥ饤�������Ϳ���ƽ�������롣���ޥ�ɥ饤�󥪥ץ�����
        �ʲ��Τ�Τ����Ѳ�ǽ�Ǥ��롣

        -f file   : ����ե�����졼�����ե��������ꤹ�롣<br>
        -l module : ���ɤ���⥸�塼�����ꤹ�롣<br>
        -o options: ����¾���ץ�������ꤹ�롣��<br>
        -d        : �ǥե���ȤΥ���ե�����졼������Ȥ���<br>
        \else
        \brief Initialization

        Initialize with command line options. The following command options
        are available.

        -f file   : Specify a configuration file. <br>
        -l module : Specify modules to be loaded at the beginning. <br>
        -o options: Other options. <br>
        -d        : Use default static configuration. <br>
        \endif
		"""
		self.parseArgs(argc, argv)


	def configure(self, prop):
		"""
		 \if jp
		 \brief Configuration �η�̤�Property��ȿ�Ǥ�����
		 \param prop(OpenRTM.Properties)
		 \else
		 \brief Apply configuration results to Property
		 \param prop(OpenRTM.Properties)
		 \endif
		"""
		prop.setDefaults(OpenRTM.default_config)
		if self.findConfigFile():
			try:
				fd = file(self._configFile,"r")
				prop.load(fd)
				fd.close()
			except:
				print "Error: file open."
		return self.setSystemInformation(prop)

	"""
        \if jp

        \brief ����ե�����졼�������������

        ����ե�����졼������������롣init()�ƤӽФ����˸Ƥ֤ȡ�
        ��Ū��������줿�ǥե���ȤΥ���ե�����졼�������֤���
        init() �ƤӽФ���˸Ƥ֤ȡ����ޥ�ɥ饤��������Ķ��ѿ�����
        ��Ť�����������줿����ե�����졼�������֤���

        \else

        \brief Get configuration value.

        This operation returns default configuration statically defined,
        when before calling init() function. When after calling init() function,
        this operation returns initialized configuration value according to
        command option, environment value and so on.

        \endif
    """
	#def getConfig(self):
	#pass


	def parseArgs(self, argc, argv):
		"""
		 \if jp
		 \brief ���ޥ�ɰ�����ѡ�������
		 
		 -f file   : ����ե�����졼�����ե��������ꤹ�롣<br>
		 -l module : ���ɤ���⥸�塼�����ꤹ�롣��<br>
		 -o options: ����¾���ץ�������ꤹ�롣��<br>
		 -d        : �ǥե���ȤΥ���ե�����졼������Ȥ���<br>
		 \else
		 \brief Parse command arguments
		 
		 -f file   : Specify a configuration file. <br>
		 -l module : Specify modules to be loaded at the beginning. <br>
		 -o options: Other options. <br>
		 -d        : Use default static configuration. <br>
		 \endif
		"""
		try:
			opts, args = getopt.getopt(argv[1:], "f:l:o:d:")
		except getopt.GetoptError:
			print "Error: getopt error!"
			sys.exit(0)

		for opt, arg in opts:
			if opt == "-f":
				self._configFile = arg

			if opt == "-l":
				pass

			if opt == "-o":
				pass

			if opt == "-d":
				pass

		return


	def findConfigFile(self):
		"""
        \if jp
        \brief Configuration file ��õ��

        Configuration file ��ͥ����

        ���ޥ�ɥ��ץ��������Ķ��ѿ���ǥե���ȥե������ǥե��������

        �ǥե���ȶ������ץ����(-d): �ǥե���ȥե����뤬���äƤ�̵�뤷��
            �ǥե���������Ȥ�
        \else
        \brief Find configuration file
        \endif
		"""
		if self._configFile != "":
			if self.fileExist(self._configFile):
				return True

		env = os.getenv(self.config_file_env)
		if env != None:
			if self.fileExist(env):
				self._configFile = env
				return True

		i = 0
		while (self.config_file_path[i] != None):
			if self.fileExist(self.config_file_path[i]):
				self._configFile = self.config_file_path[i]
				return True
			i += 1

		return False


	def setSystemInformation(self, prop):
		"""
		 \if jp

		 \brief �����ƥ����򥻥åȤ���

		    �����ƥ�����������ץ�ѥƥ��˥��åȤ��롣���ꤵ��륭���ϰʲ����̤ꡣ
		    manager.os.name    : OS̾
		    manager.os.release : OS��꡼��̾
		    maanger.os.version : OS�С������̾
		    manager.os.arch    : OS�������ƥ�����
		    manager.os.hostname: �ۥ���̾
		    manager.pid        : �ץ���ID
		 \param prop(OpenRTM.Properties)
		 \else
		 \brief Set system information
		 
		    Get the following system info and set them to Manager's properties.
		    manager.os.name    : OS name
		    manager.os.release : OS release name
		    maanger.os.version : OS version
		    manager.os.arch    : OS architecture
		    manager.os.hostname: Hostname
		    manager.pid        : process ID
		 \param prop(OpenRTM.Properties)
		 \endif
		"""
		sysinfo = platform.uname()

		prop.setProperty("manager.os.name",     sysinfo[0])
		prop.setProperty("manager.os.hostname", sysinfo[1])
		prop.setProperty("manager.os.release",  sysinfo[2])
		prop.setProperty("manager.os.version",  sysinfo[3])
		prop.setProperty("manager.os.arch",     sysinfo[4])
		prop.setProperty("manager.pid",         os.getpid())
		
		return prop


	def fileExist(self, filename):
		"""
		 \if jp
		 \brief �ե����뤬¸�ߤ��뤫�ɤ����Τ����
		 \param filename(string)
		 \else
		 \brief Check file existance
		 \param filename(string)
		 \endif
		"""
		try:
			fp = open(filename)
		except:
			print "Can't open file:", filename
			return False
		else:
			fp.close()
			return True

		return False


