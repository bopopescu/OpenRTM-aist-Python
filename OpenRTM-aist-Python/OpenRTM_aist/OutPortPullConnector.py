#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file OutPortPullConnector.py
# @brief OutPortPull type connector class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

from omniORB import *
from omniORB import any

import OpenRTM_aist


class OutPortPullConnector(OpenRTM_aist.OutPortConnector):

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # OutPortPullConnector �� OutPortProvider �ν�ͭ������ġ�
  # �������äơ�OutPortPullConnector ������ˤϡ�OutPortProvider ��Ʊ����
  # ���Ρ��������롣
  #
  # @param profile pointer to a ConnectorProfile
  # @param provider pointer to an OutPortProvider
  # @param buffer pointer to a buffer
  #
  # @elsek
  # @brief Constructor
  #
  # OutPortPullConnector assume ownership of InPortConsumer.
  # Therefore, OutPortProvider will be deleted when OutPortPushConnector
  # is destructed.
  #
  # @param profile pointer to a ConnectorProfile
  # @param provider pointer to an OutPortProvider
  # @param buffer pointer to a buffer
  #
  # @endif
  #
  # OutPortPullConnector(ConnectorInfo info,
  #                      OutPortProvider* provider,
  #                      ConnectorListeners& listeners,
  #                      CdrBufferBase* buffer = 0);
  def __init__(self, info, provider, listeners, buffer = 0):
    OpenRTM_aist.OutPortConnector.__init__(self, info)
    self._provider = provider
    self._listeners = listeners
    self._buffer = buffer

    if not self._buffer:
      self._buffer = self.createBuffer(info)

    if not self._provider or not self._buffer:
      self._rtcout.RTC_ERROR("Exeption: in OutPortPullConnector.__init__().")
      raise

    self._buffer.init(info.properties.getNode("buffer"))
    self._provider.setBuffer(self._buffer)
    self._provider.setConnector(self)
    self._provider.setListener(info, self._listeners)
    self.onConnect()
    return


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # disconnect() ���ƤФ졢provider, buffer �����Ρ��������롣
  #
  # @else
  #
  # @brief Destructor
  #
  # This operation calls disconnect(), which destructs and deletes
  # the consumer, the publisher and the buffer.
  #
  # @endif
  #
  def __del__(self):
    self.onDisConnect()
    self.disconnect()
    return


  ##
  # @if jp
  # @brief �ǡ����ν񤭹���
  #
  # Publisher���Ф��ƥǡ�����񤭹��ߡ�����ˤ���б�����InPort��
  # �ǡ�����ž������롣
  #
  # @else
  #
  # @brief Writing data
  #
  # This operation writes data into publisher and then the data
  # will be transferred to correspondent InPort.
  #
  # @endif
  #
  # virtual ReturnCode write(const cdrMemoryStream& data);
  def write(self, data):
    # data -> (conversion) -> CDR stream
    cdr_data = None
    if self._endian is not None:
      cdr_data = cdrMarshal(any.to_any(data).typecode(), data, self._endian)
    else:
      self._rtcout.RTC_ERROR("write(): endian %s is not support.",self._endian)
      return self.UNKNOWN_ERROR
    
    self._buffer.write(cdr_data)
    return self.PORT_OK


  ##
  # @if jp
  # @brief ��³���
  #
  # consumer, publisher, buffer �����Ρ��������롣
  #
  # @else
  #
  # @brief disconnect
  #
  # This operation destruct and delete the consumer, the publisher
  # and the buffer.
  #
  # @endif
  #
  # virtual ReturnCode disconnect();
  def disconnect(self):
    return self.PORT_OK


  ##
  # @if jp
  # @brief Buffer ���������
  #
  # Connector ���ݻ����Ƥ��� Buffer ���֤�
  #
  # @else
  # @brief Getting Buffer
  #
  # This operation returns this connector's buffer
  #
  # @endif
  #
  # virtual CdrBufferBase* getBuffer();
  def getBuffer(self):
    return self._buffer


  ##
  # @if jp
  # @brief �����ƥ��ֲ�
  #
  # ���Υ��ͥ����򥢥��ƥ��ֲ�����
  #
  # @else
  #
  # @brief Connector activation
  #
  # This operation activates this connector
  #
  # @endif
  #
  # virtual void activate(){}; // do nothing
  def activate(self):  # do nothing
    pass


  ##
  # @if jp
  # @brief �󥢥��ƥ��ֲ�
  #
  # ���Υ��ͥ������󥢥��ƥ��ֲ�����
  #
  # @else
  #
  # @brief Connector deactivation
  #
  # This operation deactivates this connector
  #
  # @endif
  #
  # virtual void deactivate(){}; // do nothing
  def deactivate(self): # do nothing
    pass

    
  ##
  # @if jp
  # @brief Buffer������
  # @else
  # @brief create buffer
  # @endif
  #
  # CdrBufferBase* createBuffer(ConnectorInfo& info);
  def createBuffer(self, info):
    buf_type = info.properties.getProperty("buffer_type","ring_buffer")
    return OpenRTM_aist.CdrBufferFactory.instance().createObject(buf_type)


  ##
  # @if jp
  # @brief ��³��Ω���˥�����Хå���Ƥ�
  # @else
  # @brief Invoke callback when connection is established
  # @endif
  # void onConnect()
  def onConnect(self):
    self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_CONNECT].notify(self._profile)
    return


  ##
  # @if jp
  # @brief ��³���ǻ��˥�����Хå���Ƥ�
  # @else
  # @brief Invoke callback when connection is destroied
  # @endif
  # void onDisconnect()
  def onDisconnect(self):
    self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_DISCONNECT].notify(self._profile)
    return
