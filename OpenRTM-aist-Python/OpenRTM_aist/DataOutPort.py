#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file DataOutPort.py
# @brief Base class of OutPort
# @date $Date: 2007/09/20 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import OpenRTM_aist
import RTC, RTC__POA


##
# @if jp
# @class DataOutPort
# @brief Outort �� Port
#
# �ǡ������ϥݡ��Ȥμ������饹��
#
# @since 0.4.0
#
# @else
# @class DataOutPort
# @brief OutPort abstruct class
# @endif
class DataOutPort(OpenRTM_aist.PortBase):
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
  # @param outport �����ǡ������ϥݡ��Ȥ˴�Ϣ�դ���OutPort���֥�������
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, name, outport, prop):
    OpenRTM_aist.PortBase.__init__(self, name)
    self._outport = outport
    # PortProfile::properties ������
    self.addProperty("port.port_type", "DataOutPort")
    self._providers = []
    self._providers.append(OpenRTM_aist.OutPortCorbaProvider(outport))
    self._providers[-1].publishInterfaceProfile(self._profile.properties)
    self._consumers = []
    self._consumers.append(OpenRTM_aist.InPortCorbaConsumer(outport))
    self._pf = OpenRTM_aist.PublisherFactory()


  ##
  # @if jp
  #
  # @brief Interface ������������
  #
  # ���Υ��ڥ졼�����ϡ�notify_connect() �����������󥹤λϤ�˥�����
  # �����ؿ��Ǥ��롣
  # notify_connect() �Ǥϡ�
  #
  # - publishInterfaces()
  # - connectNext()
  # - subscribeInterfaces()
  # - updateConnectorProfile()
  #
  # �ν�� protected �ؿ��������뤵����³�������Ԥ��롣
  # <br>
  # ���Υ��ڥ졼�����ϡ������� connector_id ���Ф��Ƥ���³��������
  # ��¸�� connector_id ���Ф��ƤϹ�����Ŭ�ڤ˹Ԥ���ɬ�פ����롣
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Publish interface information
  #
  # This operation is pure virutal method that would be called at the
  # beginning of the notify_connect() process sequence.
  # In the notify_connect(), the following methods would be called in order.
  #
  # - publishInterfaces()
  # - connectNext()
  # - subscribeInterfaces()
  # - updateConnectorProfile() 
  #
  # This operation should create the new connection for the new
  # connector_id, and should update the connection for the existing
  # connection_id.
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  # @endif
  def publishInterfaces(self, connector_profile):
    for provider in self._providers:
      provider.publishInterface(connector_profile.properties)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief Interface ����³����
  #
  # ���Υ��ڥ졼�����ϡ�notify_connect() �����������󥹤���֤˥�����
  # �����ؿ��Ǥ��롣
  # notify_connect() �Ǥϡ�
  #
  # - publishInterfaces()
  # - connectNext()
  # - subscribeInterfaces()
  # - updateConnectorProfile()
  #
  # �ν�� protected �ؿ��������뤵����³�������Ԥ��롣
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Publish interface information
  #
  # This operation is pure virutal method that would be called at the
  # mid-flow of the notify_connect() process sequence.
  # In the notify_connect(), the following methods would be called in order.
  #
  # - publishInterfaces()
  # - connectNext()
  # - subscribeInterfaces()
  # - updateConnectorProfile()
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  # @endif
  def subscribeInterfaces(self, connector_profile):
    subscribe = self.subscribe(prof=connector_profile)
    for consumer in self._consumers:
      subscribe(consumer)

    if not subscribe._consumer:
      return RTC.RTC_OK

    
    # Publisher������
    prop = OpenRTM_aist.NVUtil.toProperties(connector_profile.properties)
    publisher = self._pf.create(subscribe._consumer.clone(), prop)

    # Publisher��OutPort�˥����å�
    self._outport.attach(connector_profile.connector_id, publisher)
    # self._outport.onConnect(connector_profile.connector_id, publisher)

    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief Interface ����³��������
  #
  # ���Υ��ڥ졼�����ϡ�notify_disconnect() �����������󥹤ν����˥�����
  # �����ؿ��Ǥ��롣
  # notify_disconnect() �Ǥϡ�
  # - disconnectNext()
  # - unsubscribeInterfaces()
  # - eraseConnectorProfile()
  # �ν�� protected �ؿ��������뤵����³����������Ԥ��롣
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @else
  #
  # @brief Disconnect interface connection
  #
  # This operation is pure virutal method that would be called at the
  # end of the notify_disconnect() process sequence.
  # In the notify_disconnect(), the following methods would be called.
  # - disconnectNext()
  # - unsubscribeInterfaces()
  # - eraseConnectorProfile() 
  #
  # @param connector_profile The connection profile information
  #
  # @endif
  def unsubscribeInterfaces(self, connector_profile):
    publisher = self._outport.detach(connector_profile.connector_id)
    self._pf.destroy(publisher)
    self._outport.onDisconnect(connector_profile.connector_id)
    return



  ##
  # @if jp
  # @brief Interface��³��Functor
  #
  # Interface��³������¹Ԥ��뤿���Functor��
  # @else
  #
  # @endif
  class subscribe:
    
    
    
    def __init__(self, prof=None, subs=None):
      """
       \brief functor
       \param prof(RTC.ConnectorProfile)
       \param subs(subscribe)
      """
      if prof and not subs:
        self._prof = prof
        self._consumer = None
      elif not prof and subs:
        self._prof = subs._prof
        self._consumer = subs._consumer
      else:
        print "DataOutPort.subscribe: Invalid parameter."


    def __call__(self, cons):
      """
       \brief operator()�μ���
       \param cons(OpenRTM_aist.InPortConsumer)
      """
      if cons.subscribeInterface(self._prof.properties):
        self._consumer = cons
