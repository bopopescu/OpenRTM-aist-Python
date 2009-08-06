#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortCorbaConsumer.py
# @brief OutPortCorbaConsumer class
# @date  $Date: 2007/09/25 $
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
from omniORB import CORBA

import OpenRTM_aist
import RTC, RTC__POA 



##
# @if jp
# @class OutPortCorbaConsumer
#
# @brief OutPortCorbaConsumer ���饹
#
# �̿����ʤ� CORBA �����Ѥ������ϥݡ��ȥ��󥷥塼�ޤμ������饹��
#
# @since 0.4.0
#
# @else
# @class OutPortCorbaConsumer
# @brief OutPortCorbaConsumer class
# @endif
class OutPortCorbaConsumer(OpenRTM_aist.OutPortConsumer,OpenRTM_aist.CorbaConsumer):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param buffer_ �ܥݡ��Ȥ˳�����Ƥ�Хåե�
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, buffer_):
    self._buffer = buffer_
    OpenRTM_aist.CorbaConsumer.__init__(self)


  ##
  # @if jp
  # @brief �ǡ������ɤ߽Ф�
  #
  # ���ꤵ�줿�ǡ������ɤ߽Ф���
  #
  # @param self
  # @param data �ɤ߽Ф����ǡ����������륪�֥�������
  #
  # @return �ǡ����ɤ߽Ф��������(�ɤ߽Ф�����:true���ɤ߽Ф�����:false)
  #
  # @else
  #
  # @endif
  def get(self, data):
    try:
      obj = self._ptr()._narrow(RTC.OutPortAny)
      if CORBA.is_nil(obj):
        return False
      data[0] = any.from_any(obj.get(), keep_structs=True)
      return True
    except:
      return False
    
    return False


  ##
  # @if jp
  # @brief �ݡ��Ȥ���ǡ������������
  #
  # ��³��Υݡ��Ȥ���ǡ�����������롣
  # ���������ǡ��������������ꤵ�줿�Хåե��˽񤭹��ޤ�롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def pull(self):
    data = [None]
    if self.get(data):
      self._buffer.write(data[0])


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
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_any.outport_ref")
    if index < 0:
      return False

    if OpenRTM_aist.NVUtil.isString(properties,
                                    "dataport.corba_any.outport_ref"):

      try:
        ior = any.from_any(properties[index].value, keep_structs=True)
        print "OutPort ref: ", ior
        orb = OpenRTM_aist.Manager.instance().getORB()
        obj = orb.string_to_object(ior)
        self.setObject(obj)
        return True
      except:
        return False

    return False


  ##
  # @if jp
  # @brief �ǡ����������Τ������Ͽ���
  #
  # �ǡ����������Τμ�����꤫����Ͽ�������롣
  #
  # @param self
  # @param properties ��Ͽ�������
  #
  # @else
  #
  # @endif
  def unsubscribeInterface(self, properties):
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_any.outport_ref")
    if index < 0:
      return

    try:
      ior = any.from_any(properties[index].value, keep_structs=True)
      if ior:
        orb = OpenRTM_aist.Manager.instance().getORB()
        obj = orb.string_to_object(ior)
        if self._ptr()._is_equivalent(obj):
          self.releaseObject()

    except:
      return
