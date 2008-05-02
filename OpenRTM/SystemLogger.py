#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file SystemLogger.py
# @brief RT component logger class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2003-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import time
import threading
import logging
import logging.handlers

logger = None

##
# @if jp
# @class ScopedLock
# @brief ScopedLock ���饹
#
# ��¾�����ѥ�å����饹��
#
# @since 0.4.0
#
# @else
#
# @endif
class ScopedLock:
  def __init__(self, mutex):
    self.mutex = mutex
    self.mutex.acquire()

  def __del__(self):
    self.mutex.release()


##
# @if jp
#
# @class Logbuf
#
# @brief �����Хåե����ߡ����饹
#
# ���Хåե��Υ��ߡ����饹��
#
# @else
#
# @class Logbuf
#
# @brief Logger buffer dummy class
#
# @endif
class Logbuf:



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # �ե�����̾����ӥ����ץ�⡼�ɤ���ꤷ�ƥ��󥹥ȥ饯�Ȥ��륳�󥹥ȥ饯��
  #
  # @param self
  # @param fileName ���ե�����̾(�ǥե������:None)
  # @param mode �����ץ�⡼��(�ǥե������:None)
  # @param protection �ݸ�⡼��(�ǥե������:a+)�ܼ����Ǥ�̤����
  #
  # @else
  #
  # @brief constructor.
  #
  # @endif
  def __init__(self, fileName=None, mode=None, protection='a+'):
    global logger
    self._mutex = threading.RLock()

    logger = logging.getLogger('rtclog')

    if fileName:
      self._fhdlr = logging.FileHandler(fileName)
    else:
      self._fhdlr = logging.FileHandler('rtcsystem.log')


  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯�����ե�����򥯥������롣
  #
  # @param self
  #
  # @else
  #
  # @brief destractor.
  #
  # @endif
  def __del__(self):
    self._fhdlr.close()



