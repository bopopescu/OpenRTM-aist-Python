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
#
# @class Logg
#
# @brief �����ե����ޥåȥ��ߡ����饹
#
# ���ե����ޥå��ѥ��ߡ����饹��
#
# @else
#
# @endif
class Logger:



  SILENT    = 0  # ()
  ERROR     = 40 # (ERROR)
  WARN      = 30 # (ERROR, WARN)
  INFO      = 20 # (ERROR, WARN, INFO)
  NORMAL    = 11 # (ERROR, WARN, INFO, NORMAL)
  DEBUG     = 10 # (ERROR, WARN, INFO, NORMAL, DEBUG)
  TRACE     = 9  # (ERROR, WARN, INFO, NORMAL, DEBUG, TRACE)
  VERBOSE   = 8  # (ERROR, WARN, INFO, NORMAL, DEBUG, TRACE, VERBOSE)
  PARANOID  = 7  # (ERROR, WARN, INFO, NORMAL, DEBUG, TRACE, VERBOSE, PARA)
  MANDATORY = 6  #  This level is used for only LogLockLevel


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
    if lv == "SILENT":
      return Logger.SILENT
    elif lv == "ERROR":
      return Logger.ERROR
    elif lv == "WARN":
      return Logger.WARN
    elif lv == "INFO":
      return Logger.INFO
    elif lv == "NORMAL":
      return Logger.NORMAL
    elif lv == "DEBUG":
      return Logger.DEBUG
    elif lv == "TRACE":
      return Logger.TRACE
    elif lv == "VERBOSE":
      return Logger.VERBOSE
    elif lv == "PARANOID":
      return Logger.PARANOID
    elif lv == "MANDATORY":
      return Logger.MANDATORY
    else:
      return Logger.INFO



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param (mode,file_name,address)
  #
  # @else
  #
  # @brief constructor.
  #
  # @endif
  def __init__(self, *args):
    self._mutex = threading.RLock()
    self._fhdlr = None


  def init(*args):
    global logger

    if logger is not None:
      return logger


    logger = Logger()
    mode = None
    fileName = None

    if len(args) == 0:
      return
    elif len(args) == 2:
      name = args[0]
      mode = args[1]
    elif len(args) == 3:
      name = args[0]
      mode = args[1]
      fileName = args[2]


    logging.MANDATORY = logging.DEBUG - 4
    logging.PARANOID  = logging.DEBUG - 3
    logging.VERBOSE   = logging.DEBUG - 2
    logging.TRACE     = logging.DEBUG - 1
    logging.NORMAL    = logging.DEBUG + 1

    logging.addLevelName(logging.MANDATORY, "MANDATORY")
    logging.addLevelName(logging.PARANOID,  "PARANOID")
    logging.addLevelName(logging.VERBOSE,   "VERBOSE")
    logging.addLevelName(logging.TRACE,     "TRACE")
    logging.addLevelName(logging.NORMAL,    "NORMAL")

    logging.root.setLevel([logging.NOTSET,
                           logging.MANDATORY,
                           logging.PARANOID,
                           logging.VERBOSE,
                           logging.TRACE,
                           logging.DEBUG,
                           logging.NORMAL,
                           logging.INFO,
                           logging.WARNING,
                           logging.ERROR,
                           logging.CRITICAL])

    
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

    if mode is None or mode == "FILE":
      if fileName:
        logger._fhdlr = logging.FileHandler(fileName)
      else:
        logger._fhdlr = logging.FileHandler('rtcsystem.log')

      mhdlr = logging.handlers.MemoryHandler(1024,logging.NOTSET, logger._fhdlr)
      logger._fhdlr.setFormatter(formatter)
      logging.getLogger("").addHandler(mhdlr)
      logging.getLogger("").setLevel(logging.NOTSET)
      
    elif mode == "STDOUT":
      ch = logging.StreamHandler()
      ch.setLevel(logging.NOTSET)
      ch.setFormatter(formatter)
      logging.getLogger("").addHandler(ch)

    return logger

  init = staticmethod(init)



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
    #if self._fhdlr is not None:
    #  self._fhdlr.close()
    #  self._fhdler = None
    pass

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


  def addHandler(self, *args):
    mode = None
    fileName = None

    if len(args) == 0:
      return
    elif len(args) == 1:
      mode = args[0]
    elif len(args) == 2:
      mode = args[0]
      fileName = args[1]
    
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

    if mode is None or mode == "FILE":
      if fileName:
        self._fhdlr = logging.FileHandler(fileName)
      else:
        self._fhdlr = logging.FileHandler('rtcsystem.log')

      mhdlr = logging.handlers.MemoryHandler(1024,logging.NOTSET, self._fhdlr)
      self._fhdlr.setFormatter(formatter)
      logging.getLogger("").addHandler(mhdlr)
      
    elif mode.lower() == "stdout":
      ch = logging.StreamHandler()
      ch.setLevel(logging.NOTSET)
      ch.setFormatter(formatter)
      logging.getLogger("").addHandler(ch)



