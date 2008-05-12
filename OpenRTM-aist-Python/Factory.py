#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file Factory.py
 \brief RTComponent factory class
 \date $Date: 2006/11/06 01:28:36 $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2003-2005
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""

import OpenRTM


def Delete(rtc):
    del rtc


class FactoryBase:
	
	"""
	\if jp
	\class FactoryBase
	\brief FactoryBase ���쥯�饹
	
	����ݡ��ͥ�ȥե����ȥ�δ��쥯�饹��
	\else
	\class FactoryBase
	\brief FactoryBase base class
	
	RTComponent factory base class.
	\endif
	"""


	def __init__(self, profile):
		"""
		\if jp
		\brief FactoryBase ���饹���󥹥ȥ饯��
	
		FactoryBase ���饹�Υ��󥹥ȥ饯����
		\param profile(OpenRTM.Properties) ����ݡ��ͥ�ȤΥץ�ե�����
		\else
		\brief FactoryBase class constructor.
		
		FactoryBase class constructor.
		\param profile(OpenRTM.Properties) component profile
		\endif
		"""

		## \var self._Profile Component profile
		self._Profile = profile

		## \var self._Number Number of current component instances.
		self._Number = -1
		
		pass


	def __del__(self):
		pass


	def create(self, mgr):
		"""
		\if jp
		\brief ����ݡ��ͥ�Ȥ�����
		
		Python �Ǽ������줿 RTComponent �Υ��󥹥��󥹤��������롣
		���۴ؿ���
		\param mgr(OpenRTM.Manager) Manager���֥�������
		\else
		\brief Create component
		
		Create component implemented in Python.
		virtual method.
		\param mgr(OpenRTM.Manager) Manager object
		\endif
		"""
		pass


	def destroy(self, comp):
		"""
		\if jp
		\brief ����ݡ��ͥ�Ȥ��˴�
		
		RTComponent �Υ��󥹥��󥹤��˴����롣
		���۴ؿ���
		\param comp(OpenRTM.RTObject_impl) RtcBase���֥�������
		\else
		\brief Destroy component
		
		Destroy component instance)
		virtual method.
		\param comp(OpenRTM.RTObject_impl) RtcBase object
		\endif
		"""
		pass


	def profile(self):
		"""
		\if jp
		\brief ����ݡ��ͥ�ȥץ�ե�����μ���
		
		����ݡ��ͥ�ȤΥץ�ե�������������
		\else
		\brief Get component profile
	
		Get component profile.
		\endif
		"""
		return self._Profile


	def number(self):
		"""
		\if jp
		\brief ���ߤΥ��󥹥��󥹿�
		
		����ݡ��ͥ�Ȥθ��ߤΥ��󥹥��󥹿���������롣
		\else
		\brief Get number of component instances
		
		Get number of current component instances.
		\endif
		"""
		return self._Number



class FactoryPython(FactoryBase):
	
	"""
	\if jp
	\class FactoryPython
	\brief FactoryPython ���饹
	
	Python�ѥ���ݡ��ͥ�ȥե����ȥꥯ�饹��
	\else
	\class FactoryPython
	\brief FactoryPython class
	
	RTComponent factory class for Python.
	\endif
	"""


	def __init__(self, profile, new_func, delete_func, policy=None):
		"""
		\if jp
		\brief FactoryPython ���饹���󥹥ȥ饯��
		
		FactoryPython ���饹�Υ��󥹥ȥ饯����
		�ץ�ե����롢���饹̾���˴��ؿ����֥������Ȥ�����˼�ꡢ
		����ݡ��ͥ�ȤΥե����ȥꥯ�饹���������롣
		\param profile(OpenRTM.Properties) ����ݡ��ͥ�ȤΥץ�ե�����
		\param new_func(create function object) ����ݡ��ͥ�ȥ��֥�������(���饹̾)
		\param delete_func(delete function object) ����ݡ��ͥ�Ȥ��˴��ؿ����֥�������
		\else
		\brief FactoryPython class constructor.
		
		FactoryPython class constructor.
		Create component factory class with three arguments:
		component profile, component class name and
		delete function object.
		\param profile(OpenRTM.Properties) Component profile
		\param new_func(create function object) Component name
		\param delete_func(delete function object) Delete function object
		\endif
		"""

		FactoryBase.__init__(self, profile)
		
		if policy == None:
			self._policy = OpenRTM.DefaultNumberingPolicy()
		else:
			self._policy = policy

		self._New = new_func
    
		self._Delete = delete_func


	def create(self, mgr):
		"""
		\if jp
		\brief ����ݡ��ͥ�Ȥ�����
	
		Python �Ǽ������줿 RTComponent �Υ��󥹥��󥹤��������롣
		\param mgr(OpenRTM.Manager) Manager���֥�������
		\else
		\brief Create component
		
		Create component implemented in Python.
		\param mgr(OpenRTM.Manager) Manager object
		\endif
		"""
		try:
			rtobj = self._New(mgr)
			if rtobj == 0:
				return None

			self._Number += 1
			
			rtobj.setProperties(self.profile())
			
			instance_name = rtobj.getTypeName()
			instance_name += self._policy.onCreate(rtobj)
			rtobj.setInstanceName(instance_name)

			return rtobj
		except:
			return None


	def destroy(self, comp):
		"""
		\if jp
		\brief ����ݡ��ͥ�Ȥ��˴�
	
		RTComponent �Υ��󥹥��󥹤��˴����롣
		\param comp(OpenRTM.RTObject_impl) RtcBase���֥�������
		\else
		\brief Destroy component
		
		Destroy component instance
		\param comp(OpenRTM.RTObject_impl) RtcBase object
		\endif
		"""
		self._Number -= 1
		self._policy.onDelete(comp)
		self._Delete(comp)
