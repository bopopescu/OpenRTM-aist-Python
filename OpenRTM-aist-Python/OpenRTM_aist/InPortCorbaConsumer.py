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


from omniORB import *
from omniORB import CORBA
from omniORB import any
import sys
import traceback

import RTC, RTC__POA
import OpenRTM_aist
import OpenRTM, OpenRTM__POA


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
class InPortCorbaConsumer(OpenRTM_aist.InPortConsumer,OpenRTM_aist.CorbaConsumer):
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
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("InPortCorbaConsumer")

    if consumer:
      OpenRTM_aist.CorbaConsumer.__init__(self, consumer=consumer)
      self._buffer = consumer._buffer
      return
    
    OpenRTM_aist.CorbaConsumer.__init__(self)
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
    self._rtcout.RTC_PARANOID("put()")
    obj = self._ptr()._narrow(OpenRTM.InPortCdr)
    obj.put(data)


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
    self._rtcout.RTC_PARANOID("push()")
    data = [None]
    self._buffer.read(data)

    if not self._ptr():
      return

    obj = self._ptr()._narrow(OpenRTM.InPortCdr)

    # �����ϥ��顼�����򤹤٤�
    if CORBA.is_nil(obj):
      return
    try:
      obj.put(data[0])
    except:
      self._rtcout.RTC_INFO("exception while invoking _ptr().put()")
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
    self._rtcout.RTC_TRACE("clone()")
    return OpenRTM_aist.InPortCorbaConsumer(self, consumer=self)


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
    self._rtcout.RTC_TRACE("subscribeInterface()")

    if self.subscribeFromIor(properties):
      return True

    if self.subscribeFromRef(properties):
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
    self._rtcout.RTC_TRACE("unsubscribeInterface()")

    if self.unsubscribeFromIor(properties):
      return

    self.unsubscribeFromRef(properties)



  ##
  # @if jp
  # @brief IORʸ���󤫤饪�֥������Ȼ��Ȥ��������
  #
  # @return true: �������, false: ��������
  #
  # @else
  # @brief Getting object reference fromn IOR string
  #
  # @return true: succeeded, false: failed
  #
  # @endif
  #
  # bool subscribeFromIor(const SDOPackage::NVList& properties)
  def subscribeFromIor(self, properties):
    self.RTC_TRACE("subscribeFromIor()")
    
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_any.inport_ior")
    if index < 0:
      self._rtcout.RTC_ERROR("inport_ior not found")
      return False

    ior = any.from_any(properties[index].value, keep_structs=True)
    if not ior:
      self._rtcout.RTC_ERROR("inport_ior has no string")
      return False


    orb = OpenRTM_aist.Manager.instance().getORB()
    obj = orb.string_to_object(ior)
      
    if CORBA.is_nil(obj):
      self._rtcout.RTC_ERROR("invalid IOR string has been passed")
      return False

    if not self.setObject(obj):
      self._rtcout.RTC_WARN("Setting object to consumer failed.")
      return False

    return True


  ##
  # @if jp
  # @brief Any����ľ�ܥ��֥������Ȼ��Ȥ��������
  #
  # @return true: �������, false: ��������
  #
  # @else
  # @brief Getting object reference fromn Any directry
  #
  # @return true: succeeded, false: failed
  #
  # @endif
  #
  #bool subscribeFromRef(const SDOPackage::NVList& properties)
  def subscribeFromRef(self, properties):
    self._rtcout.RTC_TRACE("subscribeFromRef()")
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_any.inport_ref")
    if index < 0:
      self._rtcout.RTC_ERROR("inport_ref not found")
      return False


    obj = any.from_any(properties[index].value, keep_structs=True)
    if not obj:
      self._rtcout.RTC_ERROR("prop[inport_ref] is not objref")
      return True

    if CORBA.is_nil(obj):
      self._rtcout.RTC_ERROR("prop[inport_ref] is not objref")
      return False
      
    if not self.setObject(obj):
      self._rtcout.RTC_ERROR("Setting object to consumer failed.")
      return False

    return True


  ##
  # @if jp
  # @brief ��³���(IOR��)
  #
  # @return true: �������, false: ��������
  #
  # @else
  # @brief ubsubscribing (IOR version)
  #
  # @return true: succeeded, false: failed
  #
  # @endif
  #
  # bool unsubscribeFromIor(const SDOPackage::NVList& properties)
  def unsubscribeFromIor(self, properties):
    self._rtcout.RTC_TRACE("unsubscribeFromIor()")
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_any.inport_ior")
    if index < 0:
      self._rtcout.RTC_ERROR("inport_ior not found")
      return False

    ior = any.from_any(properties[index].value, keep_structs=True)
    if not ior:
      self._rtcout.RTC_ERROR("prop[inport_ior] is not string")
      return False


    orb = OpenRTM_aist.Manager.instance().getORB()
    var = orb.string_to_object(ior)
    
    if not self._ptr()._is_equivalent(var):
      self._rtcout.RTC_ERROR("connector property inconsistency")
      return False

    self.releaseObject()
    return True


  ##
  # @if jp
  # @brief ��³���(Object reference��)
  #
  # @return true: �������, false: ��������
  #
  # @else
  # @brief ubsubscribing (Object reference version)
  #
  # @return true: succeeded, false: failed
  #
  # @endif
  #
  # bool unsubscribeFromRef(const SDOPackage::NVList& properties)
  def unsubscribeFromRef(self, properties):
    self._rtcout.RTC_TRACE("unsubscribeFromRef()")
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_any.inport_ref")
    if index < 0:
      return False

    obj = any.from_any(properties[index].value, keep_structs=True)
    if not obj:
      return False

    if not self._ptr()._is_equivalent(obj):
      return False

    self.releaseObject()
    return True
