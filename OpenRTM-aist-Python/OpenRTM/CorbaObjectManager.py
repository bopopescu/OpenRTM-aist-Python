#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# \file CorbaObjectManager.py
# \brief CORBA Object manager class
# \date $Date: 2007/08/27$
# \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


from omniORB import CORBA, PortableServer

import OpenRTM


##
# @if jp
# @class CorbaObjectManager
# @brief CORBA ���֥������Ȥ򥢥��ƥ��ֲ����󥢥��ƥ��ֲ�����
#
# RTObject�Υ����ƥ��ֲ����󥢥��ƥ��ֲ���Ԥ����饹�Ǥ��롣
# �ݻ����Ƥ���ORB��POA���Ѥ��� CORBA ���֥������ȤΥ����ƥ��ֲ���
# �󥢥��ƥ��ֲ���Ԥ���
#
# @since 0.4.0
#
# @else
# @class CorbaObjectManager
# @brief Activate and deactivate CORBA objects
# @endif
class CorbaObjectManager:
  """
  """



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # @param self
  # @param orb ORB
  # @param poa POA
  #
  # @else
  #
  # @brief Consructor
  #
  # @param orb ORB
  #
  # @endif
  def __init__(self, orb, poa):
    self._orb = orb
    self._poa = poa


  ##
  # @if jp
  # @brief CORBA ���֥������Ȥ򥢥��ƥ��ֲ�����
  #
  # ���ꤵ�줿RTObject�� CORBA ���֥������ȤȤ��ƥ����ƥ��ֲ�����
  # ���֥������ȥ�ե���󥹤����ꤹ�롣
  #
  # @param self
  # @param comp �����ƥ��ֲ��о�RTObject
  #
  # @else
  # @brief Activate CORBA object
  # @endif
  def activate(self, comp):
    id_ = self._poa.activate_object(comp)
    obj = self._poa.id_to_reference(id_)
    comp.setObjRef(obj._narrow(OpenRTM.RTObject_impl))


  ##
  # @if jp
  # @brief CORBA ���֥������Ȥ��󥢥��ƥ��ֲ�����
  #
  # ���ꤵ�줿RTObject���󥢥��ƥ��ֲ���Ԥ�
  #
  # @param self
  # @param comp �󥢥��ƥ��ֲ��о�RTObject
  #
  # @else
  # @brief Deactivate CORBA object
  # @endif
  def deactivate(self, comp):
    id_ = self._poa.servant_to_id(comp)
    self._poa.deactivate_object(id_)
