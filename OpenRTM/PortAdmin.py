#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file PortAdmin.py
 \brief RTC's Port administration class
 \date $Date: 2007/09/03 $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""

import traceback
import sys

import RTC, RTC__POA
import OpenRTM


class PortAdmin:
	class comp_op:
		def __init__(self, name=None, factory=None):
			if name != None:
				self._name = name
			if factory != None:
				self._name = factory.getProfile().name

		def __call__(self, obj):
			name_ = obj.getProfile().name
			return self._name == name_
    

	class find_port_name:
		def __init__(self, name):
			self._name = name

		def __call__(self, p):
			prof = p.get_port_profile()
			name_ = prof.name 
			return self._name == name_


	class del_port:
		def __init__(self, pa):
			self._pa = pa

		def __call__(self, p):
			self._pa.deletePort(p)


	def __init__(self, orb, poa):
		# ORB ���֥�������
		self._orb = orb

		# POA ���֥�������
		self._poa = poa

		# Port�Υ��֥������ȥ�ե���󥹤Υꥹ��. PortList
		self._portRefs = []

		# �����Х�Ȥ�ľ�ܳ�Ǽ���륪�֥������ȥޥ͡�����
		self._portServants = OpenRTM.ObjectManager(self.comp_op)


	def getPortList(self):
		"""
		\if jp
		\brief PortList �μ���

		registerPort() �ˤ����Ͽ���줿 Port �� PortList �ؤΥݥ��󥿤��֤���
		\return PortList PortList �ؤΥݥ���
		\else
		\brief Get PortList

		This operation returns the pointer to the PortList of Ports regsitered
		by registerPort().
		\return PortList+ The pointer points PortList
		\endif
		"""
		return self._portRefs


	def getPortRef(self, port_name):
		"""
		\if jp
		\brief Port �Υ��֥������Ȼ��Ȥμ���

		port_name �ǻ��ꤷ�� Port �Υ��֥������Ȼ��Ȥ��֤���
		port_name �ǻ��ꤹ�� Port �Ϥ��餫���� registerPort() ����Ͽ����Ƥ�
		�ʤ���Фʤ�ʤ���
		\param port_name(string) ���Ȥ��֤�Port��̾��
		\return Port_ptr Port�Υ��֥������Ȼ���
		\else
		\brief Get PortList

		This operation returns the pointer to the PortList of Ports regsitered
		by registerPort().
		\param port_name(string) The name of Port to be returned the reference.
		\return Port_ptr Port's object reference.
		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._portRefs, self.find_port_name(port_name))
		if index >= 0:
			return self._portRefs[index]
		return None


	def getPort(self, port_name):
		"""
		\if jp
		\brief Port �Υ����Х�ȤΥݥ��󥿤μ���

		port_name �ǻ��ꤷ�� Port �Υ����Х�ȤΥݥ��󥿤��֤���
		port_name �ǻ��ꤹ�� Port �Ϥ��餫���� registerPort() ����Ͽ����Ƥ�
		�ʤ���Фʤ�ʤ���
		\param port_name(string) ���Ȥ��֤�Port��̾��
		\return PortBase Port�����Х�ȴ��쥯�饹�Υݥ���
		\else
		\brief Getpointer to the Port's servant

		This operation returns the pointer to the PortBase servant regsitered
		by registerPort().
		\param port_name(string) The name of Port to be returned the servant pointer.
		\return PortBase Port's servant's pointer.
		\endif
		"""
		return self._portServants.find(port_name)


	def registerPort(self, port):
		"""
		\if jp
		\brief Port ����Ͽ����

		���� port �ǻ��ꤵ�줿 Port �Υ����Х�Ȥ���Ͽ���롣
		��Ͽ���줿 Port �Υ����Х�Ȥϥ��󥹥ȥ饯����Ϳ����줿POA ���
		activate ���졢���Υ��֥������Ȼ��Ȥ�Port��Profile�˥��åȤ���롣
		\param port(OpenRTM.PortBase) Port �����Х��
		\else
		\brief Regsiter Port

		This operation registers the Port's servant given by argument.
		The given Port's servant will be activated on the POA that is given
		to the constructor, and the created object reference is set
		to the Port's profile.
		\param port(OpenRTM.PortBase) The Port's servant.
		\endif
		"""
		self._portRefs.append(port.getPortRef())
		self._portServants.registerObject(port)


	def deletePort(self, port):
		"""
		\if jp
		\brief Port ����Ͽ��������

		���� port �ǻ��ꤵ�줿 Port ����Ͽ�������롣
		������� Port �� deactivate ���졢Port��Profile�Υ�ե���󥹤ˤϡ�
		nil�ͤ���������롣
		\param port(OpenRTM.PortBase) Port �����Х��
		\else
		\brief Delete the Port's registration

		This operation unregisters the Port's registration.
		When the Port is unregistered, Port is deactivated, and the object
		reference in the Port's profile is set to nil.
		\param port(OpenRTM.PortBase) The Port's servant.
		\endif
		"""
		try:
			port.disconnect_all()

			tmp = port.getProfile().name
			OpenRTM.CORBA_SeqUtil.erase_if(self._portRefs, self.find_port_name(tmp))

			self._poa.deactivate_object(self._poa.servant_to_id(port))
			port.setPortRef(RTC.Port._nil)

			self._portServants.unregisterObject(tmp)
		except:
			traceback.print_exception(*sys.exc_info())


	def deletePortByName(self, port_name):
		"""
		\if jp
		\brief Port ����Ͽ��������

		�����ǻ��ꤵ�줿̾������� Port ����Ͽ�������롣
		������� Port �� deactivate ���졢Port��Profile�Υ�ե���󥹤ˤϡ�
		nil�ͤ���������롣
		\param port_name(string) Port ��̾��
		\else
		\brief Delete the Port' registration

		This operation delete the Port's registration specified by port_ name.
		When the Port is unregistered, Port is deactivated, and the object
		reference in the Port's profile is set to nil.
		\param port_name(string) The Port's name.
		\endif
		"""
		if not port_name:
			return

		p = self._portServants.find(port_name)
		self.deletePort(p)


	def finalizePorts(self):
		"""
		\if jp
		\brief ���Ƥ� Port ��deactivate����Ͽ��������

		��Ͽ����Ƥ������Ƥ�Port���Ф��ơ������Х�Ȥ�deactivate��Ԥ���
		��Ͽ�ꥹ�Ȥ��������롣
		\else
		\brief Unregister the Port

		This operation deactivates the all Port and deletes the all Port's
		registrations from the list.
		\endif
		"""
		ports = []
		ports = self._portServants.getObjects()
		len_ = len(ports)
		predi = self.del_port(self)
		for i in range(len_):
			idx = (len_ - 1) - i
			predi(ports[idx])
			


