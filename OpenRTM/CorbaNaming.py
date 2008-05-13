#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
#  @file CorbaNaming.py
#   CORBA naming service helper class
#  @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.

import omniORB.CORBA as CORBA
import CosNaming
import string


##
# @if jp
# @class CorbaNaming
#  CORBA Naming Service �إ�ѡ����饹
# 
# ���Υ��饹�ϡ�CosNaming.NameComponent ���Ф����åѡ����饹�Ǥ��롣
# CosNaming.NameComponent �����ĥ��ڥ졼�����Ȥۤ�Ʊ����ǽ��
# ���ڥ졼�������󶡤���ȤȤ�ˡ��͡��ॳ��ݡ��ͥ�� CosNaming.NameComponent
# �������ʸ����ˤ��̾��ɽ��������դ��륪�ڥ졼�������󶡤��롣
# 
# ���֥������Ȥ������������뤤������ľ��� CORBA �͡��ॵ���Ф���³��
# �ʸ塢���Υ͡��ॵ���ФΥ롼�ȥ���ƥ����Ȥ��Ф��Ƽ�Υ��ڥ졼�����
# ��������롣
# �������ؤΥ͡��ߥ󥰥���ƥ����Ȥκ����䥪�֥������ȤΥХ���ɤˤ����ơ�
# ����Υ���ƥ����Ȥ�¸�ߤ��ʤ����Ǥ⡢����Ū�˥���ƥ����Ȥ�Х����
# ����Ū�Υ���ƥ����Ȥ䥪�֥������ȤΥХ���ɤ�Ԥ����Ȥ�Ǥ��롣
# 
# @else
# @class CorbaNaming
#  CORBA Naming Service helper class
# 
# This class is a wrapper class of CosNaming.NameComponent.
# Almost the same operations which CosNaming.NameComponent has are
# provided, and some operation allows string naming representation of
# context and object instead of CosNaming.NameComponent.
# 
# The object of the class would connect to a CORBA naming server at
# the instantiation or immediately after instantiation.
# After that the object invokes operations to the root context of it.
# This class realizes forced binding to deep NamingContext, without binding
# intermediate NamingContexts explicitly.
# @endif

