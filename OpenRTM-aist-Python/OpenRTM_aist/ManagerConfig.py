#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ManagerConfig.py
# @brief RTC manager configuration
# @date $Date: $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2003-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#    All rights reserved.


import sys
import os
import re
import getopt
import platform

import OpenRTM_aist


##
# @if jp
#
# @class ManagerConfig
# @brief Manager configuration ���饹
#
# Manager �Υ���ե�����졼������Ԥ������ޥ�ɥ饤������������ꡢ
# (���뤤�ϰ����ʤ���)���󥹥��󥹲�����롣
# ���ޥ�ɥ饤������ǻ��ꤵ�줿����ե����롢�Ķ��ѿ��ʤɤ��� Manager ��
# �ץ�ѥƥ���������ꤹ�롣
#
# �������ͥ���٤ϰʲ��ΤȤ���Ǥ��롣
# <OL>
# <LI>���ޥ�ɥ饤�󥪥ץ���� "-f"
# <LI>�Ķ��ѿ� "RTC_MANAGER_CONFIG"
# <LI>�ǥե��������ե����� "./rtc.conf"
# <LI>�ǥե��������ե����� "/etc/rtc.conf"
# <LI>�ǥե��������ե����� "/etc/rtc/rtc.conf"
# <LI>�ǥե��������ե����� "/usr/local/etc/rtc.conf"
# <LI>�ǥե��������ե����� "/usr/local/etc/rtc/rtc.conf"
# <LI>�����ߥ���ե�����졼�������
#</OL>
# �����������ޥ�ɥ饤�󥪥ץ���� "-d" �����ꤵ�줿���ϡ�
# (���Ȥ� -f ������ե��������ꤷ�Ƥ�)�����ߥ���ե�����졼�������
# �����Ѥ���롣
#
# @since 0.4.0
#
# @else
#
# @brief
#
# @endif
class ManagerConfig :
  """
  """



  ##
  # @if jp
  # @brief Manager ����ե�����졼�����Υǥե���ȡ��ե����롦�ѥ�
  # @else
  # @endif
  config_file_path = ["./rtc.conf",
            "/etc/rtc.conf",
            "/etc/rtc/rtc.conf",
            "/usr/local/etc/rtc.conf",
            "/usr/local/etc/rtc/rtc.conf",
            None]


  ##
  # @if jp
  # @brief �ǥե���ȡ�����ե�����졼�����Υե����롦�ѥ����̤���
  #        �Ķ��ѿ�
  # @else
  # @endif
  config_file_env = "RTC_MANAGER_CONFIG"


  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # Ϳ����줿�����ˤ�ꥳ��ե�����졼��������ν������Ԥ���
  #
  # @param self
  # @param argv ���ޥ�ɥ饤�����(�ǥե������:None)
  #
  # @else
  #
  # @brief ManagerConfig constructor
  #
  # The constructor that performs initialization at the same time with
  # given arguments.
  #
  # @param argv The command line arguments
  #
  # @endif
  def __init__(self, argv=None):

    self._configFile = ""
    self._isMaster   = False
    if argv:
      self.init(argv)


  ##
  # @if jp
  #
  # @brief �����
  #
  # ���ޥ�ɥ饤������˱����ƽ������¹Ԥ��롣���ޥ�ɥ饤�󥪥ץ�����
  # �ʲ��Τ�Τ����Ѳ�ǽ�Ǥ��롣
  #
  # -f file   : ����ե�����졼�����ե��������ꤹ�롣<br>
  # -l module : ���ɤ���⥸�塼�����ꤹ�롣(̤����)<br>
  # -o options: ����¾���ץ�������ꤹ�롣(̤����)<br>
  # -d        : �ǥե���ȤΥ���ե�����졼������Ȥ���(̤����)<br>
  #
  # @param self
  # @param argv ���ޥ�ɥ饤�����
  #
  # @else
  #
  # @brief Initialization
  #
  # Initialize with command line options. The following command options
  # are available.
  #
  # -f file   : Specify a configuration file. <br>
  # -l module : Specify modules to be loaded at the beginning. <br>
  # -o options: Other options. <br>
  # -d        : Use default static configuration. <br>
  #
  # @endif
  def init(self, argv):
    self.parseArgs(argv)


  ##
  # @if jp
  # @brief Configuration ����� Property �����ꤹ��
  # 
  # Manager ��Configuration �������ꤵ�줿 Property �����ꤹ�롣
  #
  # @param self
  # @param prop Configuration �����о� Property
  # 
  # @else
  # @brief Apply configuration results to Property
  # @endif
  def configure(self, prop):
    prop.setDefaults(OpenRTM_aist.default_config)
    if self.findConfigFile():
      try:
        fd = file(self._configFile,"r")
        prop.load(fd)
        fd.close()
      except:
        print "Error: file open."

    self.setSystemInformation(prop)
    if self._isMaster:
      prop.setProperty("manager.is_master","YES")

    return

  #######
  # \if jp
  #
  # \brief ����ե�����졼�������������(̤����)
  #
  # ����ե�����졼������������롣init()�ƤӽФ����˸Ƥ֤ȡ�
  # ��Ū��������줿�ǥե���ȤΥ���ե�����졼�������֤���
  # init() �ƤӽФ���˸Ƥ֤ȡ����ޥ�ɥ饤��������Ķ��ѿ�����
  # ��Ť�����������줿����ե�����졼�������֤���
  #
  # \else
  #
  # \brief Get configuration value.
  #
  # This operation returns default configuration statically defined,
  # when before calling init() function. When after calling init() function,
  # this operation returns initialized configuration value according to
  # command option, environment value and so on.
  #
  # \endif
  #def getConfig(self):
  #pass


  ##
  # @if jp
  #
  # @brief ���ޥ�ɰ�����ѡ�������
  #
  # -f file   : ����ե�����졼�����ե��������ꤹ�롣<br>
  # -l module : ���ɤ���⥸�塼�����ꤹ�롣(̤����)<br>
  # -o options: ����¾���ץ�������ꤹ�롣(̤����)<br>
  # -d        : �ǥե���ȤΥ���ե�����졼������Ȥ���(̤����)<br>
  #
  # @param self
  # @param argv ���ޥ�ɥ饤�����
  #
  # @else
  #
  # @brief Parse command arguments
  #
  # -f file   : Specify a configuration file. <br>
  # -l module : Specify modules to be loaded at the beginning. <br>
  # -o options: Other options. <br>
  # -d        : Use default static configuration. <br>
  #
  # @endif
  def parseArgs(self, argv):
    try:
      opts, args = getopt.getopt(argv[1:], "f:l:o:d")
    except getopt.GetoptError:
      print "Error: getopt error!"
      return

    for opt, arg in opts:
      if opt == "-f":
        self._configFile = arg

      if opt == "-l":
        pass

      if opt == "-o":
        pass

      if opt == "-d":
        self._isMaster = True
        pass

    return


  ##
  # @if jp
  #
  # @brief Configuration file �θ���
  #
  # Configuration file �򸡺��������ꤹ�롣
  # ���� Configuration file ������Ѥߤξ��ϡ��ե������¸�߳�ǧ��Ԥ���
  #
  # Configuration file ��ͥ����<br>
  # ���ޥ�ɥ��ץ��������Ķ��ѿ���ǥե���ȥե������ǥե��������
  #
  # �ǥե���ȶ������ץ����(-d): �ǥե���ȥե����뤬���äƤ�̵�뤷��
  #                               �ǥե���������Ȥ�
  #
  # @param self
  #
  # @return Configuration file �������
  #
  # @else
  #
  # @brief Find configuration file
  #
  # @endif
  def findConfigFile(self):
    if self._configFile != "":
      if self.fileExist(self._configFile):
        return True

    env = os.getenv(self.config_file_env)
    if env:
      if self.fileExist(env):
        self._configFile = env
        return True

    i = 0
    while (self.config_file_path[i]):
      if self.fileExist(self.config_file_path[i]):
        self._configFile = self.config_file_path[i]
        return True
      i += 1

    return False


  ##
  # @if jp
  #
  # @brief �����ƥ��������ꤹ��
  #
  # �����ƥ�����������ץ�ѥƥ��˥��åȤ��롣���ꤵ��륭���ϰʲ����̤ꡣ
  #  - manager.os.name    : OS̾
  #  - manager.os.release : OS��꡼��̾
  #  - maanger.os.version : OS�С������̾
  #  - manager.os.arch    : OS�������ƥ�����
  #  - manager.os.hostname: �ۥ���̾
  #  - manager.pid        : �ץ���ID
  # 
  # @param self
  # @param prop �����ƥ��������ꤷ���ץ�ѥƥ�
  #
  # @else
  # 
  # @brief Set system information
  # 
  # Get the following system info and set them to Manager's properties.
  #  - manager.os.name    : OS name
  #  - manager.os.release : OS release name
  #  - manager.os.version : OS version
  #  - manager.os.arch    : OS architecture
  #  - manager.os.hostname: Hostname
  #  - manager.pid        : process ID
  #
  # @endif
  def setSystemInformation(self, prop):
    sysinfo = platform.uname()

    prop.setProperty("manager.os.name",     sysinfo[0])
    prop.setProperty("manager.os.hostname", sysinfo[1])
    prop.setProperty("manager.os.release",  sysinfo[2])
    prop.setProperty("manager.os.version",  sysinfo[3])
    prop.setProperty("manager.os.arch",     sysinfo[4])
    prop.setProperty("manager.pid",         os.getpid())
    
    return prop


  ##
  # @if jp
  # @brief �ե������¸�߳�ǧ
  #
  # ���ꤵ�줿�ե����뤬¸�ߤ��뤫��ǧ���롣
  #
  # @param self
  # @param filename ��ǧ�оݥե�����̾��
  #
  # @return �оݥե������ǧ���(¸�ߤ������true)
  #
  # @else
  # @brief Check file existance
  # @endif
  def fileExist(self, filename):
    try:
      fp = open(filename)
    except:
      print "Can't open file:", filename
      return False
    else:
      fp.close()
      return True

    return False


