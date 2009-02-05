#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
#  \file DataInPort.py
#  \brief RTC::Port implementation for Data InPort
#  \date $Date: 2007/09/20 $
#  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006-2008
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.


import OpenRTM_aist
import RTC, RTC__POA



##
# @if jp
# @class DataInPort
# @brief InPort �� Port
#
# �ǡ������ϥݡ��Ȥμ������饹��
#
# @since 0.4.0
#
# @else
# @class DataInPort
# @brief InPort abstruct class
# @endif
class DataInPort(OpenRTM_aist.PortBase):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param name �ݡ���̾��
  # @param inport �����ǡ������ϥݡ��Ȥ˴�Ϣ�դ���InPort���֥�������
  # @param prop   �ݡ��������ѥץ�ѥƥ�
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, name, inport, prop):
    OpenRTM_aist.PortBase.__init__(self, name)

    # PortProfile::properties ������
    self.addProperty("port.port_type", "DataInPort")
    self._providers = []
    self._providers.append(OpenRTM_aist.InPortCorbaProvider(inport))
    self._providers[-1].publishInterfaceProfile(self._profile.properties)
    self._consumers = []
    self._consumers.append(OpenRTM_aist.OutPortCorbaConsumer(inport))
    # self._dummy = [1]


  ##
  # @if jp
  # @brief Interface������������
  #
  # Interface�����������롣
  # ����Port����ͭ���Ƥ���ץ�Х���(Provider)�˴ؤ�������
  # ConnectorProfile#properties���������롣
  #
  # @param self
  # @param connector_profile ���ͥ����ץ�ե�����
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @endif
  def publishInterfaces(self, connector_profile):
    #if len(self._dummy) != 1:
    #  print "Memory access violation was detected."
    #  print "dummy.size(): ", len(self._dummy)
    #  print "size() should be 1."

    for provider in self._providers:
      provider.publishInterface(connector_profile.properties)

    return RTC.RTC_OK
      

  ##
  # @if jp
  # @brief Interface����³����
  #
  # Interface����³���롣
  # Port����ͭ����Consumer��Ŭ�礹��Provider�˴ؤ������� 
  # ConnectorProfile#properties ������Ф���
  # Consumer��CORBA���֥������Ȼ��Ȥ����ꤹ�롣
  #
  # @param self
  # @param connector_profile ���ͥ������ץ�ե�����
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @endif
  def subscribeInterfaces(self, connector_profile):
    for consumer in self._consumers:
      consumer.subscribeInterface(connector_profile.properties)

    return RTC.RTC_OK


  ##
  # @if jp
  # @brief Interface�ؤ���³��������
  #
  # Interface�ؤ���³�������롣
  # Ϳ����줿ConnectorProfile�˴�Ϣ����Consumer�����ꤵ�줿���Ƥ�Object��
  # ��������³�������롣
  #
  # @param self
  # @param connector_profile ���ͥ������ץ�ե�����
  #
  # @else
  #
  # @endif
  def unsubscribeInterfaces(self, connector_profile):
    for consumer in self._consumers:
      consumer.unsubscribeInterface(connector_profile.properties)
    
    
