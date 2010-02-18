#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortCorbaProvider.py
# @brief OutPortCorbaProvider class
# @date  $Date: 2008-01-14 07:52:40 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import sys
from omniORB import *
from omniORB import any

import OpenRTM_aist
import OpenRTM__POA,OpenRTM

##
# @if jp
# @class OutPortCorbaCdrProvider
# @brief OutPortCorbaCdrProvider ���饹
#
# �̿����ʤ� CORBA �����Ѥ������ϥݡ��ȥץ�Х������μ������饹��
#
# @param DataType �����ץ�Х����˳�����Ƥ��Хåե����ݻ�����ǡ�����
#
# @since 0.4.0
#
# @else
# @class OutPortCorbaCdrProvider
# @brief OutPortCorbaCdrProvider class
#
# This is an implementation class of OutPort Provider that uses 
# CORBA for mean of communication.
#
# @param DataType Data type held by the buffer that is assigned to this 
#        provider
#
# @since 0.4.0
#
# @endif
#
class OutPortCorbaCdrProvider(OpenRTM_aist.OutPortProvider,
                              OpenRTM__POA.OutPortCdr):
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param buffer �����ץ�Х����˳�����Ƥ�Хåե����֥�������
  #
  # @else
  # @brief Constructor
  #
  # Constructor
  #
  # @param buffer Buffer object that is assigned to this provider
  #
  # @endif
  #
  def __init__(self):
    OpenRTM_aist.OutPortProvider.__init__(self)
    self.setInterfaceType("corba_cdr")

    # ConnectorProfile setting
    self._objref = self._this()
    
    self._buffer = None

    # set outPort's reference
    orb = OpenRTM_aist.Manager.instance().getORB()

    self._properties.append(OpenRTM_aist.NVUtil.newNV("dataport.corba_cdr.outport_ior",
                                                      orb.object_to_string(self._objref)))
    self._properties.append(OpenRTM_aist.NVUtil.newNV("dataport.corba_cdr.outport_ref",
                                                      self._objref))

    self._listeners = None
    self._connector = None
    return


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @else
  # @brief Destructor
  #
  # Destructor
  #
  # @endif
  #
  def __del__(self):
    oid = self._default_POA().servant_to_id(self)
    self._default_POA().deactivate_object(oid)
    return


  ##
  # @if jp
  # @brief ��������
  #
  # InPortConsumer�γƼ������Ԥ����������饹�Ǥϡ�Ϳ����줿
  # Properties����ɬ�פʾ����������ƳƼ������Ԥ������� init() ��
  # ���ϡ�OutPortProvider����ľ�太��ӡ���³���ˤ��줾��ƤФ���
  # ǽ�������롣�������äơ����δؿ���ʣ����ƤФ�뤳�Ȥ����ꤷ�Ƶ�
  # �Ҥ����٤��Ǥ��롣
  # 
  # @param prop �������
  #
  # @else
  #
  # @brief Initializing configuration
  #
  # This operation would be called to configure in initialization.
  # In the concrete class, configuration should be performed
  # getting appropriate information from the given Properties data.
  # This function might be called right after instantiation and
  # connection sequence respectivly.  Therefore, this function
  # should be implemented assuming multiple call.
  #
  # @param prop Configuration information
  #
  # @endif
  #
  # virtual void init(coil::Properties& prop);
  def init(self, prop):
    pass


  ##
  # @if jp
  # @brief �Хåե��򥻥åȤ���
  #
  # OutPortProvider���ǡ�������Ф��Хåե��򥻥åȤ��롣
  # ���Ǥ˥��åȤ��줿�Хåե��������硢�����ΥХåե��ؤ�
  # �ݥ��󥿤��Ф��ƾ�񤭤���롣
  # OutPortProvider�ϥХåե��ν�ͭ�����ꤷ�Ƥ��ʤ��Τǡ�
  # �Хåե��κ���ϥ桼������Ǥ�ǹԤ�ʤ���Фʤ�ʤ���
  #
  # @param buffer OutPortProvider���ǡ�������Ф��Хåե��ؤΥݥ���
  #
  # @else
  # @brief Setting outside buffer's pointer
  #
  # A pointer to a buffer from which OutPortProvider retrieve data.
  # If already buffer is set, previous buffer's pointer will be
  # overwritten by the given pointer to a buffer.  Since
  # OutPortProvider does not assume ownership of the buffer
  # pointer, destructor of the buffer should be done by user.
  # 
  # @param buffer A pointer to a data buffer to be used by OutPortProvider
  #
  # @endif
  #
  # virtual void setBuffer(BufferBase<cdrMemoryStream>* buffer);
  def setBuffer(self, buffer):
    self._buffer = buffer
    return


  ##
  # @if jp
  # @brief �ꥹ�ʤ����ꤹ�롣
  # @else
  # @brief Set the listener. 
  # @endif
  #
  # virtual void setListener(ConnectorInfo& info,
  #                          ConnectorListeners* listeners);
  def setListener(self, info, listeners):
    self._profie = info
    self._listeners = listeners
    return


  ##
  # @if jp
  # @brief Connector�����ꤹ�롣
  # @else
  # @brief set Connector
  # @endif
  #
  # virtual void setConnector(OutPortConnector* connector);
  def setConnector(self, connector):
    self._connector = connector
    return


  ##
  # @if jp
  # @brief [CORBA interface] �Хåե�����ǡ������������
  #
  # ���ꤵ�줿�����Хåե�����ǡ�����������롣
  #
  # @return �����ǡ���
  #
  # @else
  # @brief [CORBA interface] Get data from the buffer
  #
  # Get data from the internal buffer.
  #
  # @return Data got from the buffer.
  #
  # @endif
  #
  # virtual ::OpenRTM::PortStatus get(::OpenRTM::CdrData_out data);
  def get(self):
    self._rtcout.RTC_PARANOID("OutPortCorbaCdrProvider.get()")
    if not self._buffer:
      self.onSenderError()
      return (OpenRTM.UNKNOWN_ERROR, None)

    try:
      if self._buffer.empty():
        self._rtcout.RTC_ERROR("buffer is empty.")
        return (OpenRTM.BUFFER_EMPTY, None)

      cdr = [None]
      ret = self._buffer.read(cdr)
      
    except:
      self._rtcout.RTC_TRACE(sys.exc_info()[0])
      return (OpenRTM.UNKNOWN_ERROR, None)

    return self.convertReturn(ret, cdr)
    

  # inline void onBufferRead(const cdrMemoryStream& data)
  def onBufferRead(self, data):
    self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_READ].notify(self._profile, data)
    return


  # inline void onSend(const cdrMemoryStream& data)
  def onSend(self, data):
    self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_SEND].notify(self._profile, data)
    return

  ##
  # @brief Connector listener functions
  #
  # inline void onBufferEmpty()
  def onBufferEmpty(self):
    self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_BUFFER_EMPTY].notify(self._profile)
    return


  # inline void onBufferReadTimeout()
  def onBufferReadTimeout(self):
    self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_BUFFER_READ_TIMEOUT].notify(self._profile)
    return

  # inline void onSenderEmpty()
  def onSenderEmpty(self):
    self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_EMPTY].notify(self._profile)
    return

  # inline void onSenderTimeout()
  def onSenderTimeout(self):
    self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_TIMEOUT].notify(self._profile)
    return

  # inline void onSenderError()
  def onSenderError(self):
    self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_ERROR].notify(self._profile)
    return


  ##
  # @if jp
  # @brief �꥿���󥳡����Ѵ�
  # @else
  # @brief Return codes conversion
  # @endif
  #
  # ::OpenRTM::PortStatus convertReturn(BufferStatus::Enum status,
  #                                     const cdrMemoryStream& data);
  def convertReturn(self, status, data):
    if status == OpenRTM_aist.BufferStatus.BUFFER_OK:
      self.onBufferRead(data)
      self.onSend(data)
      return (OpenRTM.PORT_OK, data[0])
    
    elif status == OpenRTM_aist.BufferStatus.BUFFER_ERROR:
      self.onSenderError()
      return (OpenRTM.PORT_ERROR, data[0])
    
    elif status == OpenRTM_aist.BufferStatus.BUFFER_FULL:
      # never come here
      return (OpenRTM.BUFFER_FULL, data[0])

    elif status == OpenRTM_aist.BufferStatus.BUFFER_EMPTY:
      self.onBufferEmpty()
      self.onSenderEmpty()
      return (OpenRTM.BUFFER_EMPTY, data[0])

    elif status == OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET:
      self.onSenderError()
      return (OpenRTM.PORT_ERROR, data[0])
    
    elif status == OpenRTM_aist.BufferStatus.TIMEOUT:
      self.onBufferReadTimeout()
      self.onSenderTimeout()
      return (OpenRTM.BUFFER_TIMEOUT, data[0])
    
    else:
      return (OpenRTM.UNKNOWN_ERROR, data[0])
    
    self.onSenderError()
    return (OpenRTM.UNKNOWN_ERROR, data[0])


def OutPortCorbaCdrProviderInit():
  factory = OpenRTM_aist.OutPortProviderFactory.instance()
  factory.addFactory("corba_cdr",
                     OpenRTM_aist.OutPortCorbaCdrProvider,
                     OpenRTM_aist.Delete)
