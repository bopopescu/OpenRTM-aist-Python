#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file PortAdmin.py
# @brief RTC's Port administration class
# @date $Date: 2007/09/03 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import traceback
import sys

import RTC, RTC__POA
import OpenRTM



##
# @if jp
# @class PortAdmin
# @brief PortAdmin ���饹
#
# �Ƽ� Port �δ�����Ԥ����饹��
# Port ����Ͽ/��Ͽ����ʤɳƼ��������¹Ԥ���ȤȤ�ˡ���Ͽ����Ƥ���
# Port �δ�����Ԥ����饹��
#
# @since 0.4.0
#
# @else
# @class PortAdmin
# @brief PortAdmin class
# @endif
class PortAdmin:
  """
  """



  ##
  # @if jp
  # @class comp_op
  # @brief Port �������������饹
  # @else
  #
  # @endif
  class comp_op:
    def __init__(self, name=None, factory=None):
      if name:
        self._name = name
      if factory:
        self._name = factory.getProfile().name

    def __call__(self, obj):
      name_ = obj.getProfile().name
      return self._name == name_


  ##
  # @if jp
  # @class find_port_name
  # @brief Port �����ѥե��󥯥�
  # @else
  # @endif
  class find_port_name:
    def __init__(self, name):
      self._name = name

    def __call__(self, p):
      prof = p.get_port_profile()
      name_ = prof.name 
      return self._name == name_


  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param orb ORB
  # @param poa POA
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, orb, poa):
    # ORB ���֥�������
    self._orb = orb

    # POA ���֥�������
    self._poa = poa

    # Port�Υ��֥������ȥ�ե���󥹤Υꥹ��. PortList
    self._portRefs = []

    # �����Х�Ȥ�ľ�ܳ�Ǽ���륪�֥������ȥޥ͡�����
    self._portServants = OpenRTM.ObjectManager(self.comp_op)


  ##
  # @if jp
  #
  # @brief Port �ꥹ�Ȥμ���
  #
  # registerPort() �ˤ����Ͽ���줿 Port �� �ꥹ�Ȥ�������롣
  #
  # @param self
  #
  # @return Port �ꥹ��
  #
  # @else
  #
  # @brief Get PortList
  #
  # This operation returns the pointer to the PortList of Ports regsitered
  # by registerPort().
  #
  # @return PortList+ The pointer points PortList
  #
  # @endif
  def getPortList(self):
    return self._portRefs


  ##
  # @if jp
  #
  # @brief Port �Υ��֥������Ȼ��Ȥμ���
  #
  # port_name �ǻ��ꤷ�� Port �Υ��֥������Ȼ��Ȥ��֤���
  # port_name �ǻ��ꤹ�� Port �Ϥ��餫���� registerPort() ����Ͽ����Ƥ�
  # �ʤ���Фʤ�ʤ���
  #
  # @param self
  # @param port_name ���Ȥ��֤�Port��̾��
  #
  # @return Port_ptr Port�Υ��֥������Ȼ���
  #
  # @else
  #
  # @brief Get PortList
  #
  # This operation returns the pointer to the PortList of Ports regsitered
  # by registerPort().
  #
  # @param port_name The name of Port to be returned the reference.
  #
  # @return Port_ptr Port's object reference.
  #
  # @endif
  def getPortRef(self, port_name):
    index = OpenRTM.CORBA_SeqUtil.find(self._portRefs, self.find_port_name(port_name))
    if index >= 0:
      return self._portRefs[index]
    return None


  ##
  # @if jp
  #
  # @brief Port �Υ����Х�ȤΥݥ��󥿤μ���
  #
  # port_name �ǻ��ꤷ�� Port �Υ����Х�ȤΥݥ��󥿤��֤���
  # port_name �ǻ��ꤹ�� Port �Ϥ��餫���� registerPort() ����Ͽ����Ƥ�
  # �ʤ���Фʤ�ʤ���
  #
  # @param self
  # @param port_name ���Ȥ��֤�Port��̾��
  #
  # @return PortBase* Port�����Х�ȴ��쥯�饹�Υݥ���
  #
  # @else
  #
  # @brief Getpointer to the Port's servant
  #
  # This operation returns the pointer to the PortBase servant regsitered
  # by registerPort().
  #
  # @param port_name The name of Port to be returned the servant pointer.
  #
  # @return PortBase* Port's servant's pointer.
  #
  # @endif
  def getPort(self, port_name):
    return self._portServants.find(port_name)


  ##
  # @if jp
  #
  # @brief Port ����Ͽ����
  #
  # ���� port �ǻ��ꤵ�줿 Port �Υ����Х�Ȥ���Ͽ���롣
  # ��Ͽ���줿 Port �Υ����Х�Ȥϥ��󥹥ȥ饯����Ϳ����줿POA ���
  # activate ���졢���Υ��֥������Ȼ��Ȥ�Port��Profile�˥��åȤ���롣
  #
  # @param self
  # @param port Port �����Х��
  #
  # @else
  #
  # @brief Regsiter Port
  #
  # This operation registers the Port's servant given by argument.
  # The given Port's servant will be activated on the POA that is given
  # to the constructor, and the created object reference is set
  # to the Port's profile.
  #
  # @param port The Port's servant.
  #
  # @endif
  def registerPort(self, port):
    self._portRefs.append(port.getPortRef())
    self._portServants.registerObject(port)


  ##
  # @if jp
  #
  # @brief Port ����Ͽ��������
  #
  # ���� port �ǻ��ꤵ�줿 Port ����Ͽ�������롣
  # ������� Port �� deactivate ���졢Port��Profile�Υ�ե���󥹤ˤϡ�
  # nil�ͤ���������롣
  #
  # @param self
  # @param port Port �����Х��
  #
  # @else
  #
  # @brief Delete the Port's registration
  #
  # This operation unregisters the Port's registration.
  # When the Port is unregistered, Port is deactivated, and the object
  # reference in the Port's profile is set to nil.
  #
  # @param port The Port's servant.
  #
  # @endif
  def deletePort(self, port):
    try:
      port.disconnect_all()

      tmp = port.getProfile().name
      OpenRTM.CORBA_SeqUtil.erase_if(self._portRefs, self.find_port_name(tmp))

      self._poa.deactivate_object(self._poa.servant_to_id(port))
      port.setPortRef(RTC.Port._nil)

      self._portServants.unregisterObject(tmp)
    except:
      traceback.print_exception(*sys.exc_info())


  ##
  # @if jp
  #
  # @brief ̾�λ���ˤ��Port ����Ͽ��������
  #
  # �����ǻ��ꤵ�줿̾������� Port ����Ͽ�������롣
  # ������� Port �� deactivate ���졢Port��Profile�Υ�ե���󥹤ˤϡ�
  # nil�ͤ���������롣
  #
  # @param self
  # @param port_name Port ��̾��
  #
  # @else
  #
  # @brief Delete the Port' registration
  #
  # This operation delete the Port's registration specified by port_ name.
  # When the Port is unregistered, Port is deactivated, and the object
  # reference in the Port's profile is set to nil.
  #
  # @param port_name The Port's name.
  #
  # @endif
  def deletePortByName(self, port_name):
    if not port_name:
      return

    p = self._portServants.find(port_name)
    self.deletePort(p)


  ##
  # @if jp
  #
  # @brief ���Ƥ� Port ��deactivate����Ͽ��������
  #
  # ��Ͽ����Ƥ������Ƥ�Port���Ф��ơ������Х�Ȥ�deactivate��Ԥ���
  # ��Ͽ�ꥹ�Ȥ��������롣
  #
  # @param self
  #
  # @else
  #
  # @brief Unregister the Port
  #
  # This operation deactivates the all Port and deletes the all Port's
  # registrations from the list.
  #
  # @endif
  def finalizePorts(self):
    ports = []
    ports = self._portServants.getObjects()
    len_ = len(ports)
    for i in range(len_):
      idx = (len_ - 1) - i
      self.deletePort(ports[idx])



