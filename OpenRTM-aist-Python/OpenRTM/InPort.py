#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file InPort.py
# @brief InPort template class
# @date $Date: 2007/09/20 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2003-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

from omniORB import any
import sys
import traceback

import OpenRTM_aist

TIMEOUT_TICK_USEC = 10.0
USEC_PER_SEC      = 1000000.0
TIMEOUT_TICK_SEC = TIMEOUT_TICK_USEC/USEC_PER_SEC


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
    tm = time.time()
    tm_f       = tm - int(tm)     # �������μ��Ф�
    self.sec   = int(tm - tm_f)   # �������μ��Ф�
    self.usec  = int(tm_f * USEC_PER_SEC) # sec -> usec (micro second)



##
# @if jp
#
# @class InPort
#
# @brief InPort ���饹
# 
# InPort �μ������饹��
# InPort �������˥�󥰥Хåե�����������������������줿�ǡ�����缡
# ���Υ�󥰥Хåե��˳�Ǽ���롣��󥰥Хåե��Υ������ϥǥե���Ȥ�64��
# �ʤäƤ��뤬�����󥹥ȥ饯�������ˤ�ꥵ��������ꤹ�뤳�Ȥ��Ǥ��롣
# �ǡ����ϥե饰�ˤ�ä�̤�ɡ����ɾ��֤��������졢isNew(), getNewDataLen()
# getNewList(), getNewListReverse() ���Υ᥽�åɤˤ��ϥ�ɥ�󥰤��뤳�Ȥ�
# �Ǥ��롣
#
# @since 0.2.0
#
# @else
#
# @class InPort
#
# @brief InPort template class
#
# This class template provides interfaces to input port.
# Component developer can define input value, which act as input
# port from other components, using this template.
# This is class template. This class have to be incarnated class as port
# value types. This value types are previously define RtComponent IDL.
# ex. type T: TimedFload, TimedLong etc... 
#
# @since 0.2.0
#
# @endif
class InPort:
  """
  """



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯����
  #
  # @param self
  # @param name InPort ̾��InPortBase:name() �ˤ�껲�Ȥ���롣
  # @param value ���� InPort �˥Х���ɤ�����ѿ�
  # @param buffer_ InPort ���������ݻ�����Хåե�
  # @param read_block �ɹ��֥�å��ե饰��
  #        �ǡ����ɹ�����̤�ɥǡ������ʤ���硢���Υǡ��������ޤǥ֥�å�����
  #        ���ɤ���������(�ǥե������:False)
  # @param write_block ����֥�å��ե饰��
  #        �ǡ���������˥Хåե����ե�Ǥ��ä���硢�Хåե��˶������Ǥ���
  #        �ޤǥ֥�å����뤫�ɤ���������(�ǥե������:False)
  # @param read_timeout �ɹ��֥�å�����ꤷ�Ƥ��ʤ����Ρ��ǡ����ɼ西����
  #        �����Ȼ���(�ߥ���)(�ǥե������:0)
  # @param write_timeout ����֥�å�����ꤷ�Ƥ��ʤ����Ρ��ǡ������������
  #        �����Ȼ���(�ߥ���)(�ǥե������:0)
  #
  # @else
  #
  # @brief A constructor.
  #
  # Setting channel name and registering channel value.
  #
  # @param self
  # @param name A name of the InPort. This name is referred by
  #             InPortBase::name().
  # @param value A channel value related with the channel.
  # @param buffer_ Buffer length of internal ring buffer of InPort 
  # @param read_block
  # @param write_block
  # @param read_timeout
  # @param write_timeout
  #
  # @endif
  def __init__(self, name, value, buffer_,
         read_block=False, write_block=False,
         read_timeout=0, write_timeout = 0):
    self._buffer         = buffer_
    self._name           = name
    self._value          = value
    self._readBlock      = read_block
    self._readTimeout    = read_timeout
    self._writeBlock     = write_block
    self._writeTimeout   = write_timeout
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
  # @brief �ݡ���̾�Τ�������롣
  #
  # �ݡ���̾�Τ�������롣
  #
  # @param self
  #
  # @return �ݡ���̾��
  #
  # @else
  #
  # @endif
  def name(self):
    return self._name


  ##
  # @if jp
  #
  # @brief DataPort ���ͤ�񤭹���
  #
  # DataPort ���ͤ�񤭹��ࡣ
  #
  # - ������Хå��ե��󥯥� OnWrite �����åȤ���Ƥ����硢
  #   InPort ���ݻ�����Хåե��˽񤭹������� OnWrite ���ƤФ�롣
  # - InPort ���ݻ�����Хåե��������С��ե��򸡽ФǤ���Хåե��Ǥ��ꡢ
  #   ���ġ��񤭹���ݤ˥Хåե��������С��ե��򸡽Ф�����硢
  #   ������Хå��ե��󥯥� OnOverflow ���ƤФ�롣
  # - ������Хå��ե��󥯥� OnWriteConvert �����åȤ���Ƥ����硢
  #   �Хåե��񤭹��߻��ˡ�OnWriteConvert �� operator()() ������ͤ�
  #   �Хåե��˽񤭹��ޤ�롣
  # - setWriteTimeout() �ˤ��񤭹��߻��Υ����ॢ���Ȥ����ꤵ��Ƥ����硢
  #   �����ॢ���Ȼ��֤����Хåե��ե���֤��������Τ��Ԥ���
  #   OnOverflow�����åȤ���Ƥ���Ф����ƤӽФ�����롣
  #
  # @param self
  # @param value ����оݥǡ���
  #
  # @return ����������(�������:true���������:false)
  #
  # @else
  #
  # @brief 
  #
  # @endif
  def write(self, value):
    if self._OnWrite:
      self._OnWrite(value)

    timeout = self._writeTimeout

    tm_pre = Time()

    # blocking and timeout wait
    while self._writeBlock and self._buffer.isFull():
      if self._writeTimeout < 0:
        time.sleep(TIMEOUT_TICK_SEC)
        continue

      # timeout wait
      tm_cur = Time()

      sec  = tm_cur.sec - tm_pre.sec
      usec = tm_cur.usec - tm_pre.usec

      timeout -= (sec * USEC_PER_SEC + usec)

      if timeout < 0:
        break

      tm_pre = tm_cur
      time.sleep(TIMEOUT_TICK_USEC)

    if self._buffer.isFull() and self._OnOverflow:
      self._OnOverflow(value)
      return False

    if not self._OnWriteConvert:
      self._buffer.put(value)
    else:
      self._buffer.put(self._OnWriteConvert(value))

    return True


  ##
  # @if jp
  #
  # @brief DataPort �����ͤ��ɤ߽Ф�
  #
  # DataPort �����ͤ��ɤ߽Ф�
  #
  # - ������Хå��ե��󥯥� OnRead �����åȤ���Ƥ����硢
  #   DataPort ���ݻ�����Хåե������ɤ߽Ф����� OnRead ���ƤФ�롣
  # - DataPort ���ݻ�����Хåե�����������ե��򸡽ФǤ���Хåե��ǡ�
  #   ���ġ��ɤ߽Ф��ݤ˥Хåե�����������ե��򸡽Ф�����硢
  #   ������Хå��ե��󥯥� OnUnderflow ���ƤФ�롣
  # - ������Хå��ե��󥯥� OnReadConvert �����åȤ���Ƥ����硢
  #   �Хåե��񤭹��߻��ˡ�OnReadConvert �� operator()() ������ͤ�
  #   read()������ͤȤʤ롣
  # - setReadTimeout() �ˤ���ɤ߽Ф����Υ����ॢ���Ȥ����ꤵ��Ƥ����硢
  #   �Хåե���������ե����֤���������ޤǥ����ॢ���Ȼ��֤����Ԥ���
  #   OnUnderflow�����åȤ���Ƥ���Ф����ƤӽФ������
  #
  # @param self
  #
  # @return �ɤ߽Ф����ǡ���
  #
  # @else
  #
  # @brief [CORBA interface] Put data on InPort
  #
  # @endif
  def read(self):
    if self._OnRead:
      self._OnRead()

    timeout = self._readTimeout

    tm_pre = Time()

    # blocking and timeout wait
    while self._readBlock and self._buffer.isEmpty():
      if self._readTimeout < 0:
        time.sleep(TIMEOUT_TICK_SEC)
        continue

      # timeout wait
      tm_cur = Time()

      sec  = tm_cur.sec - tm_pre.sec
      usec = tm_cur.usec - tm_pre.usec
      
      timeout -= (sec * USEC_PER_SEC + usec)

      if timeout < 0:
        break

      tm_pre = tm_cur
      time.sleep(TIMEOUT_TICK_SEC)

    if self._buffer.isEmpty():
      if self._OnUnderflow:
        self._value = self._OnUnderflow()
      return self._value

    if not self._OnReadConvert:
      self._value = self._buffer.get()
      return self._value
    else:
      self._value = self._OnReadConvert(self._buffer.get())
      return self._value

    # never comes here
    return self._value


  ##
  # @if jp
  #
  # @brief InPort ��Υ�󥰥Хåե����ͤ�����(���֥��饹������)
  #
  # InPort ��Υ�󥰥Хåե����ͤ���ꤷ���ͤǽ�������롣<BR>
  # �����֥��饹�Ǥμ�����������
  #
  # @param self
  # @param value ������оݥǡ���
  #
  # @else
  #
  # @brief Initialize ring buffer value of InPort
  #
  # @endif
  def init(self, value):
    pass


  ##
  # @if jp
  #
  # @brief �Х���ɤ��줿�ѿ��� InPort �Хåե��κǿ��ͤ��ɤ߹���
  #
  # �Х���ɤ��줿�ǡ����� InPort �κǿ��ͤ��ɤ߹��ࡣ
  # ���󥹥ȥ饯�����ѿ��� InPort ���Х���ɤ���Ƥ��ʤ���Фʤ�ʤ���
  # ���Υ᥽�åɤϥݥ�⡼�ե��å��˻��Ѥ�����������Ȥ��Ƥ��뤿�ᡢ
  # ���˰�¸���ʤ�����������ͤȤʤäƤ��롣
  #
  # @param self
  #
  # @else
  #
  # @brief Read into bound T-type data from current InPort
  #
  # @endif
  def update(self):
    try:
      self._value = self._buffer.get()
    except:
      if self._OnUnderflow:
        self._OnUnderflow()
      else:
        traceback.print_exception(*sys.exc_info())
        
    return


  ##
  # @if jp
  #
  # @brief ̤�ɤο������ǡ��������������
  #
  # �Хåե����̤�ɥǡ�������������롣
  #
  # @param self
  #
  # @return ̤�ɥǡ�����
  #
  # @else
  #
  # @brief Get number of new data to be read.
  #
  # @endif
  def getNewDataLen(self):
    return self._buffer.new_data_len()


  ##
  # @if jp
  #
  # @brief ̤�ɤο������ǡ������������
  #
  # �Хåե����̤�ɥǡ����ꥹ�Ȥ�������롣
  #
  # @param self
  #
  # @return ̤�ɥǡ����ꥹ��
  #
  # @else
  #
  # \brief Get new data to be read.
  #
  # @endif
  def getNewList(self):
    return self._buffer.get_new_list()


  ##
  # @if jp
  #
  # @brief ̤�ɤο������ǡ�����ս�(��->��)�Ǽ�������
  #
  # �Хåե����̤�ɥǡ�����ս�(��->��)�ǥꥹ�Ȳ������������롣
  #
  # @param self
  #
  # @return ̤�ɥǡ����ꥹ��
  #
  # @else
  #
  # \brief Get new data to be read.
  #
  # @endif
  def getNewListReverse(self):
    return self._buffer.get_new_rlist()


  ##
  # @if jp
  #
  # @brief InPort �Хåե��إǡ������ϻ��Υ�����Хå�������
  #
  # InPort �����ĥХåե��˥ǡ�����put���줿�Ȥ��˸ƤФ�륳����Хå�
  # ���֥������Ȥ����ꤹ�롣���ꤵ��륳����Хå����֥������Ȥ�
  # ������ value ������������ void �� __call__ �ؿ���������Ƥ���ɬ�פ����롣
  #
  # <pre>
  # class MyOnWrite:
  #     def __call__(self, value):
  #       ����<br>
  # </pre>
  # �Τ褦�˥�����Хå����֥������Ȥ��������<br> 
  # m_inport.setOnWrite(new MyOnWrite());<br>
  # �Τ褦�˥�����Хå����֥������Ȥ򥻥åȤ��롣
  #
  # @param self
  # @param on_write �����оݥ�����Хå����֥�������
  #
  # @else
  #
  # @brief Get new data to be read.
  #
  # @endif
  def setOnWrite(self, on_write):
    self._OnWrite = on_write


  ##
  # @if jp
  #
  # @brief InPort �Хåե��إǡ����񤭹��߻��Υ�����Хå�������
  #
  # InPort �����ĥХåե��˥ǡ����񤭹��ޤ����˸ƤФ�륳����Хå�
  # ���֥������Ȥ����ꤹ�롣�Хåե��ˤϥ�����Хå����֥������Ȥ�
  # ����ͤ����ꤵ��롣
  # 
  # @param self
  # @param on_wconvert �����оݥ�����Хå����֥�������
  #
  # @else
  #
  # @endif
  def setOnWriteConvert(self, on_wconvert):
    self._OnWriteConvert = on_wconvert


  ##
  # @if jp
  #
  # @brief InPort �Хåե��إǡ����ɤ߹��߻��Υ�����Хå�������
  #
  # InPort �����ĥХåե�����ǡ������ɤ߹��ޤ��ľ���˸ƤФ�륳����Хå�
  # ���֥������Ȥ����ꤹ�롣
  # 
  # @param self
  # @param on_read �����оݥ�����Хå����֥�������
  #
  # @else
  #
  # @endif
  def setOnRead(self, on_read):
    self._OnRead = on_read


  ##
  # @if jp
  #
  # @brief InPort �Хåե��إǡ����ɤ߽Ф����Υ�����Хå�������
  #
  # InPort �����ĥХåե�����ǡ������ɤ߽Ф����ݤ˸ƤФ�륳����Хå�
  # ���֥������Ȥ����ꤹ�롣������Хå����֥������Ȥ�����ͤ�read()�᥽�å�
  # �θƽз�̤Ȥʤ롣
  # 
  # @param self
  # @param on_rconvert �����оݥ�����Хå����֥�������
  #
  # @else
  #
  # @endif
  def setOnReadConvert(self, on_rconvert):
    self._OnReadConvert = on_rconvert


  ##
  # @if jp
  #
  # @brief InPort �Хåե��إХåե������С��ե����Υ�����Хå�������
  #
  # InPort �����ĥХåե��ǥХåե������С��ե������Ф��줿�ݤ˸ƤӽФ����
  # ������Хå����֥������Ȥ����ꤹ�롣
  # 
  # @param self
  # @param on_overflow �����оݥ�����Хå����֥�������
  #
  # @else
  #
  # @endif
  def setOnOverflow(self, on_overflow):
    self._OnOverflow = on_overflow


  ##
  # @if jp
  #
  # @brief InPort �Хåե��إХåե���������ե����Υ�����Хå�������
  #
  # InPort �����ĥХåե��ǥХåե���������ե������Ф��줿�ݤ˸ƤӽФ����
  # ������Хå����֥������Ȥ����ꤹ�롣
  # 
  # @param self
  # @param on_underflow �����оݥ�����Хå����֥�������
  #
  # @else
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
