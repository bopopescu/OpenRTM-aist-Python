#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file OutPort.py
# @brief OutPort class
# @date $Date: 2007/09/19$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


from omniORB import *
from omniORB import any

import OpenRTM_aist

##
# @if jp
# @brief ����ñ���Ѵ������
# @else
# @endif
TIMEVALUE_ONE_SECOND_IN_USECS = 1000000 # 1 [sec] = 1000000 [usec]


import time



##
# @if jp
# @class Time
# @brief ���ִ����ѥ��饹
# 
# ���ꤷ�������ͤ��ݻ����뤿��Υ��饹��
# 
# @since 0.4.1
# 
# @else
# 
# @endif
class Time:



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯����
  #
  # @param self
  #
  # @else
  # @brief Constructor.
  #
  # Constructor.
  #
  # @param self
  #
  # @endif
  def __init__(self):
    global TIMEVALUE_ONE_SECOND_IN_USECS
    tm = time.time()
    tm_f       = tm - int(tm)     # �������μ��Ф�
    self.sec   = int(tm - tm_f)   # �������μ��Ф�
    self.usec  = int(tm_f * TIMEVALUE_ONE_SECOND_IN_USECS) # sec -> usec (micro second)



##
# @if jp
#
# @class OutPort
#
# @brief OutPort ���饹
# 
# OutPort �ѥ��饹
#
# @since 0.2.0
#
# @else
# 
# @endif
class OutPort(OpenRTM_aist.OutPortBase):
  """
  """



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param name �ݡ���̾
  # @param value ���Υݡ��Ȥ˥Х���ɤ����ǡ����ѿ�
  # @param buffer_ �Хåե�
  #
  # @else
  #
  # @brief Constructor
  #
  # @endif
  def __init__(self, name, value, buffer=None):
    OpenRTM_aist.OutPortBase.__init__(self, name, OpenRTM_aist.toTypename(value))
    self._value          = value
    #self._timeoutTick    = 1000 # timeout tick: 1ms
    #self._writeBlock     = False
    #self._writeTimeout   = 0
    self._OnWrite        = None
    self._OnWriteConvert = None
    #self._OnOverflow     = None
    #self._OnUnderflow    = None
    #self._OnConnect      = None
    #self._OnDisconnect   = None
    


  ##
  # @if jp
  #
  # @brief �ǡ����񤭹���
  #
  # �ݡ��Ȥإǡ�����񤭹��ࡣ
  #
  # - ������Хå��ե��󥯥� OnWrite �����åȤ���Ƥ����硢
  #   OutPort ���ݻ�����Хåե��˽񤭹������� OnWrite ���ƤФ�롣
  # - OutPort ���ݻ�����Хåե��������С��ե��򸡽ФǤ���Хåե��Ǥ��ꡢ
  #   ���ġ��񤭹���ݤ˥Хåե��������С��ե��򸡽Ф�����硢
  #   ������Хå��ե��󥯥� OnOverflow ���ƤФ�롣
  # - ������Хå��ե��󥯥� OnWriteConvert �����åȤ���Ƥ����硢
  #   �Хåե��񤭹��߻��ˡ� OnWriteConvert �� operator() ������ͤ�
  #   �Хåե��˽񤭹��ޤ�롣
  #
  # @param self
  # @param value �񤭹����оݥǡ���
  #
  # @return �񤭹��߽������(�񤭹�������:true���񤭹��߼���:false)
  #
  # @else
  #
  # @brief Write data
  #
  # @endif
  # virtual bool write(const DataType& value)
  ##
  # @if jp
  #
  # @brief �ǡ����񤭹���
  #
  # �ݡ��Ȥإǡ�����񤭹��ࡣ
  # ���ꤵ�줿�ͤ�ݡ��Ȥ˽񤭹��ࡣ
  #
  # @param self
  # @param value �񤭹����оݥǡ���
  #
  # @return �񤭹��߽������(�񤭹�������:true���񤭹��߼���:false)
  #
  # @else
  #
  # @endif
  # bool operator<<(DataType& value)
  def write(self, value=None):
    global TIMEVALUE_ONE_SECOND_IN_USECS
    if not value:
      value=self._value

    
    if self._OnWrite:
      self._OnWrite(value)

    # check number of connectors
    conn_size = len(self._connectors)
    if not conn_size > 0:
      return True
  
    # set timestamp
    tm = Time()
    value.tm.sec  = tm.sec
    value.tm.nsec = tm.usec * 1000

    tm_pre = Time()

    # data -> (conversion) -> CDR stream
    cdr_stream = None
    
    try:
      if self._OnWriteConvert:
        value = self._OnWriteConvert(value)
        cdr_stream = cdrMarshal(any.to_any(value).typecode(), value, 1)
      else:
        cdr_stream = cdrMarshal(any.to_any(value).typecode(), value, 1)
    except:
      print "Exception: cdrMarshal."
      return False
      
    result = True

    for con in self._connectors:
      ret = con.write(cdr_stream)
      if ret != OpenRTM_aist.DataPortStatus.PORT_OK:
        result = False
        if ret == OpenRTM_aist.DataPortStatus.CONNECTION_LOST:
          self.disconnect(con.id())

    return result


  ##
  # @if jp
  #
  # @brief �ǡ����񤭹��߽����Υ֥�å��⡼�ɤ�����
  #
  # �񤭹��߽������Ф��ƥ֥�å��⡼�ɤ����ꤹ�롣
  # �֥�å��⡼�ɤ���ꤷ����硢�Хåե��˽񤭹����ΰ褬�Ǥ��뤫
  # �����ॢ���Ȥ�ȯ������ޤ� write() �᥽�åɤθƤӤ������֥�å�����롣
  #
  # @param self
  # @param block �֥�å��⡼�ɥե饰
  #
  # @else
  #
  # @brief Set read() block mode
  #
  # @endif
  #def setWriteBlock(self, block):
  #  self._writeBlock = block


  ##
  # @if jp
  #
  # @brief �񤭹��߽����Υ����ॢ���Ȼ��֤�����
  # 
  # write() �Υ����ॢ���Ȼ��֤� usec �����ꤹ�롣
  # write() �ϥ֥�å��⡼�ɤǤʤ���Фʤ�ʤ���
  #
  # @param self
  # @param timeout �����ॢ���Ȼ��� [usec]
  #
  # @else
  #
  # @brief Set write() timeout
  #
  # @endif
  #def setWriteTimeout(self, timeout):
  #  self._writeTimeout = timeout


  ##
  # @if jp
  #
  # @brief OnWrite ������Хå�������
  #
  # �ǡ����񤭹���ľ���˸ƤФ�� OnWrite ������Хå��ե��󥯥������ꤹ�롣
  #
  # @param self
  # @param on_write OnWrite ������Хå��ե��󥯥�
  #
  # @else
  #
  # @brief Set OnWrite callback
  #
  # @endif
  def setOnWrite(self, on_write):
    self._OnWrite = on_write


  ##
  # @if jp
  #
  # @brief OnWriteConvert ������Хå�������
  #
  # �ǡ����񤭹��߻��˸ƤФ�� OnWriteConvert ������Хå��ե��󥯥�������
  # ���롣
  # ���Υ�����Хå��ؿ��ν�����̤��񤭹��ޤ�롣
  # ���Τ���񤭹��ߥǡ����Υե��륿��󥰤���ǽ�Ȥʤ롣
  #
  # @param self
  # @param on_wconvert OnWriteConvert ������Хå��ե��󥯥�
  #
  # @else
  #
  # @brief Set OnWriteConvert callback
  #
  # @endif
  def setOnWriteConvert(self, on_wconvert):
    self._OnWriteConvert = on_wconvert


  ##
  # @if jp
  #
  # @brief OnOverflow ������Хå�������
  #
  # �Хåե��ե�ˤ��ǡ����񤭹��ߤ��Ǥ��ʤ����˸ƤӽФ���� OnOverflow
  # ������Хå��ե��󥯥������ꤹ�롣
  #
  # @param self
  # @param on_overflow OnOverflow ������Хå��ե��󥯥�
  #
  # @else
  #
  # @brief Set OnOverflow callback
  #
  # @endif
  #def setOnOverflow(self, on_overflow):
  #  self._OnOverflow = on_overflow


  ##
  # @if jp
  #
  # @brief OnUnderflow ������Хå�������
  #
  # �Хåե�����ץƥ��ˤ���ɤ߽Ф���ǡ������ʤ����˸ƤӽФ����
  # ������Хå��ե��󥯥� OnUnderflow �����ꤹ�롣
  #
  # @param self
  # @param on_underflow OnUnderflow ������Хå��ե��󥯥�
  #
  # @else
  #
  # @brief Set OnUnderflow callback
  #
  # @endif
  #def setOnUnderflow(self, on_underflow):
  #  self._OnUnderflow = on_underflow


  #def setOnConnect(self, on_connect):
  #  self._OnConnect = on_connect


  #def setOnDisconnect(self, on_disconnect):
  #  self._OnDisconnect = on_disconnect


  #def onConnect(self, id, publisher):
  #  print "onConnect id:", id


  #def onDisconnect(self, id):
  #  print "onDisconnect id:", id


  ##
  # @if jp
  #
  # @brief �ǡ�����̾�����ѥ᥽�å�
  #
  # �ǡ����η�̾��������뤿�ᡢInPortCorbaProvider����ƤФ�롣
  # 
  # @param self
  #
  # @return �Хåե������ꤵ��Ƥ���ǡ����η�̾
  #
  # @else
  #
  # @endif
  def getPortDataType(self):
    val = any.to_any(self._value)
    return str(val.typecode().name())



  class subscribe:
    def __init__(self, prof, subs = None):
      if subs:
        self._prof = subs._prof
        self._consumer = subs._consumer
        return

      self._prof = prof
      self._consumer = None
      

    def __call__(self, cons):
      if cons.subscribeInterface(self._prof.properties):
        self._consumer = cons
