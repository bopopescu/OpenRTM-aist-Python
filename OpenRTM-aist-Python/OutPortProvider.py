#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortProvider.py
# @brief OutPortProvider class
# @date  $Date: 2007/09/05$
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



import OpenRTM

##
# @if jp
#
# @class OutPortProvider
# @brief OutPortProvider
#
# - Port ���Ф��Ʋ����󶡤��Ƥ��뤫��������롣
#   PortProfile �� properties �� Provider �˴ؤ��������ɲä��롣
#
# (��) OutPort �� Provide ������
#
# OutPortCorbaProvider ���ʲ������
#  - dataport.interface_type = CORBA_Any
#  - dataport.dataflow_type = Push, Pull
#  - dataport.subscription_type = Once, New, Periodic
# 
# @since 0.4.0
#
# @else
#
#
# @endif
class OutPortProvider:
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._properties = []


  ##
  # @if jp
  # @brief InterfaceProfile������������
  #
  # InterfaceProfile�����������롣
  # �����ǻ��ꤹ��ץ�ѥƥ�������� NameValue ���֥������Ȥ�
  # dataport.interface_type �ͤ�Ĵ�١������ݡ��Ȥ����ꤵ��Ƥ���
  # ���󥿡��ե����������פȰ��פ�����Τ߾����������롣
  #
  # @param self
  # @param prop InterfaceProfile�����������ץ�ѥƥ�
  #
  # @else
  #
  # @endif
  def publishInterfaceProfile(self, prop):
    OpenRTM.NVUtil.appendStringValue(prop, "dataport.data_type", self._dataType)
    OpenRTM.NVUtil.appendStringValue(prop, "dataport.interface_type", self._interfaceType)
    OpenRTM.NVUtil.appendStringValue(prop, "dataport.dataflow_type", self._dataflowType)
    OpenRTM.NVUtil.appendStringValue(prop, "dataport.subscription_type", self._subscriptionType)


  ##
  # @if jp
  # @brief Interface������������
  #
  # Interface�����������롣
  # �����ǻ��ꤹ��ץ�ѥƥ�������� NameValue ���֥������Ȥ�
  # dataport.interface_type �ͤ�Ĵ�١������ݡ��Ȥ����ꤵ��Ƥ��ʤ����
  # NameValue �˾�����ɲä��롣
  # ���Ǥ�Ʊ�쥤�󥿡��ե���������Ͽ�Ѥߤξ��ϲ���Ԥ�ʤ���
  #
  # @param self
  # @param prop InterfaceProfile�����������ץ�ѥƥ�
  #
  # @else
  #
  # @endif
  def publishInterface(self, prop):
    if not OpenRTM.NVUtil.isStringValue(prop,"dataport.interface_type",self._interfaceType):
      return

    OpenRTM.NVUtil.append(prop,self._properties)


  ##
  # @if jp
  # @brief �ݡ��ȥ����פ����ꤹ��
  #
  # �����ǻ��ꤷ���ݡ��ȥ����פ����ꤹ�롣
  #
  # @param self
  # @param port_type �����оݥݡ��ȥ�����
  #
  # @else
  #
  # @endif
  def setPortType(self, port_type):
    self._portType = port_type


  ##
  # @if jp
  # @brief �ǡ��������פ����ꤹ��
  #
  # �����ǻ��ꤷ���ǡ��������פ����ꤹ�롣
  #
  # @param self
  # @param data_type �����оݥǡ���������
  #
  # @else
  #
  # @endif
  def setDataType(self, data_type):
    self._dataType = data_type


  ##
  # @if jp
  # @brief ���󥿡��ե����������פ����ꤹ��
  #
  # �����ǻ��ꤷ�����󥿡��ե����������פ����ꤹ�롣
  #
  # @param self
  # @param interface_type �����оݥ��󥿡��ե�����������
  #
  # @else
  #
  # @endif
  def setInterfaceType(self, interface_type):
    self._interfaceType = interface_type


  ##
  # @if jp
  # @brief �ǡ����ե������פ����ꤹ��
  #
  # �����ǻ��ꤷ���ǡ����ե������פ����ꤹ�롣
  #
  # @param self
  # @param dataflow_type �����оݥǡ����ե�������
  #
  # @else
  #
  # @endif
  def setDataFlowType(self, dataflow_type):
    self._dataflowType = dataflow_type


  ##
  # @if jp
  # @brief ���֥�����ץ���󥿥��פ����ꤹ��
  #
  # �����ǻ��ꤷ�����֥�����ץ���󥿥��פ����ꤹ�롣
  #
  # @param self
  # @param subs_type �����оݥ��֥�����ץ���󥿥���
  #
  # @else
  #
  # @endif
  def setSubscriptionType(self, subs_type):
    self._subscriptionType = subs_type


