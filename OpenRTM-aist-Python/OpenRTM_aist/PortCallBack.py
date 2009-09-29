#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file PortCallBack.py
# @brief PortCallBack class
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
 

#============================================================
# callback functor base classes
#

##
# @if jp
# @class OnWrite
# @brief write() ���Υ�����Хå����饹(���֥��饹������)
#
# DataPort�ΥХåե��˥ǡ�����write()�����ľ���˸ƤӽФ���륳����Хå���<BR>
# �����֥��饹�Ǥμ���������
#
# @param DataType �Хåե��˽񤭹���ǡ�����
#
# @since 0.4.0
#
# @else
# @class OnPut
# @brief OnPut abstract class
#
# @endif
class OnWrite:
  def __call__(self, value):
    pass



##
# @if jp
# @class OnWriteConvert
# @brief write() ���Υǡ����Ѵ�������Хå����饹(���֥��饹������)
#
# InPort/OutPort�ΥХåե��˥ǡ����� write()�������˸ƤӽФ����<BR>
# �����֥��饹�Ǥμ���������
# ������Хå��ѥ��󥿡��ե�������
# ���Υ�����Хå�������ͤ��Хåե��˳�Ǽ����롣
#
# @since 0.4.0
#
# @else
# @class OnWriteConvert
# @brief OnWriteConvert abstract class
#
# @endif
class OnWriteConvert:
  def __call__(self,value):
    pass



##
# @if jp
# @class OnRead
# @brief read() ���Υ�����Хå����饹(���֥��饹������)
#
# InPort/OutPort�ΥХåե�����ǡ����� read()�����ľ���˸ƤӽФ����
# ������Хå��ѥ��󥿡��ե�������<BR>
# �����֥��饹�Ǥμ���������
#
# @since 0.4.0
#
# @else
# @class OnRead
# @brief OnRead abstract class
#
# @endif
class OnRead:
  def __call__(self):
    pass



##
# @if jp
# @class OnReadConvert
# @brief read() ���Υǡ����Ѵ�������Хå����饹(���֥��饹������)
#
# InPort/OutPort�ΥХåե�����ǡ����� read()�����ݤ˸ƤӽФ����
# ������Хå��ѥ��󥿡��ե�������
# ���Υ�����Хå�������ͤ�read()������ͤȤʤ롣<BR>
# �����֥��饹�Ǥμ���������
#
# @since 0.4.0
#
# @else
# @class OnReadConvert
# @brief OnReadConvert abstract class
#
# @endif
class OnReadConvert:
  def __call__(self,value):
    pass



##
# @if jp
# @class OnOverflow
# @brief �Хåե������С��ե����Υ�����Хå����饹(���֥��饹������)
#
# InPort/OutPort�ΥХåե��˥ǡ�����put()���������Хåե������С��ե���
# ���������˸ƤФ�륳����Хå��᥽�åɡ�<BR>
# �����֥��饹�Ǥμ���������
#
# @since 0.4.0
#
# @else
# @class OnOverflow
# @brief OnOverflow abstract class
#
# @endif
class OnOverflow:
  def __call__(self,value):
    pass


##
# @if jp
# @class OnUnderflow
# @brief Underflow ���Υ�����Хå����饹(���֥��饹������)
#
# @since 0.4.0
#
# InPort/OutPort�ΥХåե��˥ǡ�����read()�������ˡ��ɤ߽Ф��٤��ǡ�����
# �ʤ����˸ƤӽФ���륳����Хå����󥿥ե�������
# ���Υ�����Хå�������ͤ�read()������ͤȤʤ롣<BR>
# �����֥��饹�Ǥμ���������
#
# @else
# @class OnUnderflow
# @brief OnUnderflow abstract class
#
# @endif
class OnUnderflow:
  def __call__(self,value):
    pass


