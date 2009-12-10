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
    #InPortPushConnector(Profile profile, InPortProvider* provider,
    #                    CdrBufferBase* buffer = 0);
    def __init__(self, profile, provider, buffer = 0):
        OpenRTM_aist.InPortConnector.__init__(self, profile, buffer)
        self._provider = provider
        if buffer:
            self._deleteBuffer = True
        else:
            self._deleteBuffer = False

        if self._buffer == 0:
            self._buffer = self.createBuffer(profile)

        if self._buffer == 0:
            raise

        self._provider.init(profile.properties)
        self._provider.setBuffer(self._buffer)

    
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
        self.disconnect()


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
            return OpenRTM_aist.DataPortStatus.PORT_OK

        elif ret == OpenRTM_aist.BufferStatus.BUFFER_EMPTY:
            return OpenRTM_aist.DataPortStatus.BUFFER_EMPTY

        elif ret == OpenRTM_aist.BufferStatus.TIMEOUT:
            return OpenRTM_aist.DataPortStatus.BUFFER_TIMEOUT

        elif ret == OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET:
            return OpenRTM_aist.DataPortStatus.PRECONDITION_NOT_MET

        return OpenRTM_aist.DataPortStatus.PORT_ERROR
        

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

        return OpenRTM_aist.DataPortStatus.PORT_OK

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
        if not self._endian:
            return OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET

        elif self._endian == "little":
            _data = cdrUnmarshal(any.to_any(self._dataType).typecode(),data,1)

        elif self._endian == "big":
            _data = cdrUnmarshal(any.to_any(self._dataType).typecode(),data,0)
        else:
            self._rtcout.RTC_ERROR("unknown endian from connector")
            return OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET

        self._buffer.write(_data)
        return OpenRTM_aist.BufferStatus.BUFFER_OK

        
