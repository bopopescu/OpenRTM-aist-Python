#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file  OutPortCorbaCdrConsumer.py
# @brief OutPortCorbaCdrConsumer class
# @date  $Date: 2008-01-13 10:28:27 $
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

import sys
from omniORB import any
import OpenRTM_aist
import OpenRTM, OpenRTM__POA

##
# @if jp
# @class OutPortCorbaCdrConsumer
#
# @brief OutPortCorbaCdrConsumer ���饹
#
# �̿����ʤ� CORBA �����Ѥ������ϥݡ��ȥ��󥷥塼�ޤμ������饹��
#
# @param DataType �ܥݡ��Ȥˤư����ǡ�����
#
# @since 0.4.0
#
# @else
# @class OutPortCorbaCdrConsumer
#
# @brief OutPortCorbaCdrConsumer class
#
# This is an implementation class of the output Consumer 
# that uses CORBA for means of communication.
#
# @param DataType Data type for this port
#
# @since 0.4.0
#
# @endif
#
class OutPortCorbaCdrConsumer(OpenRTM_aist.OutPortConsumer,OpenRTM_aist.CorbaConsumer):

    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    #
    # @param buffer �ܥݡ��Ȥ˳�����Ƥ�Хåե�
    #
    # @else
    # @brief Constructor
    #
    # Constructor
    #
    # @param buffer Buffer that is attached to this port
    #
    # @endif
    #
    def __init__(self):
        OpenRTM_aist.CorbaConsumer.__init__(self)
        self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("OutPortCorbaCdrConsumer")
        self._buffer = None
        pass

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
    # OutPortConsumer�γƼ������Ԥ����������饹�Ǥϡ�Ϳ����줿
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
    # OutPortConsumer���ǡ�������Ф��Хåե��򥻥åȤ��롣
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
    # virtual void setBuffer(CdrBufferBase* buffer);
    def setBuffer(self, buffer):
        self._buffer = buffer
        return

    ##
    # @if jp
    # @brief �ǡ������ɤ߽Ф�
    #
    # ���ꤵ�줿�ǡ������ɤ߽Ф���
    #
    # @param data �ɤ߽Ф����ǡ����������륪�֥�������
    #
    # @return �ǡ����ɤ߽Ф��������(�ɤ߽Ф�����:true���ɤ߽Ф�����:false)
    #
    # @else
    # @brief Read data
    #
    # Read set data
    #
    # @param data Object to receive the read data
    #
    # @return Read result (Successful:true, Failed:false)
    #
    # @endif
    #
    # virtual ReturnCode get(cdrMemoryStream& data);
    def get(self, data):
        self._rtcout.RTC_PARANOID("get()")

        try:
            ret,cdr_data = self._ptr().get()
            
            if ret == OpenRTM.PORT_OK:
                data[0] = cdr_data
                self._buffer.put(data[0])
                self._buffer.advanceWptr()
                self._buffer.advanceRptr()

                return OpenRTM_aist.DataPortStatus.PORT_OK
            return ret

        except:
            return OpenRTM_aist.DataPortStatus.CONNECTION_LOST

        return OpenRTM_aist.DataPortStatus.UNKNOWN_ERROR


    ##
    # @if jp
    # @brief �ǡ����������Τؤ���Ͽ
    #
    # ���ꤵ�줿�ץ�ѥƥ��˴�Ť��ơ��ǡ����������Τμ���������Ͽ���롣
    #
    # @param properties ��Ͽ����
    #
    # @return ��Ͽ�������(��Ͽ����:true����Ͽ����:false)
    #
    # @else
    # @brief Subscribe the data receive notification
    #
    # Subscribe the data receive notification based on specified property
    # information
    #
    # @param properties Subscription information
    #
    # @return Subscription result (Successful:true, Failed:false)
    #
    # @endif
    #
    # virtual bool subscribeInterface(const SDOPackage::NVList& properties);
    def subscribeInterface(self, properties):
        self._rtcout.RTC_TRACE("subscribeInterface()")
        index = OpenRTM_aist.NVUtil.find_index(properties,"dataport.corba_cdr.outport_ior")
        
        if index < 0:
            return False

        if OpenRTM_aist.NVUtil.isString(properties,"dataport.corba_cdr.outport_ior"):
            ior = ""
            try:
                ior = any.from_any(properties[index].value, keep_structs=True)
            except:
                #traceback.print_exception(*sys.exc_info())
                self._rtcout.RTC_ERROR(sys.exc_info()[0])
            
            orb = OpenRTM_aist.Manager.instance().getORB()
            obj = orb.string_to_object(ior)
            self.setObject(obj)
            return True

        return False


    ##
    # @if jp
    # @brief �ǡ����������Τ������Ͽ���
    #
    # �ǡ����������Τμ�����꤫����Ͽ�������롣
    #
    # @param properties ��Ͽ�������
    #
    # @else
    # @brief Unsubscribe the data receive notification
    #
    # Unsubscribe the data receive notification.
    #
    # @param properties Unsubscription information
    #
    # @endif
    #
    # virtual void unsubscribeInterface(const SDOPackage::NVList& properties);
    def unsubscribeInterface(self, properties):
        self._rtcout.RTC_TRACE("unsubscribeInterface()")
        index = OpenRTM_aist.NVUtil.find_index(properties,
                                               "dataport.corba_cdr.outport_ref")
        if index < 0:
            return
    
            ior = ""
            try:
                ior = any.from_any(properties[index].value, keep_structs=True)
                
                if ior:
                    orb = OpenRTM_aist.Manager.instance().getORB()
                    obj = orb.string_to_object(ior)
                    if self._ptr()._is_equivalent(obj):
                        self.releaseObject()

            except:
                #traceback.print_exception(*sys.exc_info())
                self._rtcout.RTC_ERROR(sys.exc_info()[0])

    
def OutPortCorbaCdrConsumerInit():
    factory = OpenRTM_aist.OutPortConsumerFactory.instance()
    factory.addFactory("corba_cdr",
                       OpenRTM_aist.OutPortCorbaCdrConsumer,
                       OpenRTM_aist.Delete)
