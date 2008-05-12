#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
#  @file CorbaConsumer.py
#   CORBA Consumer class
#  @date $Date: 2007/09/20 $
#  @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.

from omniORB import CORBA

##
# @if jp
# @class ConsumerBase
#  ���֥������ȥ�ե���󥹤��ݻ�����ץ졼���ۥ�����쥯�饹
# @else
# @class ConsumerBase
#  Placeholder base class to hold remote object reference.
# @endif

class CorbaConsumerBase:
	

	##
	# @if jp
	#  ���󥹥ȥ饯��
	# @param consumer(CorbaConsumerBase&) CorbaConsumerBase���֥�������
	# @else
	#  Consructor
	# @param consumer(CorbaConsumerBase&) CorbaConsumerBase object
	# @endif
	def __init__(self, consumer=None):
		if consumer:
			self._objref = consumer._objref
		else:
			self._objref = None


	def equal(self, consumer):
		self._objref = consumer._objref
		return self

	##
	# @if jp
	#  �ǥ��ȥ饯��
	# @else
	#  Destructor
	# @endif
	def __del__(self):
		pass


	##
	# @if jp
	#  CORBA���֥������Ȥ򥻥åȤ���
	# 
	# Ϳ����줿���֥������ȥ�ե���󥹤ϡ�ConsumerBase ���֥����������
	# �ݻ�����롣 
	# 
	# @param obj CORBA ���֥������ȤΥ�ե����
	# @return obj �� nil ��ե���󥹤ξ�� false ���֤���
	# @else
	#  Set CORBA Object
	# 
	# The given CORBA Object is held.
	# @param obj Object reference of CORBA object
	# @return If obj is nil reference, it returns false.
	# @endif
	def setObject(self, obj):
		if CORBA.is_nil(obj):
			return False

		self._objref = obj
		return True


	##
	# @if jp
	#  CORBA���֥������Ȥ��������
	# 
	# setObject(obj)�ˤ�Ϳ����줿���֥������ȥ�ե���󥹤��֤���
	# @return obj CORBA ���֥������ȤΥ�ե����
	# @else
	#  Set CORBA Object
	# 
	# The CORBA Object reference that given by setObject(obj)
	# @return obj Object reference of CORBA object
	# @endif
	def getObject(self):
		return self._objref


	def releaseObject(self):
		self._objref = CORBA.Object._nil


##
# @if jp
# @class Consumer
#  ���֥������ȥ�ե���󥹤��ݻ�����ץ졼���ۥ���ƥ�ץ졼�ȥ��饹
# 
# interfaceType������Ϳ����줿���Υ��֥������Ȥ��ݻ����롣
# ���֥������Ȥ����åȤ��줿�Ȥ��ˡ�Ϳ����줿���� narrow �����Τǡ�
# _ptr() �Ǽ��������ե���󥹤ϡ�narrow �ѤߤΥ�ե���󥹤Ǥ��롣
# @param interfaceType ���Υۥ�����ݻ����륪�֥������Ȥη�
# @param consumer ���Υ��饹���Υ��֥�������
# @else
# @class Consumer
#  Placeholder template class to hold remote object reference.
# 
# This class holds a type of object that given by interfaceType parameter.
# @endif

class CorbaConsumer(CorbaConsumerBase):
	
	##
	# @if jp
	#  ���󥹥ȥ饯��
	# @param interfaceType idl�ե�������������Ƥ��륤�󥿡��ե�����
	# @param consumer(CorbaConsumer&) CorbaConsumer���֥�������
	# @else
	#  Consructor
	# @param interfaceType Type of interface defined in your xxx.idl
	# @param consumer(CorbaConsumer&) CorbaConsumer object
	# @endif
	def __init__(self, interfaceType=None, consumer=None):
		if interfaceType:
			self._interfaceType = interfaceType
		else:
			self._interfaceType = None

		if consumer:
			CorbaConsumerBase.__init__(self, consumer)
			self._var = consumer._var
		else:
			CorbaConsumerBase.__init__(self)
			self._var = None


	def equal(self, consumer):
		self._var = consumer._var


	##
	# @if jp
	#  �ǥ��ȥ饯��
	# @else
	#  Destructor
	# @endif
	def __del__(self):
		pass


	##
	# @if jp
	#  ���֥������Ȥ򥻥åȤ���
	# ConsumerBase �Υ����С��饤�ɡ� CorbaConsumerBase._objref�˥��֥�������
	# �򥻥åȤ���ȤȤ�ˡ�interfaceType���� narrow �������֥������Ȥ�
	# �����ѿ����ݻ����롣
	# @param obj CORBA Objecct
	# @return True or False
	# @else
	#  Set Object
	# Override function of ConsumerBase. This operation set an Object to 
	# self._objref in the CorbaConsumerBase class, and this object is narrowed to
	# given interfaceType parameter and stored in the member variable.
	# @param obj CORBA Objecct
	# @return True or False
	# @endif
	def setObject(self, obj):
		if CorbaConsumerBase.setObject(self, obj):
			if self._interfaceType:
				self._var = obj._narrow(self._interfaceType)
			else:
				self._var = self._objref
			if not CORBA.is_nil(self._var):
				return True
		return False


	##
	# @if jp
	#  ���֥������Ȥ�narrow�ѤߤΥ��֥������ȥ�ե���󥹤����
	# 	
	# ���֥������ȤΥ�ե���󥹤�������롣
	# ���֥������ȥ�ե���󥹤���Ѥ���ˤϡ�setObject() �ǥ��åȺѤߤ�
	# �ʤ���Фʤ�ʤ���
	# ���֥������Ȥ����åȤ���Ƥ��ʤ���С�nil ���֥������ȥ�ե���󥹤���
	# �֤���롣
	# @return interfaceType��narrow�ѤߤΥ��֥������ȤΥ�ե����
	# @else
	#  Get Object reference narrowed as interfaceType
	# 
	# This operation returns object reference narrowed as interfaceType.
	# To use the returned object reference, reference have to be set by
	# setObject().
	# If object is not set, this operation returns nil object reference.
	# @return The object reference narrowed as interfaceType
	# @endif
	def _ptr(self):
		return self._var


	def releaseObject(self):
		CorbaConsumerBase.releaseObject(self)
		self._var = CORBA.Object._nil
