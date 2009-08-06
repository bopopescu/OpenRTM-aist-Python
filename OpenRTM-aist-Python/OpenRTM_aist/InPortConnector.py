#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file InPortConnector.py
# @brief InPortConnector base class
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

import OpenRTM_aist


##
# @if jp
# @class InPortConnector
# @brief InPortConnector ���쥯�饹
#
# InPort �� Push/Pull �Ƽ� Connector �����������뤿���
# ���쥯�饹��
#
# @since 1.0.0
#
# @else
# @class InPortConnector
# @brief I��PortConnector base class
#
# The base class to derive subclasses for InPort's Push/Pull Connectors
#
# @since 1.0.0
#
# @endif
#
class InPortConnector(OpenRTM_aist.ConnectorBase):
    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    # @else
    # @brief Constructor
    # @endif
    #
    def __init__(self, profile, buffer):
        self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("InPortConnector")
        self._profile = profile
        self._buffer = buffer


    ##
    # @if jp
    # @brief �ǥ��ȥ饯��
    # @else
    # @brief Destructor
    # @endif
    #
    def __del__(self):
        pass

    ##
    # @if jp
    # @brief Profile ����
    #
    # Connector Profile ���������
    #
    # @else
    # @brief Getting Profile
    #
    # This operation returns Connector Profile
    #
    # @endif
    #
    # const Profile& profile();
    def profile(self):
        self._rtcout.RTC_TRACE("profile()")
        return self._profile


    ##
    # @if jp
    # @brief Connector ID ����
    #
    # Connector ID ���������
    #
    # @else
    # @brief Getting Connector ID
    #
    # This operation returns Connector ID
    #
    # @endif
    #
    # const char* id();
    def id(self):
        self._rtcout.RTC_TRACE("id() = %s", self.profile().id)
        return self.profile().id


    ##
    # @if jp
    # @brief Connector ̾����
    #
    # Connector ̾���������
    #
    # @else
    # @brief Getting Connector name
    #
    # This operation returns Connector name
    #
    # @endif
    #
    # const char* name();
    def name(self):
        self._rtcout.RTC_TRACE("name() = %s", self.profile().name)
        return self.profile().name


    ##
    # @if jp
    # @brief ��³����ؿ�
    #
    # Connector ���ݻ����Ƥ�����³��������
    #
    # @else
    # @brief Disconnect connection
    #
    # This operation disconnect this connection
    #
    # @endif
    #
    # virtual ReturnCode disconnect() = 0;
    def disconnect(self):
        pass

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
    # @brief read �ؿ�
    #
    # Buffer ����ǡ����� InPort �� read ����ؿ�
    #
    # @else
    # @brief Destructor
    #
    # The read function to read data from buffer to InPort
    #
    # @endif
    #
    # virtual ReturnCode read(cdrMemoryStream& data) = 0;
    def read(self, data):
        pass
