#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
#  \file  OutPortCorbaProvider.py
#  \brief OutPortCorbaProvider class
#  \date  $Date: 2007/09/26 $
#  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006-2008
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.


from omniORB import any

import OpenRTM_aist
import RTC, RTC__POA



##
# @if jp
# @class OutPortCorbaProvider
# @brief OutPortCorbaProvider ���饹
#
# �̿����ʤ� CORBA �����Ѥ������ϥݡ��ȥץ�Х������μ������饹��
#
# @since 0.4.0
#
# @else
# @class OutPortCorbaProvider
# @brief OutPortCorbaProvider class
# @endif
class OutPortCorbaProvider(OpenRTM_aist.OutPortProvider, RTC__POA.OutPortAny):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param buffer_ �����ץ�Х����˳�����Ƥ�Хåե����֥�������
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, buffer_):
    OpenRTM_aist.OutPortProvider.__init__(self)
    self._buffer = buffer_

    # PortProfile setting
    self.setDataType(self._buffer.getPortDataType())
    self.setInterfaceType("CORBA_Any")
    self.setDataFlowType("Push, Pull")
    self.setSubscriptionType("Flush, New, Periodic")

    # ConnectorProfile setting
    self._objref = self._this()
    OpenRTM_aist.CORBA_SeqUtil.push_back(self._properties,
                                         OpenRTM_aist.NVUtil.newNV("dataport.corba_any.outport_ref",
                                                                   self._objref))


  ##
  # @if jp
  # @brief �Хåե�����ǡ������������
  #
  # ���ꤵ�줿�����Хåե�����ǡ�����������롣
  #
  # @param self
  #
  # @return �����ǡ���
  #
  # @else
  #
  # @endif
  def get(self):
    data = [None]
    self._buffer.read(data)
    try:
      retval = any.to_any(data[0])
    except:
      return None

    return retval