##
# @if jp
#
# @class Logg
#
# @brief �����ե����ޥåȥ��ߡ����饹
#
# ���ե����ޥå��ѥ��ߡ����饹��
#
# @else
#
# @endif
class LogStream:

  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param (mode,file_name,address)
  #
  # @else
  #
  # @brief constructor.
  #
  # @endif
  def __init__(self, *args):
    self._LogLock = False
    self._log_enable = False
    self._loggerObj = None
    name = ""

    if len(args) == 0:
      return
    elif len(args) > 0:
      name = args[0]

    self._loggerObj = Logger.init(*args)
    self._log_enable = True
    self.logger = logging.getLogger(name)


  def addHandler(self, *args):
    if self._loggerObj is not None:
      self._loggerObj.addHandler(*args)


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
    if level == "INFO":
      self.logger.setLevel(logging.INFO)
    elif level == "ERROR":
      self.logger.setLevel(logging.ERROR)
    elif level == "WARN":
      self.logger.setLevel(logging.WARNING)
    elif level == "DEBUG":
      self.logger.setLevel(logging.DEBUG)
    elif level == "SILENT":
      self.logger.setLevel(logging.NOTSET)
    elif level == "NORMAL":
      self.logger.setLevel(logging.NORMAL)
    elif level == "TRACE":
      self.logger.setLevel(logging.TRACE)
    elif level == "VERBOSE":
      self.logger.setLevel(logging.VERBOSE)
    elif level == "PARANOID":
      self.logger.setLevel(logging.PARANOID)
    elif level == "MANDATORY":
      self.logger.setLevel(logging.MANDATORY)
    else:
      self.logger.setLevel(logging.INFO)


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
      self.guard = OpenRTM_aist.ScopedLock(self._mutex)


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
    if self._log_enable:
      self.acquire()

      if opt is None:
        messages = msg
      else:
        try:
          messages = msg%(opt)
        except:
          print "RTC_LOG : argument error"
          return

      self.logger.log(LV,messages)

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
    if self._log_enable:
      self.acquire()

      if opt is None:
        messages = msg
      else:
        try:
          messages = msg%(opt)
        except:
          print "RTC_ERROR : argument error"
          return

      self.logger.error(messages)

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
    if self._log_enable:
      self.acquire()

      if opt is None:
        messages = msg
      else:
        try:
          messages = msg%(opt)
        except:
          print "RTC_WARN : argument error"
          return

      self.logger.warning(messages)

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
    if self._log_enable:
      self.acquire()

      if opt is None:
        messages = msg
      else:
        try:
          messages = msg%(opt)
        except:
          print "RTC_INFO : argument error"
          return

      self.logger.info(messages)
    
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
    if self._log_enable:
      self.acquire()

      if opt is None:
        messages = msg
      else:
        try:
          messages = msg%(opt)
        except:
          print "RTC_NORMAL : argument error"
          return

      self.logger.log(logging.NORMAL,messages)
    
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
    if self._log_enable:
      self.acquire()

      if opt is None:
        messages = msg
      else:
        try:
          messages = msg%(opt)
        except:
          print "RTC_DEBUG : argument error"
          return
        
      self.logger.debug(messages)
      
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
    if self._log_enable:
      self.acquire()

      if opt is None:
        messages = msg

      else:
        try:
          messages = msg%(opt)
        except:
          print "RTC_TRACE : argument error"
          return

      self.logger.log(logging.TRACE,messages)
    
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
    if self._log_enable:
      self.acquire()

      if opt is None:
        messages = msg
      else:
        try:
          messages = msg%(opt)
        except:
          print "RTC_VERBOSE : argument error"
          return

      self.logger.log(logging.VERBOSE,messages)
    
      self.release()



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
    if self._log_enable:
      self.acquire()

      if opt is None:
        messages = msg
      else:
        try:
          messages = msg%(opt)
        except:
          print "RTC_PARANOID : argument error"
          return

      self.logger.log(logging.PARANOID,messages)
    
      self.release()


  ##
  # @if jp
  #
  # @brief �ޥ���ȥ꡼����
  #
  # �ޥ���ȥ꡼��٥�Υ�����Ϥ��롣<BR>����٥뤬
  # ( MANDATORY )
  # �ξ��˥����Ϥ���롣<br>
  # �������Ǥ�̤����
  #
  # @param self
  # @param msg ����å�����
  # @param opt ���ץ����(�ǥե������:None)
  #
  # @else
  #
  # @brief Mandatory level log output macro.
  #
  # If logging levels are
  # ( MANDATORY ),
  # message will be output to log.
  #
  # @endif
  def RTC_MANDATORY(self, msg, opt=None):
    if self._log_enable:
      self.acquire()

      if opt is None:
        messages = msg
      else:
        try:
          messages = msg%(opt)
        except:
          print "RTC_MANDATORY : argument error"
          return

      self.logger.log(logging.MANDATORY,messages)
    
      self.release()