##
# @if jp
#
# @class LogStream
#
# @brief �����ե����ޥåȥ��ߡ����饹
#
# ���ե����ޥå��ѥ��ߡ����饹��
#
# @else
#
# @endif
class LogStream:



  SILENT    = 0 # ()
  ERROR     = 1 # (ERROR)
  WARN      = 2 # (ERROR, WARN)
  INFO      = 3 # (ERROR, WARN, INFO)
  NORMAL    = 4 # (ERROR, WARN, INFO, NORMAL)
  DEBUG     = 5 # (ERROR, WARN, INFO, NORMAL, DEBUG)
  TRACE     = 6 # (ERROR, WARN, INFO, NORMAL, DEBUG, TRACE)
  VERBOSE   = 7 # (ERROR, WARN, INFO, NORMAL, DEBUG, TRACE, VERBOSE)
  PARANOID  = 8 # (ERROR, WARN, INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARA)
  MANDATORY = 9 #  This level is used for only LogLockLevel


  ##
  # @if jp
  #
  # @brief ����٥�����
  #
  # Ϳ����줿ʸ������б���������٥�����ꤹ�롣
  #
  # @param self
  # @param lv ����٥�ʸ����
  #
  # @return ���ꤷ������٥�
  #
  # @else
  #
  # @endif
  def strToLogLevel(self, lv):
    if lv == LogStream.SILENT:
      return LogStream.SILENT
    elif lv == LogStream.ERROR:
      return LogStream.ERROR
    elif lv == LogStream.WARN:
      return LogStream.WARN
    elif lv == LogStream.INFO:
      return LogStream.INFO
    elif lv == LogStream.NORNAL:
      return LogStream.NORMAL
    elif lv == LogStream.DEBUG:
      return LogStream.DEBUG
    elif lv == LogStream.TRACE:
      return LogStream.TRACE
    elif lv == LogStream.VERBOSE:
      return LogStream.VERBOSE
    elif lv == LogStream.PARANOID:
      return LogStream.PARANOID
    elif lv == LogStream.MANDATORY:
      return LogStream.MANDATORY
    else:
      return LogStream.NORMAL


  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param logbufObj ���Хåե����֥�������(�ǥե������:None)
  #
  # @else
  #
  # @brief constructor.
  #
  # @endif
  def __init__(self, logbufObj=None):
    global logger
    self._mutex = threading.RLock()
    self._LogLock = False
    self._log_enable = False
    if logbufObj:
      formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
      self._pLogbuf = logbufObj
      fh = self._pLogbuf._fhdlr
      self._mhdlr = logging.handlers.MemoryHandler(1024,logging.DEBUG, fh)
      fh.setFormatter(formatter)
      logger.addHandler(self._mhdlr)
      logger.setLevel(logging.DEBUG)
      self._log_enable = True


  ##
  # @if jp
  #
  # @brief printf �ե����ޥåȽ���
  #
  # printf�饤���ʽ񼰤ǥ����Ϥ��롣<br>
  # ���ܼ����Ǥϰ��� fmt ��Ϳ����줿ʸ���򤽤Τޤ��֤���
  #
  # @param self
  # @param fmt ��ʸ����
  #
  # @return ���դ�ʸ�������
  #
  # @else
  #
  # @brief Formatted output like printf
  #
  # @endif
  def printf(self, fmt):
    return fmt


  ##
  # @if jp
  #
  # @brief ����٥�����
  #
  # ����٥�����ꤹ�롣
  #
  # @param self
  # @param level ����٥�
  #
  # @else
  #
  # @endif
  def setLogLevel(self, level):
    global logger

    if level == "INFO":
      logger.setLevel(logging.INFO)
    elif level == "ERROR":
      logger.setLevel(logging.ERROR)
    elif level == "WARNING":
      logger.setLevel(logging.WARNING)
    elif level == "DEBUG":
      logger.setLevel(logging.DEBUG)
    elif level == "SILENT":
      logger.setLevel(logging.NOTSET)
    else:
      logger.setLevel(logging.INFO)


  ##
  # @if jp
  #
  # @brief ��å��⡼������
  #
  # ���Υ�å��⡼�ɤ����ꤹ�롣
  #
  # @param self
  # @param lock ����å��ե饰
  #
  # @else
  #
  # @endif
  def setLogLock(self, lock):
    if lock == 1:
      self._LogLock = True
    elif lock == 0:
      self._LogLock = False


  ##
  # @if jp
  #
  # @brief ��å��⡼��ͭ����
  #
  # @param self
  #
  # ��å��⡼�ɤ�ͭ���ˤ��롣
  #
  # @else
  #
  # @endif
  def enableLogLock(self):
    self._LogLock = True


  ##
  # @if jp
  #
  # @brief ��å��⡼�ɲ��
  #
  # @param self
  #
  # ��å��⡼�ɤ�̵���ˤ��롣
  #
  # @else
  #
  # @endif
  def disableLogLock(self):
    self._LogLock = False


  ##
  # @if jp
  #
  # @brief ����å�����
  # ��å��⡼�ɤ����ꤵ��Ƥ����硢���Υ�å���������롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def acquire(self):
    if self._LogLock:
      self.guard = ScopedLock(self._mutex)


  ##
  # @if jp
  #
  # @brief ����å�����
  # ��å��⡼�ɤ����ꤵ��Ƥ�����ˡ����Υ�å���������롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def release(self):
    if self._LogLock:
      del self.guard


  ##
  # @if jp
  #
  # @brief ���ѥ�����
  #
  # ����٥뤪��ӽ��ϥե����ޥå�ʸ���������Ȥ��ƤȤꡤ
  # ���ѥ�����Ϥ��롣
  #
  # @param self
  # @param LV ����٥�
  # @param msg ����å�����
  # @param opt ���ץ����(�ǥե������:None)
  #
  # @else
  #
  # @brief Log output macro
  #
  # @endif
  def RTC_LOG(self, LV, msg, opt=None):
    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_LOG : argument error"
          return
      else:
        messages = msg

      logger.log(LV,messages)

      self.release()


  ##
  # @if jp
  #
  # @brief ���顼������
  #
  # ���顼��٥�Υ�����Ϥ��롣<BR>����٥뤬
  # ERROR, WARN, INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARANOID
  # �ξ��˥����Ϥ���롣
  #
  # @param self
  # @param msg ����å�����
  # @param opt ���ץ����(�ǥե������:None)
  #
  # @else
  #
  # @brief Error log output macro.
  #
  # @endif
  def RTC_ERROR(self, msg, opt=None):
    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_ERROR : argument error"
          return
      else:
        messages = msg

      logger.error(messages)

      self.release()


  ##
  # @if jp
  #
  # @brief ��˥󥰥�����
  #
  # ��˥󥰥�٥�Υ�����Ϥ��롣<BR>����٥뤬
  # ( WARN, INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARANOID )
  # �ξ��˥����Ϥ���롣
  #
  # @param self
  # @param msg ����å�����
  # @param opt ���ץ����(�ǥե������:None)
  #
  # @else
  #
  # @brief Warning log output macro.
  #
  # If logging levels are
  # ( WARN, INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_WARN(self, msg, opt=None):
    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_WARN : argument error"
          return
      else:
        messages = msg

      logger.warning(messages)

      self.release()


  ##
  # @if jp
  #
  # @brief ����ե�������
  #
  # ����ե���٥�Υ�����Ϥ��롣<BR>����٥뤬
  # ( INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARANOID )
  # �ξ��˥����Ϥ���롣
  #
  # @param self
  # @param msg ����å�����
  # @param opt ���ץ����(�ǥե������:None)
  #
  # @else
  #
  # @brief Infomation level log output macro.
  #
  #  If logging levels are
  # ( INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_INFO(self, msg, opt=None):
    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_INFO : argument error"
          return
      else:
        messages = msg

      logger.info(messages)
    
      self.release()


  ##
  # @if jp
  #
  # @brief �Ρ��ޥ������
  #
  # �Ρ��ޥ��٥�Υ�����Ϥ��롣<BR>����٥뤬
  # ( NORMAL, DEBUG, TRACE, VERBOSE, PARANOID )
  # �ξ��˥����Ϥ���롣
  #
  # @param self
  # @param msg ����å�����
  # @param opt ���ץ����(�ǥե������:None)
  #
  # @else
  #
  # @brief Normal level log output macro.
  #
  # If logging levels are
  # ( NORMAL, DEBUG, TRACE, VERBOSE, PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_NORMAL(self, msg, opt=None):
    return

    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_NORMAL : argument error"
          return
      else:
        messages = msg
        
      self.release()


  ##
  # @if jp
  #
  # @brief �ǥХå�������
  #
  # �ǥХå���٥�Υ�����Ϥ��롣<BR>����٥뤬
  # ( DEBUG, TRACE, VERBOSE, PARANOID )
  # �ξ��˥����Ϥ���롣
  #
  # @param self
  # @param msg ����å�����
  # @param opt ���ץ����(�ǥե������:None)
  #
  # @else
  #
  # @brief Debug level log output macro.
  #
  # If logging levels are
  # ( DEBUG, TRACE, VERBOSE, PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_DEBUG(self, msg, opt=None):
    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_DEBUG : argument error"
          return
      else:
        messages = msg
        
      logger.debug(messages)
      
      self.release()


  ##
  # @if jp
  #
  # @brief �ȥ졼��������
  #
  # �ȥ졼����٥�Υ�����Ϥ��롣<BR>����٥뤬
  # ( TRACE, VERBOSE, PARANOID )
  # �ξ��˥����Ϥ���롣
  #
  # @param self
  # @param msg ����å�����
  # @param opt ���ץ����(�ǥե������:None)
  #
  # @else
  #
  # @brief Trace level log output macro.
  #
  # If logging levels are
  # ( TRACE, VERBOSE, PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_TRACE(self, msg, opt=None):
    global logger

    if self._log_enable:
      self.acquire()

      if opt:
        try:
          messages = msg%(opt)
        except:
          print "RTC_TRACE : argument error"
          return
      else:
        messages = msg
        
      logger.debug(messages)
      
      self.release()


  ##
  # @if jp
  #
  # @brief �٥�ܡ���������
  #
  # �٥�ܡ�����٥�Υ�����Ϥ��롣<BR>����٥뤬
  # ( VERBOSE, PARANOID )
  # �ξ��˥����Ϥ���롣<br>
  # �������Ǥ�̤����
  #
  # @param self
  # @param msg ����å�����
  # @param opt ���ץ����(�ǥե������:None)
  #
  # @else
  #
  # @brief Verbose level log output macro.
  #
  # If logging levels are
  # ( VERBOSE, PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_VERBOSE(self, msg, opt=None):
    pass


  ##
  # @if jp
  #
  # @brief �ѥ�Υ��ɥ�����
  #
  # �ѥ�Υ��ɥ�٥�Υ�����Ϥ��롣<BR>����٥뤬
  # ( PARANOID )
  # �ξ��˥����Ϥ���롣<br>
  # �������Ǥ�̤����
  #
  # @param self
  # @param msg ����å�����
  # @param opt ���ץ����(�ǥե������:None)
  #
  # @else
  #
  # @brief Paranoid level log output macro.
  #
  # If logging levels are
  # ( PARANOID ),
  # message will be output to log.
  #
  # @endif
  def RTC_PARANOID(self, msg, opt=None):
    pass
