#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
#
# @file InPortPushConnector.py
# @brief Push type connector class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara.
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
import sys

import OpenRTM_aist

class InPortPushConnector(OpenRTM_aist.InPortConnector):

    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # InPortPushConnector �� InPortConsumer �ν�ͭ������ġ�
    # �������äơ�InPortPushConnector ������ˤϡ�InPortConsumer��Ʊ����
    # ���Ρ��������롣
    #
    # @param profile ConnectorProfile
    # @param consumer InPortConsumer
    #
    # @else
    # @brief Constructor
    #
    # InPortPushConnector assume ownership of InPortConsumer.
    # Therefore, InPortConsumer will be deleted when InPortPushConnector
    # is destructed.
    #
    # @param profile ConnectorProfile
    # @param consumer InPortConsumer
    #
    # @endif
    #
    #InPortPushConnector(ConnectorInfo info, InPortProvider* provider,
    #                    ConnectorListeners listeners, CdrBufferBase* buffer = 0);
    def __init__(self, info, provider, listeners, buffer = 0):
        OpenRTM_aist.InPortConnector.__init__(self, info, buffer)
        self._provider = provider
        self._listeners = listeners

        if buffer:
            self._deleteBuffer = True
        else:
            self._deleteBuffer = False

        if self._buffer == 0:
            self._buffer = self.createBuffer(info)

        if self._buffer == 0:
            raise

        self._provider.init(info.properties)
        self._provider.setBuffer(self._buffer)
        self._provider.setListener(info, self._listeners)

        self.onConnect()
        return

    
    #
    # @if jp
    # @brief �ǥ��ȥ饯��
    #
    # disconnect() ���ƤФ졢consumer, publisher, buffer �����Ρ��������롣
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
        self.onDisconnect()
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
    # virtual ReturnCode read(cdrMemoryStream& data);
    def read(self, data):
        self._rtcout.RTC_TRACE("read()")

        ##
        # buffer returns
        #   BUFFER_OK
        #   BUFFER_EMPTY
        #   TIMEOUT
        #   PRECONDITION_NOT_MET
        #
        if type(data) == list:
            ret = self._buffer.read(data, 0, 0)
        else:
            tmp = [data]
            ret = self._buffer.read(tmp, 0, 0)
            
            
        if ret == OpenRTM_aist.BufferStatus.BUFFER_OK:
            return self.PORT_OK

        elif ret == OpenRTM_aist.BufferStatus.BUFFER_EMPTY:
            return self.BUFFER_EMPTY

        elif ret == OpenRTM_aist.BufferStatus.TIMEOUT:
            return self.BUFFER_TIMEOUT

        elif ret == OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET:
            return self.PRECONDITION_NOT_MET

        return self.PORT_ERROR
        

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
        # delete consumer
        if self._provider:
            cfactory = OpenRTM_aist.InPortProviderFactory.instance()
            cfactory.deleteObject(self._provider)

        self._provider = 0

        # delete buffer
        if self._buffer and self._deleteBuffer == True:
            bfactory = OpenRTM_aist.CdrBufferFactory.instance()
            bfactory.deleteObject(self._buffer)
    
        self._buffer = 0

        return self.PORT_OK

    ## virtual void activate(){}; // do nothing
    def activate(self): # do nothing
        pass

    ## virtual void deactivate(){}; // do nothing
    def deactivate(self):  # do nothing
        pass

    ##
    # @if jp
    # @brief Buffer������
    # @else
    # @brief create buffer
    # @endif
    #
    # virtual CdrBufferBase* createBuffer(Profile& profile);
    def createBuffer(self, profile):
        buf_type = profile.properties.getProperty("buffer_type","ring_buffer")
        return OpenRTM_aist.CdrBufferFactory.instance().createObject(buf_type)

    # ReturnCode write(const OpenRTM::CdrData& data);
    def write(self, data):

        if not self._dataType:
            return OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET

        _data = None
        # CDR -> (conversion) -> data
        if self._endian is not None:
            _data = cdrUnmarshal(any.to_any(self._dataType).typecode(),data,self._endian)

        else:
            self._rtcout.RTC_ERROR("unknown endian from connector")
            return OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET

        return self._buffer.write(_data)
        
    
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
