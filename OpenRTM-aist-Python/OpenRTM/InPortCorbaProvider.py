#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file  InPortCorbaProvider.py
# @brief InPortCorbaProvider class
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
 

from  omniORB import any
import sys
import traceback

import OpenRTM
import RTC,RTC__POA


##
# @if jp
# @class InPortCorbaProvider
# @brief InPortCorbaProvider ���饹
#
# �̿����ʤ� CORBA �����Ѥ������ϥݡ��ȥץ�Х������μ������饹��
#
# @since 0.4.0
#
# @else
# @class InPortCorbaProvider
# @brief InPortCorbaProvider class
# @endif
class InPortCorbaProvider(OpenRTM.InPortProvider, RTC__POA.InPortAny):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  # �ݡ��ȥץ�ѥƥ��˰ʲ��ι��ܤ����ꤹ�롣
  #  - ���󥿡��ե����������� : CORBA_Any
  #  - �ǡ����ե������� : Push, Pull
  #  - ���֥�����ץ���󥿥��� : Any
  #
  # @param self
  # @param buffer_ �����ץ�Х����˳�����Ƥ�Хåե����֥�������
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, buffer_):
    OpenRTM.InPortProvider.__init__(self)
    self._buffer = buffer_

    # PortProfile setting
    self.setDataType(self._buffer.getPortDataType())
    self.setInterfaceType("CORBA_Any")
    self.setDataFlowType("Push, Pull")
    self.setSubscriptionType("Any")

    # ConnectorProfile setting
    self._objref = self._this()


  ##
  # @if jp
  # @brief Interface������������
  #
  # Interface�����������롣
  #
  # @param self
  # @param prop Interface�����������ץ�ѥƥ�
  #
  # @else
  #
  # @endif
  def publishInterface(self, prop):
    if not OpenRTM.NVUtil.isStringValue(prop,
                "dataport.interface_type",
                "CORBA_Any"):
      return

    nv = self._properties
    OpenRTM.CORBA_SeqUtil.push_back(nv,
            OpenRTM.NVUtil.newNV("dataport.corba_any.inport_ref",
                     self._objref))
    OpenRTM.NVUtil.append(prop, nv)


  ##
  # @if jp
  # @brief �Хåե��˥ǡ�����񤭹���
  #
  # ���ꤵ�줿�Хåե��˥ǡ�����񤭹��ࡣ
  #
  # @param self
  # @param data ����оݥǡ���
  #
  # @else
  #
  # @endif
  def put(self, data):
    try:
      tmp = any.from_any(data, keep_structs=True)
      self._buffer.write(tmp)
    except:
      traceback.print_exception(*sys.exc_info())
      return

    return
