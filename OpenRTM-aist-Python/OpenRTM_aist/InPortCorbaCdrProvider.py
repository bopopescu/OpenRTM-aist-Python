#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  InPortCorbaCdrProvider.py
# @brief InPortCorbaCdrProvider class
# @date  $Date: 2008-01-14 07:49:59 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import sys
from omniORB import *
from omniORB import any

import OpenRTM_aist
import OpenRTM__POA,OpenRTM

##
# @if jp
# @class InPortCorbaCdrProvider
# @brief InPortCorbaCdrProvider ���饹
#
# �̿����ʤ� CORBA �����Ѥ������ϥݡ��ȥץ�Х������μ������饹��
#
# @param DataType �����ץ�Х����˳�����Ƥ��Хåե����ݻ�����ǡ�����
#
# @since 0.4.0
#
# @else
# @class InPortCorbaCdrProvider
# @brief InPortCorbaCdrProvider class
#
# This is an implementation class of the input port Provider 
# that uses CORBA for means of communication.
#
# @param DataType Data type held by the buffer that attached 
#                 to this provider.
#
# @since 0.4.0
#
# @endif
#
class InPortCorbaCdrProvider(OpenRTM_aist.InPortProvider,
                             OpenRTM__POA.InPortCdr):
    
    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    # �ݡ��ȥץ�ѥƥ��˰ʲ��ι��ܤ����ꤹ�롣
    #  - ���󥿡��ե����������� : CORBA_Any
    #  - �ǡ����ե������� : Push, Pull
    #  - ���֥�����ץ���󥿥��� : Any
    #
    # @param buffer �����ץ�Х����˳�����Ƥ�Хåե����֥�������
    #
    # @else
    # @brief Constructor
    #
    # Constructor
    # Set the following items to port properties
    #  - Interface type : CORBA_Any
    #  - Data flow type : Push, Pull
    #  - Subscription type : Any
    #
    # @param buffer Buffer object that is attached to this provider
    #
    # @endif
    #
    def __init__(self):
        OpenRTM_aist.InPortProvider.__init__(self)

        # PortProfile setting
        self.setInterfaceType("corba_cdr")
    
        # ConnectorProfile setting
        self._objref = self._this()

        self._buffer = None

        # set InPort's reference
        orb = OpenRTM_aist.Manager.instance().getORB()

        self._properties.append(OpenRTM_aist.NVUtil.newNV("dataport.corba_cdr.inport_ior",
                                                          orb.object_to_string(self._objref)))
        self._properties.append(OpenRTM_aist.NVUtil.newNV("dataport.corba_cdr.inport_ref",
                                                          self._objref))

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
        oid = OpenRTM_aist.Manager.instance().getPOA.servant_to_id(self)
        OpenRTM_aist.Manager.instance().getPOA.deactivate_object(oid)


    ## virtual void init(coil::Properties& prop);
    def init(self, prop):
        pass

    ## virtual void setBuffer(BufferBase<cdrMemoryStream>* buffer);
    def setBuffer(self, buffer):
        self._buffer = buffer

    ##
    # @if jp
    # @brief [CORBA interface] �Хåե��˥ǡ�����񤭹���
    #
    # ���ꤵ�줿�Хåե��˥ǡ�����񤭹��ࡣ
    #
    # @param data ����оݥǡ���
    #
    # @else
    # @brief [CORBA interface] Write data into the buffer
    #
    # Write data into the specified buffer.
    #
    # @param data The target data for writing
    #
    # @endif
    #
    #virtual ::OpenRTM::PortStatus put(const ::OpenRTM::CdrData& data)
    #  throw (CORBA::SystemException);
    def put(self, data):
        try:
            self._rtcout.RTC_PARANOID("put()")

            if not self._buffer:
                return OpenRTM.PORT_ERROR

            if self._buffer.full():
                self._rtcout.RTC_WARN("buffer full")
                return OpenRTM.BUFFER_FULL

            self._rtcout.RTC_PARANOID("received data size: %d", len(data))

            # ret = self._buffer.write(data)
            if not self._connector:
                return OpenRTM.PORT_ERROR
            ret = self._connector.write(data)

            if ret == OpenRTM_aist.BufferStatus.BUFFER_OK:
                return OpenRTM.PORT_OK
            
            elif ret == OpenRTM_aist.BufferStatus.BUFFER_ERROR:
                return OpenRTM.PORT_ERROR

            elif ret == OpenRTM_aist.BufferStatus.BUFFER_FULL:
                return OpenRTM.BUFFER_FULL

            elif ret == OpenRTM_aist.BufferStatus.BUFFER_EMPTY:
                return OpenRTM.BUFFER_EMPTY

            elif ret == OpenRTM_aist.BufferStatus.TIMEOUT:
                return OpenRTM.BUFFER_TIMEOUT
        except:
            self._rtcout.RTC_TRACE(sys.exc_info()[0])
            return OpenRTM.UNKNOWN_ERROR
        return OpenRTM.UNKNOWN_ERROR


def InPortCorbaCdrProviderInit():
    factory = OpenRTM_aist.InPortProviderFactory.instance()
    factory.addFactory("corba_cdr",
                       OpenRTM_aist.InPortCorbaCdrProvider,
                       OpenRTM_aist.Delete)