class CorbaNaming:
	

	##
	# @if jp
	#  ���饹���󥹥ȥ饯��
	# @param orb(CORBA.ORB_ptr)
	# @param name_server(string)
	# 
	# @else
	#  constructor.
	# @param orb(CORBA.ORB_ptr)
	# @param name_server(string)
	# @endif
	def __init__(self, orb, name_server=None):
		self._orb = orb
		self._nameServer = ""
		self._rootContext = CosNaming.NamingContext._nil
		self._blLength = 100

		if name_server != None:
			self._nameServer = "corbaloc::" + name_server + "/NameService"
			try:
				obj = orb.string_to_object(self._nameServer)
				self._rootContext = obj._narrow(CosNaming.NamingContext)
				if CORBA.is_nil(self._rootContext):
					print "CorbaNaming: Failed to narrow the root naming context."

			except CORBA.ORB.InvalidName:
				print "Service required is invalid [does not exist]."

		return
	

	def __del__(self):
		return


	##
	# @if jp
	#  ������ѥ᥽�å�
	# @param name_server(string)
	# 
	# @else
	#  initialiize method.
	# @param name_server(string)
	# @endif
	def init(self, name_server):
		self._nameServer = "corbaloc::" + name_server + "/NameService"
		obj = self._orb.string_to_object(self._nameServer)
		self._rootContext = obj._narrow(CosNaming.NamingContext)
		if CORBA.is_nil(self._rootContext):
			raise MemoryError

		return


	##
	# @if jp
	# 
	#  Object �� bind ����
	# 
	# CosNaming::bind() �Ȥۤ�Ʊ����Ư���򤹤뤬�����Ϳ����줿�͡��ॵ���Ф�
	# �롼�ȥ���ƥ����Ȥ��Ф���bind()���ƤӽФ���������ۤʤ롣
	# 
	# Name <name> �� Object <obj> ������ NamingContext ��˥Х���ɤ��롣
	# c_n �� n ���ܤ� NameComponent �򤢤�魯�Ȥ���ȡ�
	# name �� n �Ĥ� NameComponent ��������Ȥ����ʲ��Τ褦�˰����롣
	# 
	# cxt->bind(<c_1, c_2, ... c_n>, obj) �ϰʲ�������Ʊ���Ǥ��롣
	# cxt->resolve(<c_1, ... c_(n-1)>)->bind(<c_n>, obj)
	# 
	# ���ʤ����1���ܤ���n-1���ܤΥ���ƥ����Ȥ��褷��n-1���ܤΥ���ƥ�����
	# ��� name <n> �Ȥ��ơ�obj �� bind ���롣
	# ̾�����˻��ä��� <c_1, ... c_(n-1)> �� NemingContext �ϡ�
	# bindContext() �� rebindContext() �Ǵ��˥Х���ɺѤߤǤʤ���Фʤ�ʤ���
	# �⤷ <c_1, ... c_(n-1)> �� NamingContext ��¸�ߤ��ʤ����ˤϡ�
	# NotFound �㳰��ȯ�����롣
	# 
	# �������������Х���ɥե饰 force �� true �λ��ϡ�<c_1, ... c_(n-1)>
	# ��¸�ߤ��ʤ����ˤ⡢�Ƶ�Ū�˥���ƥ����Ȥ�Х���ɤ��ʤ��顢
	# �ǽ�Ū�� obj ��̾�� name <c_n> �˥Х���ɤ��롣
	# 
	# ������ξ��Ǥ⡢n-1���ܤΥ���ƥ����Ⱦ�� name<n> �Υ��֥�������
	# (Object ���뤤�� ����ƥ�����) ���Х���ɤ���Ƥ����
	# AlreadyBound �㳰��ȯ�����롣
	# 
	# @param name_list(list) ���֥������Ȥ��դ���̾���� NameComponent�ꥹ��
	# @param obj(CORBA::Object) ��Ϣ�դ����� Object
	# @param force(bool) true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
	# 
	# @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
	# @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
	# @exception InvalidName ���� name ��̾����������
	# @exception AlreadyBound name <c_n> �� Object �����Ǥ˥Х���ɤ���Ƥ��롣
	# 
	# @else
	# 
	# 
	# 
	# @endif
	def bind(self, name_list, obj, force=None):
		if force == None :
			force = True

		try:
			self._rootContext.bind(name_list, obj)
		except CosNaming.NamingContext.NotFound:
			if force:
				self.bindRecursive(self._rootContext, name_list, obj)
			else:
				raise
		except CosNaming.NamingContext.CannotProceed, err:
			if force:
				self.bindRecursive(err.cxt, err.rest_of_name, obj)
			else:
				raise
		except CosNaming.NamingContext.AlreadyBound:
			self._rootContext.rebind(name_list, obj)


	##
	# @if jp
	#  Object �� bind ����
	# 
	# Object �� bind ����ݤ�Ϳ����̾����ʸ����ɽ���Ǥ��뤳�Ȱʳ��ϡ�bind()
	# ��Ʊ���Ǥ��롣bind(toName(string_name), obj) ��������
	# @param string_name(string) ���֥������Ȥ��դ���̾����ʸ����ɽ��
	# @param obj(CORBA::Object) ��Ϣ�դ����륪�֥�������
	# @param force(bool) true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
	# @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
	# @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
	# @exception InvalidName ���� name ��̾����������
	# @exception AlreadyBound name <n> �� Object �����Ǥ˥Х���ɤ���Ƥ��롣
	# 
	# @else
	# 
	# @endif
	def bindByString(self, string_name, obj, force=True):
		self.bind(self.toName(string_name), obj, force)


	##
	# @if jp
	#  ����Υ���ƥ����Ȥ� bind ���ʤ��� Object �� bind ����
	# 
	# context ��Ϳ����줿 NamingContext ���Ф��ơ�name_list �ǻ��ꤵ�줿
	# �͡��ॳ��ݡ��ͥ�� <c_1, ... c_(n-1)> �� NamingContext �Ȥ���
	# ��褷�ʤ��顢̾�� <c_n> ���Ф��� obj �� bind ���롣
	# �⤷��<c_1, ... c_(n-1)> ���б����� NamingContext ���ʤ����ˤ�
	# ������ NamingContext ��Х���ɤ��롣
	# 
	# �ǽ�Ū�� <c_1, c_2, ..., c_(n-1)> ���б����� NamingContext ������
	# �ޤ��ϲ�褵�줿��ǡ�CosNaming::bind(<c_n>, object) ���ƤӽФ���롣
	# ���ΤȤ������Ǥ˥Х���ǥ��󥰤�¸�ߤ���� AlreadyBound�㳰��ȯ�����롣
	# 
	# ����Υ���ƥ����Ȥ��褹������ǡ���褷�褦�Ȥ��륳��ƥ����Ȥ�
	# Ʊ��̾���� NamingContext �ǤϤʤ� Binding ��¸�ߤ����硢
	# CannotProceed �㳰��ȯ������������ߤ��롣
	# @param(CosNaming.NameComponent) context bind �򳫻Ϥ��롡NamingContext
	# @param name(CosNaming.NameComponent�Υꥹ��) ���֥������Ȥ��դ���̾���Υ͡��ॳ��ݡ��ͥ��
	# @param obj(CORBA::Object) ��Ϣ�դ����륪�֥�������
	# @exception CannotProceed <c_1, ..., c_(n-1)> ���б����� NamingContext 
	# �Τ����ҤȤĤ������Ǥ� NamingContext �ʳ��� object �˥Х����
	# ����Ƥ��ꡢ�������³�Ǥ��ʤ���
	# @exception InvalidName ̾�� name_list ������
	# @exception AlreadyBound name <c_n> �ˤ��Ǥ˲��餫�� object ���Х����
	# ����Ƥ��롣
	# @else
	# 
	# @endif
	def bindRecursive(self, context, name_list, obj):
		length = len(name_list)
		cxt = context
		for i in range(length):
			if i == length -1:
				try:
					cxt.bind(self.subName(name_list, i, i), obj)
				except CosNaming.NamingContext.AlreadyBound:
					cxt.rebind(self.subName(name_list, i, i), obj)
				return
			else:
				if self.objIsNamingContext(cxt):
					cxt = self.bindOrResolveContext(cxt,self.subName(name_list, i, i))
				else:
					raise CosNaming.NamingContext.CannotProceed(cxt, self.subName(name_list, i))
		return


	##
	# @if jp
	#  Object �� rebind ����
	# 
	# name_list �ǻ��ꤵ�줿 Binding �����Ǥ�¸�ߤ����������� bind() ��Ʊ��
	# �Ǥ��롣�Х���ǥ��󥰤����Ǥ�¸�ߤ�����ˤϡ��������Х���ǥ��󥰤�
	# �֤��������롣
	# @param name_list(CosNaming.NameComponent��list) ���֥������Ȥ��դ���̾���� NameComponent
	# @param obj(CORBA::Object) ��Ϣ�դ����륪�֥�������
	# @param force(bool) true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
	# @else
	# 
	# @endif
	def rebind(self, name_list, obj, force=True):
		if force == None:
			force = True
			
		try:
			self._rootContext.rebind(name_list, obj)

		except CosNaming.NamingContext.NotFound:
			if force:
				self.rebindRecursive(self._rootContext, name_list, obj)
			else:
				raise

		except CosNaming.NamingContext.CannotProceed, err:
			if force:
				self.rebindRecursive(err.cxt, err,rest_of_name, obj)
			else:
				raise
			
		return


	##
	# @if jp
	#  Object �� rebind ����
	# 
	# Object �� rebind ����ݤ�Ϳ����̾����ʸ����ɽ���Ǥ��뤳�Ȱʳ��� rebind()
	# ��Ʊ���Ǥ��롣rebind(toName(string_name), obj) ��������
	# @param string_name(string) ���֥������Ȥ��դ���̾����ʸ����ɽ��
	# @param obj(CORBA::Object) ��Ϣ�դ����륪�֥�������
	# @param force(bool) true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
	# @exception NotFound ����� <c_1, c_2, ..., c_(n-1)> ��¸�ߤ��ʤ���
	# @exception CannotProceed ���餫����ͳ�ǽ������³�Ǥ��ʤ���
	# @exception InvalidName ���� name ��̾����������
	# @else
	# 
	# @endif
	def rebindByString(self, string_name, obj, force=True):
		self.rebind(self.toName(string_name), obj, force)

		return


	##
	# @if jp
	#  ����Υ���ƥ����Ȥ� bind ���ʤ��� Object �� rebind ����
	# 
	# name <c_n> �ǻ��ꤵ�줿 NamingContext �⤷���� Object �����Ǥ�¸�ߤ���
	# ��������� bindRecursive() ��Ʊ���Ǥ��롣
	# 
	# name <c_n> �ǻ��ꤵ�줿�Х���ǥ��󥰤����Ǥ�¸�ߤ�����ˤϡ�
	# �������Х���ǥ��󥰤��֤��������롣
	# @param context(CosNaming.NameComponent) ���֥������Ȥ��դ���̾����ʸ����ɽ��
	# @param name_list(CosNaming.NameComponent�Υꥹ��) ��Ϣ�դ����륪�֥�������
	# @param obj(CORBA::Object) true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
	# @exception CannotProceed ����Υ���ƥ����Ȥ����Ǥ��ʤ���
	# @exception InvalidName Ϳ����줿 name ��������
	# @else
	# 
	# @endif
	def rebindRecursive(self, context, name_list, obj):
		length = len(name_list)
		for i in range(length):
			if i == length - 1:
				context.rebind(self.subName(name_list, i, i), obj)
				return
			else:
				if self.objIsNamingContext(context):
					try:
						context = context.bind_new_context(self.subName(name_list, i, i))
					except CosNaming.NamingContext.AlreadyBound:
						obj_ = context.resolve(self.subName(name_list, i, i))
						context = obj_._narrow(CosNaming.NamingContext)
				else:
					raise CosNaming.NamingContext.CannotProceed(context, self.subName(name_list, i))
		return


	##
	# @if jp
	#  NamingContext �� bind ����
	# 
	# bind ����륪�֥������Ȥ� NamingContext �Ǥ��뤳�Ȥ������ bind() 
	# ��Ʊ���Ǥ��롣
	# @param name(CosNaming.NameComponent�Υꥹ��) ���֥������Ȥ��դ���̾����ʸ����ɽ���ޤ��ϡ�NameComponent�Υꥹ��
	# @param name_cxt(CosNaming.NameComponent) ��Ϣ�դ����� NamingContext
	# @param force(bool) true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
	# @else
	# 
	# @endif
	def bindContext(self, name, name_cxt, force=True):
		if isinstance(name, basestring):
			self.bind(self.toName(name), name_cxt, force)
		else:
			self.bind(name, name_cxt, force)
		return


	##
	# @if jp
	#  NamingContext �� bind ����
	# 
	# bind ����륪�֥������Ȥ� NamingContext �Ǥ��뤳�Ȥ������
	# bindRecursive() ��Ʊ���Ǥ��롣
	# @param context(CosNaming.NameComponent) bind �򳫻Ϥ��롡NamingContext
	# @param name_list(CosNaming.NameComponent�Υꥹ��) ���֥������Ȥ��դ���̾���Υ͡��ॳ��ݡ��ͥ��
	# @param name_cxt(CosNaming.NameComponent) ��Ϣ�դ����� NamingContext
	# @else
	# 
	# @endif
	def bindContextRecursive(self, context, name_list, name_cxt):
		self.bindRecursive(context, name_list, name_cxt)
		return


	##
	# @if jp
	#  NamingContext �� rebind ����
	# 
	# name �ǻ��ꤵ�줿����ƥ����Ȥ����Ǥ�¸�ߤ����������� bindContext() 
	# ��Ʊ���Ǥ��롣
	# �Х���ǥ��󥰤����Ǥ�¸�ߤ�����ˤϡ��������Х���ǥ��󥰤�
	# �֤��������롣
	# @param name(CosNaming.NameComponent�Υꥹ��) ���֥������Ȥ��դ���̾���Υ͡��ॳ��ݡ��ͥ�Ȥޤ��ϡ�ʸ����
	# @param name_cxt(CosNaming.NameComponent) ��Ϣ�դ����� NamingContext
	# @param force(bool) true�ξ�硢����Υ���ƥ����Ȥ���Ū�˥Х���ɤ���
	# @else
	# 
	# @endif
	def rebindContext(self, name, name_cxt, force=True):
		if isinstance(name, basestring):
			self.rebind(self.toName(name), name_cxt, force)
		else:
			self.rebind(name, name_cxt, force)
		return


	##
	# @if jp
	#  NamingContext �� �Ƶ�Ū��rebind ����
	# @param context(CosNaming.NameComponent) NamingContext
	# @param name_list(CosNaming.NameComponent��list) NamingContext�Υꥹ��
	# @param name_cxt(CosNaming.NameComponent) NamingContext
	# @else
	# 
	# @endif
	def rebindContextRecursive(self, context, name_list, name_cxt):
		self.rebindRecursive(context, name_list, name_cxt)
		return


	##
	# @if jp
	#  Object �� name �����褹��
	# 
	# name �� bind ����Ƥ��륪�֥������Ȼ��Ȥ��֤���
	# �͡��ॳ��ݡ��ͥ�� <c_1, c_2, ... c_n> �ϺƵ�Ū�˲�褵��롣
	# 
	# CosNaming::resolve() �Ȥۤ�Ʊ����Ư���򤹤뤬�����Ϳ����줿
	# �͡��ॵ���ФΥ롼�ȥ���ƥ����Ȥ��Ф��� resolve() ���ƤӽФ��������
	# �ۤʤ롣
	# @param name(CosNaming.NameComponent�Υꥹ�� �ޤ��ϡ� str) ��褹�٤����֥������Ȥ�̾���Υ͡��ॳ��ݡ��ͥ��
	# �������������ޤ��ϡ���褹�٤����֥������Ȥ�̾����ʸ����ɽ��
	# @return ��褵�줿���֥������Ȼ���
	# @else
	# @endif
	def resolve(self, name):
		if isinstance(name, basestring):
			name_ = self.toName(name)
		else:
			name_ = name
			
		try:
			obj = self._rootContext.resolve(name_)
			return obj
		except CosNaming.NamingContext.NotFound, ex:
			return None


	##
	# @if jp
	#  ���ꤵ�줿̾���Υ��֥������Ȥ� bind ��������
	# 
	# name �� bind ����Ƥ��륪�֥������Ȼ��Ȥ��֤���
	# �͡��ॳ��ݡ��ͥ�� <c_1, c_2, ... c_n> �ϺƵ�Ū�˲�褵��롣
	# 
	# CosNaming::unbind() �Ȥۤ�Ʊ����Ư���򤹤뤬�����Ϳ����줿
	# �͡��ॵ���ФΥ롼�ȥ���ƥ����Ȥ��Ф��� unbind() ���ƤӽФ��������
	# �ۤʤ롣
	# @param name(CosNaming.NameComponent�Υꥹ�� �ޤ��ϡ�str) ��褹�٤����֥������Ȥ�̾���Υ͡��ॳ��ݡ��ͥ��
	# �������������ޤ��ϡ���褹�٤����֥������Ȥ�̾����ʸ����ɽ��
	# @return ��褵�줿���֥������Ȼ���
	# @else
	# @endif
	def unbind(self, name):
		if isinstance(name, basestring):
			name_ = self.toName(name)
		else:
			name_ = name

		self._rootContext.unbind(name_)
		return


	##
	# @if jp
	#  ����������ƥ����Ȥ���������
	# 
	# Ϳ����줿�͡��ॵ���о���������줿 NamingContext ���֤���
	# �֤��줿 NamingContext �� bind ����Ƥ��ʤ���
	# @return �������줿������ NamingContext
	# @else
	# @endif
	def newContext(self):
		return self._rootContext.new_context()


	##
	# @if jp
	#  ����������ƥ����Ȥ� bind ����
	# 
	# Ϳ����줿 name ���Ф��ƿ���������ƥ����Ȥ�Х���ɤ��롣
	# �������줿��NamingContext �ϥ͡��ॵ���о���������줿��ΤǤ��롣
	# @param name(CosNaming.NameComponent�Υꥹ�� �ޤ��ϡ� str) NamingContext���դ���̾���Υ͡��ॳ��ݡ��ͥ��
	# �������������ޤ��ϡ���褹�٤����֥������Ȥ�̾����ʸ����ɽ��
	# @return �������줿������ NamingContext
	# @else
	# @endif
	def bindNewContext(self, name, force=True):
		if force == None:
			force = True
			
		if isinstance(name, basestring):
			name_ = self.toName(name)
		else:
			name_ = name

		try:
			return self._rootContext.bind_new_context(name_)
		except CosNaming.NamingContext.NotFound:
			if force:
				self.bindRecursive(self._rootContext, name_, self.newContext())
			else:
				raise
		except CosNaming.NamingContext.CannotProceed, err:
			if force:
				self.bindRecursive(err.cxt, err.rest_of_name, self.newContext())
			else:
				raise
		return None


	##
	# @if jp
	#  NamingContext ���󥢥��ƥ��ֲ�����
	# 
	# context �ǻ��ꤵ�줿 NamingContext ���󥢥��ƥ��ֲ����롣
	# context ��¾�Υ���ƥ����Ȥ��Х���ɤ���Ƥ������ NotEmpty �㳰��
	# ȯ�����롣
	# @param context(CosNaming.NameComponent) �󥢥��ƥ��ֲ����� NamingContext
	# @else
	#  Destroy the naming context
	# 
	# Delete the specified naming context.
	# any bindings should be <unbind> in which the given context is bound to
	# some names before invoking <destroy> operation on it. 
	# @param context NamingContext which is destroied.
	# @endif
	def destroy(self, context):
		context.destroy()


	##
	# @if jp
	#  NamingContext ��Ƶ�Ū�˲��ä��󥢥��ƥ��ֲ�����
	# @param context(CosNaming.NameComponent) 
	# @else
	#  Destroy the naming context recursively
	# @param context(CosNaming.NameComponent)
	# @endif
	def destroyRecursive(self, context):
		cont = True
		bl = []
		bi = 0
		bl, bi = context.list(self._blLength)
		while cont:
			for i in range(len(bl)):
				if bl[i].binding_type == CosNaming.ncontext:
					obj = context.resolve(bl[i].binding_name)
					next_context = obj._narrow(CosNaming.NamingContext)

					self.destroyRecursive(next_context)
					context.unbind(bl[i].binding_name)
					next_context.destroy()
				elif bl[i].binding_type == CosNaming.nobject:
					context.unbind(bl[i].binding_name)
				else:
					assert(0)
			if CORBA.is_nil(bi):
				cont = False
			else:
				bi.next_n(self._blLength, bl)

		if not (CORBA.is_nil(bi)):
			bi.destroy()
		return


	##
	# @if jp
	#  ���٤Ƥ� Binding ��������
	# @else
	#  Destroy all binding
	# @endif
	def clearAll(self):
		self.destroyRecursive(self._rootContext)
		return


	##
	# @if jp
	#  Ϳ����줿 NamingContext �� Binding ���������
	# @param name_cxt(CosNaming.NameComponent)
	# @param how_many(long)
	# @param rbl(list)
	# @param rbi(list)
	# @else
	#  Get Binding on the NamingContextDestroy all binding
	# @param name_cxt(CosNaming.NameComponent)
	# @param how_many(long)
	# @param rbl(list)
	# @param rbi(list)
	# @endif
	def list(self, name_cxt, how_many, rbl, rbi):
		bl, bi = name_cxt.list(how_many)

		for i in bl:
			rbl.append(bl)

		rbi.append(bi)
	

	#============================================================
	# interface of NamingContext
	#============================================================

	##
	# @if jp
	#  Ϳ����줿 NameComponent ��ʸ����ɽ�����֤�
	# @param name_list(CosNaming.NameComponent�Υꥹ��)
	# @else
	#  Get string representation of given NameComponent
	# @param name_list(list of CosNaming.NameComponent)
	# @endif
	def toString(self, name_list):
		if len(name_list) == 0:
			raise CosNaming.NamingContext.InvalidName

		slen = self.getNameLength(name_list)
		string_name = [""]
		self.nameToString(name_list, string_name, slen)

		return string_name


	##
	# @if jp
	#  Ϳ����줿ʸ����ɽ���� NameComponent ��ʬ�򤹤�
	# @param sname(string)
	# @else
	#  Get NameComponent from gien string name representation
	# @param sname(string)
	# @endif
	def toName(self, sname):
		if not sname:
			raise CosNaming.NamingContext.InvalidName

		string_name = sname
		name_comps = []

		nc_length = 0
		nc_length = self.split(string_name, "/", name_comps)
		if not (nc_length > 0):
			raise CosNaming.NamingContext.InvalidName

		name_list = [CosNaming.NameComponent("","") for i in range(nc_length)]

		for i in range(nc_length):
			pos = string.rfind(name_comps[i][0:],".")
			if pos == -1:
				name_list[i].id   = name_comps[i]
				name_list[i].kind = ""
			else:
				name_list[i].id   = name_comps[i][0:pos]
				name_list[i].kind = name_comps[i][(pos+1):]

		return name_list


	##
	# @if jp 
	#  Ϳ����줿 addre �� string_name ���� URLɽ�����������
	# @param addr(string)
	# @param string_name(string)
	# @else
	#  Get URL representation from given addr and string_name
	# @param addr(string)
	# @param string_name(string)
	# @endif
	def toUrl(self, addr, string_name):
		return self._rootContext.to_url(addr, string_name)


	##
	# @if jp 
	#  Ϳ����줿ʸ����ɽ���� resolve �����֥������Ȥ��֤�
	# @param string_name(string)
	# @else
	#  Resolve from name of string representation and get object 
	# @param string_name(string)
	# @endif
	def resolveStr(self, string_name):
		return self.resolve(self.toName(string_name))


	#============================================================
	# Find functions
	#============================================================

	##
	# @if jp
	#  ̾����Х���ɤޤ��ϲ�褹��
	# @param context(CosNaming.NameComponent)
	# @param name_list(CosNaming.NameComponent�Υꥹ��)
	# @param obj(CORBA::Object)
	# @else
	#  Bind of resolve the given name component
	# @param context(CosNaming.NameComponent)
	# @param name_list(list of CosNaming.NameComponent)
	# @param obj(CORBA::Object)
	# @endif
	def bindOrResolve(self, context, name_list, obj):
		try:
			context.bind_context(name_list, obj)
			return obj
		except CosNaming.NamingContext.AlreadyBound:
			obj = context.resolve(name_list)
			return obj
		return CORBA.Object._nil


	##
	# @if jp
	#  ̾����Х���ɤޤ��ϲ�褹��
	# @param context(CosNaming.NameComponent)
	# @param name_list(CosNaming.NameComponent�Υꥹ��)
	# @param new_context(CosNaming.NameComponent)
	# @else
	#  Bind of resolve the given name component
	# @endif
	def bindOrResolveContext(self, context, name_list, new_context=None):
		if new_context == None:
			new_cxt = self.newContext()
		else:
			new_cxt = new_context

		obj = self.bindOrResolve(context, name_list, new_cxt)
		return obj._narrow(CosNaming.NamingContext)


	##
	# @if jp
	#  �͡��ॵ���Ф�̾�����������
	# @return string
	# @else
	#  Get the name of naming server
	# @return string
	# @endif
	def getNameServer(self):
		return self._nameServer


	##
	# @if jp
	#  �롼�ȥ���ƥ����Ȥ��������
	# @return CosNaming.NameComponent
	# @else
	#  Get the root context
	# @return CosNaming.NameComponent
	# @endif
	def getRootContext(self):
		return self._rootContext


	##
	# @if jp 
	#  ���֥������Ȥ��͡��ߥ󥰥���ƥ����Ȥ�Ƚ�̤���
	# @param obj(CORBA::Object)
	# @else
	#  Whether the object is NamingContext
	# @param obj(CORBA::Object)
	# @endif
	def objIsNamingContext(self, obj):
		nc = obj._narrow(CosNaming.NamingContext)
		if CORBA.is_nil(nc):
			return False
		else:
			return True


	##
	# @if jp
	#  Ϳ����줿̾�����͡��ߥ󥰥���ƥ����Ȥ��ɤ���
	# @param name_list(CosNaming.NameComponent�Υꥹ��)
	# @else
	#  Whether the given name component is NamingContext
	# @param name_list(list of CosNaming.NameComponent)
	# @endif
	def nameIsNamingContext(self, name_list):
		return self.objIsNamingContext(self.resolve(name_list))


	##
	# @if jp
	#  �͡��ॳ��ݡ��ͥ�Ȥ���ʬ���֤�
	# @param name_list(CosNaming.NameComponent�Υꥹ��)
	# @param begin(long)
	# @param end(long)
	# @else
	#  Get subset of given name component
	# @param name_list(list of CosNaming.NameComponent)
	# @param begin(long)
	# @param end(long)
	# @endif 
	def subName(self, name_list, begin, end = None):
		if end == None or end < 0:
			end = len(name_list) - 1

		sub_len = end - (begin -1)
		objId = ""
		kind  = ""
		
		sub_name = []
		for i in range(sub_len):
			sub_name.append(name_list[begin + i])

		return sub_name


	##
	# @if jp
	#  �͡��ॳ��ݡ��ͥ�Ȥ�ʸ����ɽ�����������
	# @param name_list(CosNaming.NameComponent�Υꥹ��)
	# @param string_name(string)
	# @param slen(long)
	# @else
	#  Get string representation of name component
	# @param name_list(list of CosNaming.NameComponent)
	# @param string_name(string)
	# @param slen(long)
	# @endif 
	def nameToString(self, name_list, string_name, slen):

		for i in range(len(name_list)):
			for id_ in name_list[i].id:
				if id_ == "/" or id_ == "." or id_ == "\\":
					string_name[0] += "\\"
				string_name[0] += id_

			if name_list[i].id == "" or name_list[i].kind != "":
				string_name[0] += "."

			for kind_ in name_list[i].kind:
				if kind_ == "/" or kind_ == "." or kind_ == "\\":
					string_name[0] += "\\"
				string_name[0] += kind_

			string_name[0] += "/"


	##
	# @if jp
	#  �͡��ॳ��ݡ��ͥ�Ȥ�ʸ����ɽ������ʸ��Ĺ���������
	# @param name_list(CosNaming.NameComponent�Υꥹ��)
	# @else
	#  Get string length of the name component's string representation
	# @param name_list(list of CosNaming.NameComponent)
	# @endif
	def getNameLength(self, name_list):
		slen = 0

		for i in range(len(name_list)):
			for id_ in name_list[i].id:
				if id_ == "/" or id_ == "." or id_ == "\\":
					slen += 1
				slen += 1
			if name_list[i].id == "" or name_list[i].kind == "":
				slen += 1

			for kind_ in name_list[i].kind:
				if kind_ == "/" or kind_ == "." or kind_ == "\\":
					slen += 1
				slen += 1

			slen += 1

		return slen


	##
	# @if jp
	#  ʸ�����ʬ��
	# @param input(string)
	# @param delimiter(string)
	# @param results(list of string)
	# @else
	#  Split of string
	# @param input(string)
	# @param delimiter(string)
	# @param results(list of string)
	# @endif
	def split(self, input, delimiter, results):
		delim_size = len(delimiter)
		found_pos = begin_pos = pre_pos = substr_size = 0

		if input[0:delim_size] == delimiter:
			begin_pos = pre_pos = delim_size

		while 1:
			found_pos = string.find(input[begin_pos:],delimiter)
			
			if found_pos == -1:
				results.append(input[pre_pos:])
				break

			if found_pos > 0 and input[found_pos - 1] == "\\":
				begin_pos += found_pos + delim_size
			else:
				substr_size = found_pos + (begin_pos - pre_pos)
				if substr_size > 0:
					results.append(input[pre_pos:(pre_pos+substr_size)])
				begin_pos += found_pos + delim_size
				pre_pos   = begin_pos

		return len(results)
