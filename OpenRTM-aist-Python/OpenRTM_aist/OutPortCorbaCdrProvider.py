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
        pass


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
        if not self._buffer:
            return (OpenRTM.UNKNOWN_ERROR, None)

        if self._buffer.empty():
            return (OpenRTM.BUFFER_EMPTY, None)

        cdr = [None]
        ret = self._buffer.read(cdr)

        if ret == 0:
            return (OpenRTM.PORT_OK, cdr[0])

        return (ret, None)
    


def OutPortCorbaCdrProviderInit():
    factory = OpenRTM_aist.OutPortProviderFactory.instance()
    factory.addFactory("corba_cdr",
                       OpenRTM_aist.OutPortCorbaCdrProvider,
                       OpenRTM_aist.Delete)