##
# @if jp
# @class OnWriteTimeout
# @brief �����ॢ���Ȼ��Υ�����Хå���ݥ��饹
#
# InPort/OutPort�ΥХåե��˥ǡ�����write()����ݤˡ������ॢ���Ȥ�ȯ������
# ���˸ƤӽФ���륳����Хå����󥿥ե�������
#
# @since 0.4.0
#
# @else
# @class OnWriteTimeout
# @brief Callback abstract class on timeout
#
# This is the interface for callback invoked when data is done write()
# into the InPort/OutPort's buffer and the timeout occurred.
#
# @since 0.4.0
#
# @endif
class OnWriteTimeout:
  ##
  # @if jp
  #
  # @brief ������Хå��᥽�å�
  #
  # �����ॢ����ȯ�����˸ƤӽФ���륳����Хå��᥽�å�
  #
  # @param value �Хåե��ؽ񤭹���ǡ���
  #
  # @else
  #
  # @brief Callback method
  #
  # This is the callback method invoked when the timeout occurs.
  #
  # @param value Data that is written into the buffer
  #
  # @endif
  # virtual void operator()(const DataType& value) = 0;
  def __call__(self, value):
    pass

  
##
# @if jp
# @class OnReadTimeout
# @brief �����ॢ���Ȼ��Υ�����Хå���ݥ��饹
#
# InPort/OutPort�ΥХåե��˥ǡ�����read()����ݤˡ������ॢ���Ȥ�ȯ������
# ���˸ƤӽФ���륳����Хå����󥿥ե�������
#
# @since 0.4.0
#
# @else
# @class OnReadTimeout
# @brief OnReadTimeout abstract class
#
# This is the interface for callback invoked when data is done read()
# into the InPort/OutPort's buffer and the timeout occurred.
#
# @since 0.4.0
#
# @endif
class OnReadTimeout:
  ##
  # @if jp
  #
  # @brief ������Хå��᥽�å�
  #
  # �����ॢ����ȯ�����˸ƤӽФ���륳����Хå��᥽�å�
  #
  # @return ���ؤȤʤ��ɤ߽Ф��ǡ���
  #
  # @else
  #
  # @brief Callback method
  #
  # This is the callback method invoked when the timeout occurs.
  #
  # @return Substituted readout data
  #
  # @endif
  # virtual DataType operator()() = 0;
  def __call__(self):
    pass


  #============================================================
  # callback functor base classes
  ##
  # @if jp
  # @class ConnectCallback
  # @brief connect/notify_connect() ���Υ�����Хå���ݥ��饹
  #
  # Port���Ф���connect/notify_connect() �����ƤӽФ������˸ƤӽФ����
  # ������Хå��ե��󥯥��������� RTC::ConnectorProfile ���롣
  #
  # @param profile ConnectorProfile
  #
  # @since 1.0.0
  #
  # @else
  # @class ConnectCallback
  # @brief Callback functor abstract for connect/notify_connect() funcs
  #
  # This is the interface for callback functor for connect/notify_connect()
  # invocation in Port. Argument is RTC::ConnectorProfile that is given
  # these functions.
  #
  # @param profile ConnectorProfile
  #
  # @since 1.0.0
  #
  # @endif
  #
  class ConnectionCallback:
    # virtual void operator()(RTC::ConnectorProfile& profile) = 0;
    def __call__(self, profile):
      pass

  ##
  # @if jp
  # @class DisconnectCallback
  # @brief disconnect/notify_disconnect() ���Υ�����Хå���ݥ��饹
  #
  # Port���Ф���disconnect/notify_disconnect() �����ƤӽФ������˸ƤӽФ����
  # ������Хå��ե��󥯥�����������³ID���롣
  #
  # @param connector_id Connector ID
  #
  # @since 1.0.0
  #
  # @else
  # @class DisconnectCallback
  # @brief Callback functor abstract for disconnect/notify_disconnect() funcs
  #
  # This is the interface for callback functor for 
  # disconnect/notify_disconnect() invocation in Port.
  # Argument is connector ID is given these functions.
  #
  # @param connector_id Connector ID
  #
  # @since 1.0.0
  #
  # @endif
  #
  class DisconnectCallback:
    #virtual void operator()(const char* connector_id) = 0;
    def __call__(self, connector_id):
      pass
