#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file SdoOrganization.py
  \brief SDO Organization implementation class
  \date $Date: 2007/09/12 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2006
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""


import omniORB.any
from omniORB import CORBA
import threading

import OpenRTM
import SDOPackage, SDOPackage__POA


class ScopedLock:
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()


# SdoOrganization.o 23788
# 41892

class Organization_impl:
	def __init__(self):
		self._pId = OpenRTM.uuid1()
		self._org_mutex = threading.RLock()

		self._orgProperty = SDOPackage.OrganizationProperty([])
		self._varOwner	  = None
		self._memberList  = []


    #============================================================
    #
    # <<< CORBA interfaces >>>
    #
    #============================================================
	def get_organization_id(self):
		"""
		\if jp

		\brief [CORBA interface] Organization ID ���������

		Organization �� ID ���֤����ڥ졼�����

		\return Resource Data Model ��������줿 Organization ID��
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Get Organization Id

		This operation returns the 'id' of the Organization.

		\return The id of the Organization defined in the resource data model.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		return self._pId


	def get_organization_property(self):
		"""
		\if jp

		\brief [CORBA interface] OrganizationProperty �μ���

		Organization ����ͭ���� OrganizationProperty ���֤����ڥ졼�����
		Organization ���ץ�ѥƥ�������ʤ���ж��Υꥹ�Ȥ��֤���

		\return Organization �Υץ�ѥƥ��Υꥹ�ȡ�
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Get OrganizationProperty

		This operation returns the OrganizationProperty that an Organization
		has. An empty OrganizationProperty is returned if the Organization does
		not have any properties.

		\return The list with properties of the organization.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		guard = ScopedLock(self._org_mutex)
		prop = SDOPackage.OrganizationProperty(self._orgProperty.properties)
		return prop


	def get_organization_property_value(self, name):
		"""
		\if jp

		\brief [CORBA interface] OrganizationProperty ��������ͤμ���

		OrganizationProperty �λ��ꤵ�줿�ͤ��֤����ڥ졼�����
		���� "name" �ǻ��ꤵ�줿�ץ�ѥƥ����ͤ��֤���

		\param name(string) �ͤ��֤��ץ�ѥƥ���̾����
		\return ���� "name" �ǻ��ꤵ�줿�ץ�ѥƥ����͡�
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception InvalidParameter ���� "namne" �ǻ��ꤵ�줿�ץ�ѥƥ���
			¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Get specified value of OrganizationProperty

		This operation returns a value in the OrganizationProperty.
		The value to be returned is specified by argument "name."

		\param name(string) The name of the value to be returned.
		\return The value of property which is specified by argument "name."
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not name:
			raise SDOPackage.InvalidParameter("Empty name.")

		index = OpenRTM.CORBA_SeqUtil.find(self._orgProperty.properties, self.nv_name(name))

		if index < 0:
			raise SDOPackage.InvalidParameter("Not found.")

		try:
			value = omniORB.any.to_any(self._orgProperty.properties[index].value)
			return value
		except:
			raise SDOPackage.InternalError("get_organization_property_value()")

		# never reach here
		return None


	def set_organization_property(self, org_property):
		"""
		\if jp

		\brief [CORBA interface] OrganizationProperty �Υ��å�

		�� SDO Specification �� PIM ���Ҥȥ��ڥ졼�����̾���ۤʤ롣
		�� addOrganizationProperty ���б�����
		OrganizationProperty �� Organization ���ɲä��륪�ڥ졼�����
		OrganizationProperty �� Organization �Υץ�ѥƥ����ҤǤ��롣

		\param org_property(SDOPackage::OrganizationProperty) ���åȤ��� OrganizationProperty
		\return ���ڥ졼����������������ɤ������֤���
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception InvalidParameter "org_property" �� null��
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Set OrganizationProperty

		�� SDO Specification �� PIM ���Ҥȥ��ڥ졼�����̾���ۤʤ롣
		�� addOrganizationProperty ���б�����
		This operation adds the OrganizationProperty to an Organization. The
		OrganizationProperty is the property description of an Organization.

		\param org_property(SDOPackage::OrganizationProperty) The type of organization to be added.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception InvalidParameter The argument "organizationProperty" is null.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			guard = ScopedLock(self._org_mutex)
			self._orgProperty = org_property
			return True
		except:
			raise SDOPackage.InternalError("set_organization_property()")

		return False


	def set_organization_property_value(self, name, value):
		"""
		\if jp

		\brief [CORBA interface] OrganizationProperty ���ͤΥ��å�

		OrganizationProperty �� NVList �� name �� value �Υ��åȤ��ɲä⤷����
		�������륪�ڥ졼�����name �� value �ϰ��� "name" �� "value" �ˤ��
		���ꤹ�롣

		\param name(string) �ɲá����������ץ�ѥƥ���̾����
		\param value(CORBA::Any) �ɲá����������ץ�ѥƥ����͡�
		\return ���ڥ졼����������������ɤ������֤���
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception InvalidParameter ���� "name" �ǻ��ꤵ�줿�ץ�ѥƥ���
			¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Set specified value of OrganizationProperty

		This operation adds or updates a pair of name and value as a property
		of Organization to/in NVList of the OrganizationProperty. The name and
		the value to be added/updated are specified by argument "name" and
		"value."

		\param name(string) The name of the property to be added/updated.
		\param value(CORBA::Any) The value of the property to be added/updated.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The property that is specified by argument
			"name" does not exist.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not name:
			raise SDOPackage.InvalidParameter("set_organization_property_value(): Enpty name.")

		index = OpenRTM.CORBA_SeqUtil.find(self._orgProperty.properties, self.nv_name(name))

		if index < 0:
			nv = SDOPackage.NameValue(name, value)
			OpenRTM.CORBA_SeqUtil.push_back(self._orgProperty.properties, nv)
		else:
			self._orgProperty.properties[index].value = value

		return True


	def remove_organization_property(self, name):
		"""
		\if jp

		\brief [CORBA interface] OrganizationProperty �κ��

		OrganizationProperty �� NVList ��������Υץ�ѥƥ��������롣
		��������ץ�ѥƥ���̾���ϰ��� "name" �ˤ����ꤵ��롣

		\param name(string) �������ץ�ѥƥ���̾����
		\return ���ڥ졼����������������ɤ������֤���
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception InvalidParameter ���� "name" �ǻ��ꤵ�줿�ץ�ѥƥ���
			¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Remove specified OrganizationProperty

		This operation removes a property of Organization from NVList of the
		OrganizationProperty. The property to be removed is specified by
		argument "name."

		\param name(string) The name of the property to be removed.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The property that is specified by argument
			"name" does not exist.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not name:
			raise SDOPackage.InvalidParameter("remove_organization_property_value(): Enpty name.")

		index = OpenRTM.CORBA_SeqUtil.find(self._orgProperty.properties, self.nv_name(name))

		if index < 0:
			raise SDOPackage.InvalidParameter("remove_organization_property_value(): Not found.")

		try:
			OpenRTM.CORBA_SeqUtil.erase(self._orgProperty.properties, index)
			return True
		except:
			raise SDOPackage.InternalError("remove_organization_property_value()")

		return False


	def get_owner(self):
		"""
		\if jp

		\brief [CORBA interface] Organization �Υ����ʡ����������

		���� Organization �Υ����ʡ��ؤλ��Ȥ��֤���

		\return �����ʡ����֥������Ȥؤλ��ȡ�
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Get the owner of the SDO

		This operation returns the SDOSystemElement that is owner of
		the Organization.

		\return Reference of owner object.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		return self._varOwner


	def set_owner(self, sdo):
		"""
		\if jp

		\brief [CORBA interface] Organization �˥����ʡ��򥻥åȤ���

		Organization ���Ф��� SDOSystemElement �򥪡��ʡ��Ȥ��ƥ��åȤ��롣
		���� "sdo" �˥��åȤ��� SDOSystemElement ����ꤹ�롣

		\param sdo(SDOPackage::SDOSystemElement) �����ʡ����֥������Ȥλ��ȡ�
		\return ���ڥ졼����������������ɤ������֤���
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception InvalidParameter ���� "sdo" �� null�Ǥ��롢�⤷���ϡ�
			"sdo" ��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Set the orner of the Organization

		This operation sets an SDOSystemElement to the owner of the
		Organization. The SDOSystemElement to be set is specified by argument
		"sdo."

		\param sdo(SDOPackage::SDOSystemElement) Reference of owner object.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument "sdo" is null, or the object
			that is specified by "sdo" in argument "sdo" does not exist.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if CORBA.is_nil(sdo):
			raise SDOPackage.InvalidParameter("set_owner()")

		try:
			self._varOwner = sdo
			return True
		except:
			raise SDOPackage.InternalError("set_owner()")

		return True


	def get_members(self):
		"""
		\if jp

		\brief [CORBA interface] Organization �Υ��С����������

		Organization �Υ��С��� SDO �Υꥹ�Ȥ��֤���
		���С���¸�ߤ��ʤ���ж��Υꥹ�Ȥ��֤���

		\return Organization �˴ޤޤ����С� SDO �Υꥹ�ȡ�
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Get a menber list of the Organization

		This operation returns a list of SDOs that are members of an
		Organization. An empty list is returned if the Organization does not
		have any members.

		\return Member SDOs that are contained in the Organization object.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			return self._memberList
		except:
			raise SDOPackage.InternalError("get_members()")


	def set_members(self, sdos):
		"""
		\if jp

		\brief [CORBA interface] SDO �� ServiceProfile �Υ��å�

		SDO �Υꥹ�Ȥ� Organization �Υ��С��Ȥ��ƥ��åȤ��롣
		Organization �����Ǥ˥��С��� SDO ��������Ƥ�����ϡ�
		Ϳ����줿 SDO �Υꥹ�Ȥ��֤������롣

		\param sdos(SDOPackage::SDO�Υꥹ��) ���С��� SDO��
		\return ���ڥ졼����������������ɤ������֤���
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception InvalidParameter ���� "SDOList" �� null�Ǥ��롢�⤷����
			�����˻��ꤵ�줿 "SDOList" ��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Set SDO's ServiceProfile

		This operation assigns a list of SDOs to an Organization as its members.
		If the Organization has already maintained a member SDO(s) when it is
		called, the operation replaces the member(s) with specified list of
		SDOs.

		\param sdos(SDOPackage::SDO�Υꥹ��) Member SDOs to be assigned.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument "SDOList" is null, or if the
			object that is specified by the argument "sdos" does not
			exist.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not sdos:
			raise SDOPackage.InvalidParameter("set_members(): SDOList is empty.")

		try:
			self._memberList = sdos
			return True
		except:
			raise SDOPackage.InternalError("set_members()")

		return True


	def add_members(self, sdo_list):
		"""
		\if jp

		\brief [CORBA interface] SDO ���С����ɲ�

		Organization �˥��С��Ȥ��� SDO ���ɲä��롣
		���� "sdo" ���ɲä�����С� SDO ����ꤹ�롣

		\param sdo Organization ���ɲä���� SDO �Υꥹ�ȡ�
		\return ���ڥ졼����������������ɤ������֤���
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception InvalidParameter ���� "sdo" �� null�Ǥ��롣
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Add the menebr SDOs

		This operation adds a member that is an SDO to the organization.
		The member to be added is specified by argument "sdo."

		\param sdo The member to be added to the organization.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument "sdo" is null.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			OpenRTM.CORBA_SeqUtil.push_back_list(self._memberList, sdo_list)
			return True
		except:
			raise SDOPackage.InternalError("add_members()")

		return False


	def remove_member(self, id):
		"""
		\if jp

		\brief [CORBA interface] SDO ���С��κ��

		Organization ��������ǻ��ꤵ�줿 "id" �� SDO �������롣

		\param id(string) ������� SDO �� id��
		\return ���ڥ졼����������������ɤ������֤���
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception InvalidParameter ���� "id" �� null �⤷����¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Remove menber SDO from Organization

		This operation removes a member from the organization. The member to be
		removed is specified by argument "id."

		\param id(string) Id of the SDO to be removed from the organization.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument "id" is null or does not exist.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if not id:
			raise SDOPackage.InvalidParameter("remove_member(): Empty name.")

		index = OpenRTM.CORBA_SeqUtil.find(self._memberList, self.sdo_id(id))

		if index < 0:
			raise SDOPackage.InvalidParameter("remove_member(): Not found.")

		try:
			OpenRTM.CORBA_SeqUtil.erase(self._memberList, index)
			return True
		except:
			raise SDOPackage.InternalError("remove_member(): Not found.")

		return False


	def get_dependency(self):
		"""
		\if jp

		\brief [CORBA interface] Organization �� DependencyType �����

		Organization �δط���ɽ�� "DependencyType" ���֤���

		\return Organizaton �ΰ�¸�ط� DependencyType ���֤���
			DependencyType �� OMG SDO ���ͤ� Section 2.2.2 2-3 �ڡ�����
			"Data Structures Used by Resource Data Model" �򻲾ȡ�
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Get the DependencyType of the Organization

		This operation gets the relationship "DependencyType" of the
		Organization.

		\return The relationship of the Organization as DependencyType.
			DependencyType is defined in Section 2.2.2, "Data Structures
			Used by Resource Data Model," on page 2-3
			of OMG SDO Specification.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		return self._dependency


	def set_dependency(self, dependency):
		"""
		\if jp

		\brief [CORBA interface] Organization �� DependencyType �򥻥åȤ���

		Organization �ΰ�¸�ط� "DependencyType" �򥻥åȤ��롣
		���� "dependencty" �ˤ���¸�ط���Ϳ���롣

		\param dependency(SDOPackage::DependencyType) Organization �ΰ�¸�ط���ɽ�� DependencyType��
			DependencyType �� OMG SDO ���ͤ� Section 2.2.2��2-3 �ڡ�����
			"Data Structures Used by Resource Data Model" �򻲾ȡ�
		\return ���ڥ졼����������������ɤ������֤���
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception InvalidParameter ���� "sProfile" �� null�Ǥ��롣
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Set the DependencyType of the Organization

		This operation sets the relationship "DependencyType" of the
		Organization. The value to be set is specified by argument "dependency."

		\param dependency(SDOPackage::DependencyType) The relationship of the Organization as
			DependencyType. DependencyType is defined in Section
			2.2.2, "Data Structures Used by Resource Data Model,"
			on page 2-3.
		\return If the operation was successfully completed.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The argument "dependency" is null.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			self._dependency = dependency
			return True
		except:
			raise SDOPackage.InternalError("set_dependency(): Unknown.")

		return False
		

	# end of CORBA interface definition
	#============================================================


	class nv_name:
		def __init__(self, name):
			self._name = name

		def __call__(self, nv):
			return str(self._name) == str(nv.name)

	class sdo_id:
		def __init__(self, id_):
			self._id = id_

		def __call__(self, sdo):
			id_ = sdo.get_sdo_id()
			return str(self._id) == str(id_)
		
