#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  InPortCorbaConsumer.py
# @brief InPortCorbaConsumer class
# @date  $Date: 2007/09/20 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


from omniORB import CORBA
from omniORB import any
import sys
import traceback

import RTC, RTC__POA
import OpenRTM


##
# @if jp
#
# @class InPortCorbaConsumer
#
# @brief InPortCorbaConsumer ���饹
#
# �̿����ʤ� CORBA �����Ѥ������ϥݡ��ȥ��󥷥塼�ޤμ������饹��
#
# @param DataType �ܥݡ��Ȥˤư����ǡ�����
#
# @since 0.4.0
#
# @else
# @class InPortCorbaConsumer
# @brief InPortCorbaConsumer class
# @endif
class InPortCorbaConsumer(OpenRTM.InPortConsumer,OpenRTM.CorbaConsumer):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param buffer_ �������󥷥塼�ޤ˳�����Ƥ�Хåե����֥�������
  # @param consumer Consumer ���֥�������(�ǥե������:None)
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, buffer_, consumer=None):
    if consumer:
      OpenRTM.CorbaConsumer.__init__(self, consumer=consumer)
      self._buffer = consumer._buffer
      return
    
    OpenRTM.CorbaConsumer.__init__(self)
    self._buffer = buffer_


  ##
  # @if jp
  # @brief �����黻��
  #
  # �����黻��
  #
  # @param self
  # @param consumer ������ InPortCorbaConsumer ���֥�������
  #
  # @return �������
  #
  # @else
  #
  # @endif
  def equal_operator(self, consumer):
    if self == consumer:
      return self

    self._buffer = consumer._buffer


  ##
  # @if jp
  # @brief �Хåե��ؤΥǡ������
  #
  # �Хåե��˥ǡ�����񤭹���
  #
  # @param self
  # @param data ����оݥǡ���
  #
  # @else
  #
  # @endif
  def put(self, data):
    tmp = any.to_any(data)
    obj = self._ptr()._narrow(RTC.InPortAny)
    obj.put(tmp)


  ##
  # @if jp
  # @brief �Хåե�����Υǡ������
  #
  # �Хåե�����ǡ�������Ф������Ф��롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def push(self):
    data = [None]
    self._buffer.read(data)
    tmp = any.to_any(data[0])

    if not self._ptr():
      return

    obj = self._ptr()._narrow(RTC.InPortAny)

    # �����ϥ��顼�����򤹤٤�
    if CORBA.is_nil(obj):
      return
    try:
      obj.put(tmp)
    except:
      # ���֥������Ȥ�̵���ˤʤä���disconnect���٤�
      traceback.print_exception(*sys.exec_info())
      return


  ##
  # @if jp
  # @brief ���ԡ�������
  #
  # ����InPortCorbaConsumer���֥������Ȥ�ʣ�����������롣
  #
  # @param self
  #
  # @return ���ԡ����줿InPortCorbaConsumer���֥�������
  #
  # @else
  #
  # @endif
  def clone(self):
    return OpenRTM.InPortCorbaConsumer(self, consumer=self)


  ##
  # @if jp
  # @brief �ǡ����������Τؤ���Ͽ
  #
  # ���ꤵ�줿�ץ�ѥƥ��˴�Ť��ơ��ǡ����������Τμ���������Ͽ���롣
  #
  # @param self
  # @param properties ��Ͽ����
  #
  # @return ��Ͽ�������(��Ͽ����:true����Ͽ����:false)
  #
  # @else
  #
  # @endif
  def subscribeInterface(self, properties):
    if not OpenRTM.NVUtil.isStringValue(properties,
                      "dataport.dataflow_type",
                      "Push"):
      return False

    index = OpenRTM.NVUtil.find_index(properties,
                      "dataport.corba_any.inport_ref")

    if index < 0:
      return False

    obj = None
    try:
      obj = any.from_any(properties[index].value,keep_structs=True)
    except:
      return False

    if not CORBA.is_nil(obj):
      self.setObject(obj)
      return True

    return False


  ##
  # @if jp
  # @brief �ǡ����������Τ������Ͽ���(���֥��饹������)
  #
  # �ǡ����������Τμ�����꤫����Ͽ�������롣<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param properties ��Ͽ�������
  #
  # @else
  #
  # @endif
  def unsubscribeInterface(self, properties):
    pass
