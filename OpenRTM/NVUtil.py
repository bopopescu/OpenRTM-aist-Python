#!/usr/bin/env python
# -*- coding: euc-jp -*- 

"""
  \file NVUtil.py
  \brief NameValue and NVList utility functions
  \date $Date: 2007/09/11$
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2006
      Noriaki Ando
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""

import sys
import traceback
from omniORB import any

import OpenRTM
import SDOPackage, SDOPackage__POA


def newNV(name, value):
	"""
	 \if jp
	 \brief NameValue ����������
	    ���Υ��ڥ졼������NameValue��������롣
	    CORBA::Char, CORBA::Boolean, CORBA::Octet �Ϻ����Ǥ��ʤ���
	    �������ͤ� newNVChar(), newNVBool(), newNVOctet() �Ǻ������롣
	 \param name(string) NameValue �� name
	 \param value(data) NameValue �� value
	 \return NameValue(SDOPackage::NameValue)

	 \else
	 \brief Create NameVale
	    This operation creates NameVale.
	    CORBA::Char, CORBA::Boolean, CORBA::Octet creation is not supported.
	    These type of NameValue should be created by using 
	    newNVChar(), newNVBool(), newNVOctet() functions.
	 \param name(string) name of NameValue
	 \param value(data) value of NameValue
	 \return NameValue(SDOPackage::NameValue)
	 \endif
	"""
	try:
		any_val = any.to_any(value)
	except:
		print "ERROR  NVUtil.newNV : Can't convert to any. ", type(value)
		raise

		
	nv = SDOPackage.NameValue(name, any_val)
	return nv


def newNVBool(name, value):
	"""
	 \if jp
	 \brief value �� CORBA::Boolean �� NameValue ����������
	    ���Υ��ڥ졼������f value �� CORBA::Boolean �� NameValue��������롣
	 \param name(string) NameValue �� name
	 \param value(bool) NameValue �� value
	 \return NameValue(SDOPackage::NameValue)
	 
	 \else
	 \brief Create CORBA::Boolean value type NameVale
	    This operation creates CORBA::Boolean value type NameVale.
	 \param name(string) name of NameValue
	 \param value(bool) value of NameValue
	 \return NameValue(SDOPackage::NameValue)
	 \endif
	"""
	return newNV(name, value)


def newNVOctet(name, value):
	"""
	 \if jp
	 \brief value �� CORBA::Octet �� NameValue ����������
	    ���Υ��ڥ졼������ value �� CORBA::Octet �� NameValue��������롣
	 \param name(string) NameValue �� name
	 \param value(CORBA::Octet) NameValue �� value
	 \return NameValue(SDOPackage::NameValue)
	 
	 \else
	 \brief Create CORBA::Octet value type NameVale
	    This operation creates CORBA::Octet value type NameVale.
	 \param name(string) name of NameValue
	 \param value(CORBA::Octet) value of NameValue
	 \return NameValue(SDOPackage::NameValue)
	 \endif
	"""
	return newNV(name, value)


def newNVAny(name, value):
	"""
	 \if jp
	 \brief value �� CORBA::Any �� NameValue ����������
	    ���Υ��ڥ졼������ value �� CORBA::Any �� NameValue��������롣
	 \param name(string) NameValue �� name
	 \param value(CORBA::Any) NameValue �� value
	 \return NameValue(SDOPackage::NameValue)
	 
	 \else
	 \brief Create CORBA::Any value type NameVale
	    This operation creates CORBA::Any value type NameVale.
	 \param name(string) name of NameValue
	 \param value(CORBA::Any) value of NameValue
	 \return NameValue(SDOPackage::NameValue)
	 \endif
	"""
	return newNV(name, value)


def copyFromProperties(nv, prop):
	"""
	 \if jp
	 \brief Properties �� NVList �إ��ԡ�����
	    ���Υ��ڥ졼������ Properties �� NVList �إ��ԡ����롣
	    NVList �� value ������ CORBA::string ���Ȥ��ƥ��ԡ����롣
	 \param nv(SDOPackage::NameValue�Υꥹ��) Properties ���ͤ��Ǽ���� NVList
	 \param prop(OpenRTM.Properties) ���ԡ����� Properties
	 
	 \else
	 \brief Copy to NVList from Proeprties
	    This operation copies Properties to NVList.
	    Created NVList's values are CORBA::string.
	 \param nv(list of SDOPackage::NameValue) NVList to store Properties values
	 \param prop(OpenRTM.Properties) Properties that is copies from
	 \endif
	"""
	keys = prop.propertyNames()
	keys_len = len(keys)
	nv_len = len(nv)
	if nv_len > 0:
		for i in range(nv_len):
			del nv[-1]

	for i in range(keys_len):
		nv.append(newNV(keys[i], prop.getProperty(keys[i])))


def copyToProperties(prop, nvlist):
	"""
	 \if jp
	 \brief NVList �� Properties �إ��ԡ�����
	    ���Υ��ڥ졼������ NVList �� Properties �إ��ԡ����롣
	 \param prop(OpenRTM.Properties) NVList ���ͤ��Ǽ���� Properties
	 \param nvlist(SDOPackage::NameValue�Υꥹ��) ���ԡ����� 
	 
	 \else
	 \brief Copy to Proeprties from NVList
	    This operation copies NVList to Properties.
	 \param prop(OpenRTM.Properties) NVList that is copies from
	 \param nvlist(list of SDOPackage::NameValue) Properties to store NVList values
	 \endif
	"""
	for nv in nvlist:
		try:
			val = str(any.from_any(nv.value, keep_structs=True))
			prop.setProperty(str(nv.name),val)
		except:
			traceback.print_exception(*sys.exc_info())
			pass


class to_prop:
	def __init__(self):
		self._prop = OpenRTM.Properties()
		
	def __call__(self, nv):
		self._prop.setProperty(nv.name, nv.value)


def toProperties(nv):
	"""
	 \brief nv��Properties���Ѵ�����
	 \param nv(SDOPackage::NameValue�Υꥹ��)
	"""
	p = OpenRTM.CORBA_SeqUtil.for_each(nv, to_prop())
	return p._prop


class nv_find:
	def __init__(self, name):
		self._name = name

	def __call__(self, nv):
		return str(self._name) == str(nv.name)
	

def find(nv, name):
	"""
	 \if jp
	 \brief NVList ���� name �ǻ��ꤵ�줿 value ���֤�
	    ���Υ��ڥ졼������ name �ǻ��ꤵ�줿 value �� Any �����֤���
	 \param nv(SDOPackage::NameValue�Υꥹ��) �����оݤ� NVList
	 \param name(string) ��������̾��
	 
	 \else
	 \brief Get value in NVList specified by name
	    This operation returns Any type of value specified by name.
	    Created NVList's values are CORBA::string.
	 \param nv(list of SDOPackage::NameValue) NVList to be searched
	 \param name(string) name to seartch in NVList
	 \endif
	"""
	index = OpenRTM.CORBA_SeqUtil.find(nv, nv_find(name))

	if index < 0:
		raise "Not found."

	return nv[index].value


def find_index(nv, name):
	"""
	 \if jp
	 \brief NVList ���� name �ǻ��ꤵ�줿 value ����������ֹ��֤�
	    ���Υ��ڥ졼������ name �ǻ��ꤵ�줿 value �� Any �����֤���
	 \param nv(SDOPackage::NameValue�Υꥹ��) �����оݤ� NVList
	 \param name(string) ��������̾��
	 
	 \else
	 \brief Get value in NVList specified by name
	    This operation returns Any type of value specified by name.
	    Created NVList's values are CORBA::string.
	 \param nv(list of SDOPackage::NameValue) NVList to be searched
	 \param name(string) name to seartch in NVList
	 \endif
	"""
	return OpenRTM.CORBA_SeqUtil.find(nv, nv_find(name))


def isString(nv, name):
	"""
	\if jp

	\brief ���ꤵ�줿 name �� value �η��� string �Ǥ��뤫�ɤ�����

	���Υ��ڥ졼������ name �ǻ��ꤵ�줿 value �η��� CORBA::string
	���ɤ����� bool �ͤ��֤���

	\param nv(SDOPackage::NameValue�Υꥹ��) �����оݤ� NVList
	\param name(string) ��������̾��

	\else

	\brief Whether the name of NVList's value is CORBA::string

	This operation returns boolean value whether the name of NVList's value
	is CORBA::string.

	\param nv(list of SDOPackage::NameValue) NVList to be searched
	\param name(string) name to seartch in NVList

	\endif
	"""
	try:
		value = find(nv, name)
		val = any.from_any(value, keep_structs=True)
		return type(val) == str
	except:
		return False
	

def isStringValue(nv, name, value):
	"""
	 \brief value��ʸ�����ݤ�������å�
	 \param nv(SDOPackage::NameValue�Υꥹ��)
	 \param name(string)
	 \param value(string)
	"""
	if isString(nv, name):
		if toString(nv, name) == value:
			return True
	return False


def toString(nv, name):
	"""
	\if jp

	\brief ���ꤵ�줿 name �� NVList �� string �Ȥ����֤���

	���Υ��ڥ졼������ name �ǻ��ꤵ�줿 NVList ���ͤ� string ���֤���
	�⤷��name �ǻ��ꤷ�� value ���ͤ� CORBA::string �Ǥʤ���С�
	����ʸ�����string���֤���

	\param nv(SDOPackage::NameValue�Υꥹ��) �����оݤ� NVList
	\param name(string) ��������̾��
	\return name ���б������ͤ�string������

	\else

	\brief Get string value in NVList specified by name

	This operation returns string value in NVList specified by name.
	If the value in NVList specified by name is not CORBA::string type
	this operation returns empty string value.

	\param nv(list of SDOPackage::NameValue) NVList to be searched
	\param name(string) name to to serach
	\return string value named by name

	\endif
	"""
	str_value = ""
	try:
		ret_value = find(nv, name)
		val = any.from_any(ret_value, keep_structs=True)
		if type(val) == str:
			str_value = val
	except:
		traceback.print_exception(*sys.exc_info())
		pass
	
	return str_value


def appendStringValue(nv, name, value):
	"""
	 \param nv(SDOPackage::NameValue�Υꥹ��)
	 \param name(string)
	 \param value(string)
	"""
	index = find_index(nv, name)

	if index >= 0:
		tmp_str = nv[index].value

		values = OpenRTM.split(tmp_str,",")
		find_flag = False
		for val in values:
			if val == value:
				find_flag = True

		if not find_flag:
			tmp_str += ", "
			tmp_str += value
			nv[index].value = tmp_str
	else:
		OpenRTM.CORBA_SeqUtil.push_back(nv, newNV(name, value))

	return True
			

def append(dest, src):
	"""
	 \param dest(SDOPackage::NameValue�Υꥹ��)
	 \param src(SDOPackage::NameValue�Υꥹ��)
	"""
	for i in range(len(src)):
		OpenRTM.CORBA_SeqUtil.push_back(dest, src[i])


def dump(nv):
	"""
	 \param nv(SDOPackage::Namevalue�Υꥹ��)
	"""
	for i in range(len(nv)):
		if type(nv[i].value) == str:
			print nv[i].name, ": ", nv[i].value
		else:
			print nv[i].name, ": not a string value"
