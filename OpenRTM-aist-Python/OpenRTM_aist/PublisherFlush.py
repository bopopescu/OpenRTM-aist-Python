#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherFlush.py
# @brief PublisherFlush class
# @date  $Date: 2007/09/06$
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


##
# @if jp
# @class PublisherFlush
# @brief PublisherFlush ���饹
#
# Flush �� Publisher ���饹
# �Хåե���˳�Ǽ����Ƥ���̤�����ǡ������������롣
# �ǡ������Ф��Ԥĥ��󥷥塼�ޤ����Ф���¦��Ʊ������åɤ�ư����롣
#
# @else
# @class PublisherFlush
# @brief PublisherFlush class
# @endif
class PublisherFlush(OpenRTM_aist.PublisherBase):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param consumer �ǡ������Ф��Ԥĥ��󥷥塼��
  # @param property ��Publisher�ζ�ư�����������ꤷ��Property���֥�������
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("PublisherFlush")
    self._consumer  = None
    self._active    = False
    self._profile   = None # ConnectorInfo
    self._listeners = None # ConnectorListeners


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  # ����Publisher���˴�����ݤˡ�PublisherFactory�ˤ��ƤӽФ���롣
  #
  # @param self
  #
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    # "consumer" should be deleted in the Connector
    self._rtcout.RTC_TRACE("~PublisherFlush()")
    self._consumer = None


  ##
  # @if jp
  # @brief �����
  # @else
  # @brief initialization
  # @endif
  # PublisherBase::ReturnCode PublisherFlush::init(coil::Properties& prop)
  def init(self, prop):
    self._rtcout.RTC_TRACE("init()")
    return self.PORT_OK;


  ##
  # @if jp
  # @brief InPort���󥷥塼�ޤΥ��å�
  # @else
  # @brief Store InPort consumer
  # @endif
  # PublisherBase::ReturnCode
  # PublisherFlush::setConsumer(InPortConsumer* consumer)
  def setConsumer(self, consumer):
    self._rtcout.RTC_TRACE("setConsumer()")
    if not consumer:
      return self.INVALID_ARGS

    self._consumer = consumer

    return self.PORT_OK


  ##
  # @if jp
  # @brief �Хåե��Υ��å�
  # @else
  # @brief Setting buffer pointer
  # @endif
  # PublisherBase::ReturnCode PublisherFlush::setBuffer(CdrBufferBase* buffer)
  def setBuffer(self, buffer):
    self._rtcout.RTC_TRACE("setBuffer()")
    return self.PORT_ERROR


  ##
  # @if jp
  # @brief �ꥹ�ʤΥ��å�
  # @else
  # @brief Setting buffer pointer
  # @endif
  #
  # virtual ::RTC::DataPortStatus::Enum
  # setListener(ConnectorInfo& info,
  #             RTC::ConnectorListeners* listeners);
  def setListener(self, info, listeners):
    self._rtcout.RTC_TRACE("setListeners()")
    
    if not listeners:
      self._rtcout.RTC_ERROR("setListeners(listeners == 0): invalid argument")
      return self.INVALID_ARGS

    self._profile = info
    self._listeners = listeners

    return self.PORT_OK


  ## PublisherBase::ReturnCode PublisherFlush::write(const cdrMemoryStream& data,
  ##                                                 unsigned long sec,
  ##                                                 unsigned long usec)
  def write(self, data, sec, usec):
    self._rtcout.RTC_PARANOID("write()")
    if not self._consumer or not self._listeners:
      return self.PRECONDITION_NOT_MET

    self.onSend(data)

    ret = self._consumer.put(data)

    if ret == self.PORT_OK:
      self.onReceived(data)
      return ret
    elif ret == self.PORT_ERROR:
      self.onReceiverError(data)
      return ret
    elif ret == self.SEND_FULL:
      self.onReceiverFull(data)
      return ret
    elif ret == self.SEND_TIMEOUT:
      self.onReceiverTimeout(data)
      return ret
    elif ret == self.UNKNOWN_ERROR:
      self.onReceiverError(data)
      return ret
    else:
      self.onReceiverError(data)
      return ret

    return ret


  ## bool PublisherFlush::isActive()
  def isActive(self):
    return self._active


  ## PublisherBase::ReturnCode PublisherFlush::activate()
  def activate(self):
    if self._active:
      return self.PRECONDITION_NOT_MET

    self._active = True

    return self.PORT_OK


  ## PublisherBase::ReturnCode PublisherFlush::deactivate()
  def deactivate(self):
    if not self._active:
      return self.PRECONDITION_NOT_MET

    self._active = False

    return self.PORT_OK

  ##
  # @brief Connector data listener functions
  #

  # inline void onSend(const cdrMemoryStream& data)
  def onSend(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_SEND].notify(self._profile, data)
    return

  # inline void onReceived(const cdrMemoryStream& data)
  def onReceived(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED].notify(self._profile, data)
    return

  # inline void onReceiverFull(const cdrMemoryStream& data)
  def onReceiverFull(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_FULL].notify(self._profile, data)
    return

  # inline void onReceiverTimeout(const cdrMemoryStream& data)
  def onReceiverTimeout(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_TIMEOUT].notify(self._profile, data)
    return

  # inline void onReceiverError(const cdrMemoryStream& data)
  def onReceiverError(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_ERROR].notify(self._profile, data)
    return
  

def PublisherFlushInit():
  OpenRTM_aist.PublisherFactory.instance().addFactory("flush",
                                                      OpenRTM_aist.PublisherFlush,
                                                      OpenRTM_aist.Delete)
