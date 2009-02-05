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
