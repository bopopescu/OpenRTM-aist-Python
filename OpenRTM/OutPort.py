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


from omniORB import any

import OpenRTM

##
# @if jp
# @brief ����ñ���Ѵ������
# @else
# @endif
usec_per_sec = 1000000


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
    global usec_per_sec
    tm = time.time()
    tm_f       = tm - int(tm)     # �������μ��Ф�
    self.sec   = int(tm - tm_f)   # �������μ��Ф�
    self.usec  = int(tm_f * usec_per_sec) # sec -> usec (micro second)



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
class OutPort(OpenRTM.OutPortBase):
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
  def __init__(self, name, value, buffer_):
    OpenRTM.OutPortBase.__init__(self, name)
    self._buffer         = buffer_
    self._value          = value
    self._timeoutTick    = 1000 # timeout tick: 1ms
    self._readBlock      = False
    self._readTimeout    = 0
    self._writeBlock     = False
    self._writeTimeout   = 0
    self._OnWrite        = None
    self._OnWriteConvert = None
    self._OnRead         = None
    self._OnReadConvert  = None
    self._OnOverflow     = None
    self._OnUnderflow    = None


  ##
  # @if jp
  # @brief �ǿ��ǡ�������ǧ
  #
  # ���ߤΥХåե����֤˳�Ǽ����Ƥ���ǡ������ǿ��ǡ�������ǧ���롣
  #
  # @param self
  #
  # @return �ǿ��ǡ�����ǧ���
  #            ( true:�ǿ��ǡ������ǡ����Ϥޤ��ɤ߽Ф���Ƥ��ʤ�
  #             false:���Υǡ������ǡ����ϴ����ɤ߽Ф���Ƥ���)
  #
  # @else
  #
  # @endif
  def isNew(self):
    return self._buffer.isNew()


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
    if not value:
      value=self._value

    global usec_per_sec
    
    if self._OnWrite:
      self._OnWrite(value)

    timeout = self._writeTimeout

    tm_pre = Time()

    # blocking and timeout wait
    count = 0
    while self._writeBlock and self._buffer.isFull():
      if self._writeTimeout < 0:
        time.sleep(self._timeoutTick/usec_per_sec)
        continue
      
        
      # timeout wait
      tm_cur = Time()

      sec  = tm_cur.sec - tm_pre.sec
      usec = tm_cur.usec - tm_pre.usec

      timeout -= (sec * usec_per_sec + usec)

      if timeout < 0:
        break
      tm_pre = tm_cur
      time.sleep(self._timeoutTick/usec_per_sec)
      count += 1
      
    if self._buffer.isFull():
      if self._OnOverflow:
        self._OnOverflow(value)
      return False
      
    if not self._OnWriteConvert:
      self._buffer.put(value)
    else:
      self._buffer.put(self._OnWriteConvert(value))

    self.notify()
    return True


  ##
  # @if jp
  #
  # @brief �ǡ����ɤ߽Ф�
  #
  # DataPort �����ͤ��ɤ߽Ф�
  #
  # - ������Хå��ե��󥯥� OnRead �����åȤ���Ƥ����硢
  #   DataPort ���ݻ�����Хåե������ɤ߽Ф����� OnRead ���ƤФ�롣
  # - DataPort ���ݻ�����Хåե�����������ե��򸡽ФǤ���Хåե��ǡ�
  #   ���ġ��ɤ߽Ф��ݤ˥Хåե�����������ե��򸡽Ф�����硢
  #   ������Хå��ե��󥯥� OnUnderflow ���ƤФ�롣
  # - ������Хå��ե��󥯥� OnReadConvert �����åȤ���Ƥ����硢
  #   �Хåե��񤭹��߻��ˡ� OnReadConvert �� operator() ������ͤ�
  #   read()������ͤȤʤ롣
  # - setReadTimeout() �ˤ���ɤ߽Ф����Υ����ॢ���Ȥ����ꤵ��Ƥ����硢
  #   �Хåե���������ե����֤���������ޤǥ����ॢ���Ȼ��֤����Ԥ���
  #   OnUnderflow �����åȤ���Ƥ���Ф����ƤӽФ������
  #
  # @param self
  # @param value �ɤ߽Ф����ǡ���
  #
  # @return �ɤ߽Ф������¹Է��(�ɤ߽Ф�����:true���ɤ߽Ф�����:false)
  #
  # @else
  #
  # @brief Read data
  #
  # @endif
  def read(self, value):
    if self._OnRead:
      self._OnRead()

    timeout = self._readTimeout
    tm_pre = Time()

    # blocking and timeout wait
    while self._readBlock and self._buffer.isEmpty():
      if self._readTimeout < 0:
        time.sleep(self._timeoutTick/usec_per_sec)
        continue

      # timeout wait
      tm_cur = Time()
      sec  = tm_cur.sec - tm_pre.sec
      usec = tm_cur.usec - tm_pre.usec
      
      timeout -= (sec * usec_per_sec + usec)
      if timeout < 0:
        break
      tm_pre = tm_cur
      time.sleep(self._timeoutTick/usec_per_sec)

    if self._buffer.isEmpty():
      if self._OnUnderflow:
        value[0] = self._OnUnderflow()
        return False
      else:
        return False

    if not self._OnReadConvert:
      value[0] = self._buffer.get()
      return True
    else:
      value[0] = self._OnReadConvert(self._buffer.get())
      return true

    # never comes here
    return False


  ##
  # @if jp
  #
  # @brief �ǡ����ɤ߽Ф������Υ֥�å��⡼�ɤ�����
  #
  # �ɤ߽Ф��������Ф��ƥ֥�å��⡼�ɤ����ꤹ�롣
  # �֥�å��⡼�ɤ���ꤷ����硢�ɤ߽Ф���ǡ�����������뤫�����ॢ����
  # ��ȯ������ޤǡ� read() �᥽�åɤθƤӤ������֥�å�����롣
  #
  # @param self
  # @param block �֥�å��⡼�ɥե饰
  #
  # @else
  #
  # @brief Set read() block mode
  #
  # @endif
  def setReadBlock(self, block):
    self._readBlock = block


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
  def setWriteBlock(self, block):
    self._writeBlock = block


  ##
  # @if jp
  #
  # @brief �ɤ߽Ф������Υ����ॢ���Ȼ��֤�����
  # 
  # read() �Υ����ॢ���Ȼ��֤� usec �����ꤹ�롣
  # read() �ϥ֥�å��⡼�ɤǤʤ���Фʤ�ʤ���
  #
  # @param self
  # @param timeout �����ॢ���Ȼ��� [usec]
  #
  # @else
  #
  # @brief Set read() timeout
  #
  # @endif
  def setReadTimeout(self, timeout):
    self._readTimeout = timeout


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
  def setWriteTimeout(self, timeout):
    self._writeTimeout = timeout


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
  def setOnOverflow(self, on_overflow):
    self._OnOverflow = on_overflow


  ##
  # @if jp
  #
  # @brief OnRead ������Хå�������
  #
  # �ǡ����ɤ߽Ф�ľ���˸ƤӽФ���� OnRead ������Хå��ե��󥯥�������
  # ���롣
  #
  # @param self
  # @param on_read OnRead ������Хå��ե��󥯥�
  #
  # @else
  #
  # @brief Set OnRead callback
  #
  # @endif
  def setOnRead(self, on_read):
    self._OnRead = on_read


  ##
  # @if jp
  #
  # @brief OnReadConvert ������Хå�������
  #
  # �ǡ����ɤ߽Ф����˸ƤФ�� OnReadConvert ������Хå��ե��󥯥�������
  # ���롣
  # ���Υ�����Хå��ؿ��ν�����̤��ɤ߹��ޤ�롣
  # ���Τ����ɤ߹��ߥǡ����Υե��륿��󥰤���ǽ�Ȥʤ롣
  #
  # @param self
  # @param on_rconvert OnReadConvert ������Хå��ե��󥯥�
  #
  # @else
  #
  # @brief Set OnReadConvert callback
  #
  # @endif
  def setOnReadConvert(self, on_rconvert):
    self._OnReadConvert = on_rconvert


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
  def setOnUnderflow(self, on_underflow):
    self._OnUnderflow = on_underflow


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
