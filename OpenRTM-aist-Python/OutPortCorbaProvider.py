#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
#  \file  OutPortCorbaProvider.py
#  \brief OutPortCorbaProvider class
#  \date  $Date: 2007/09/26 $
#  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.


from omniORB import any

import OpenRTM
import RTC, RTC__POA


class OutPortCorbaProvider(OpenRTM.OutPortProvider, RTC__POA.OutPortAny):
	"""
	\if jp
	\class OutPortCorbaProvider
	\brief OutPortCorbaProvider ���饹
	\else
	\class OutPortCorbaProvider
	\brief OutPortCorbaProvider class
	\endif
	"""
	
	def __init__(self, buffer_):
		"""
		\if jp
		\brief ���󥹥ȥ饯��
		  ���Υ��饹�Υ��󥹥����������ˤϡ��ݡ��ȥ��֥������Ȥ�
		  ������buffer_�Ȥ����Ϥ�ɬ�פ����롣
		\param buffer_(OpenRTM.BufferBase)
		\else
		\brief Constructor
		\param buffer_(OpenRTM.BufferBase)
		\endif
		"""
		OpenRTM.OutPortProvider.__init__(self)
		self._buffer = buffer_

		# PortProfile setting
		self.setDataType(self._buffer.getPortDataType())
		self.setInterfaceType("CORBA_Any")
		self.setDataFlowType("Push, Pull")
		self.setSubscriptionType("Flush, New, Periodic")

		# ConnectorProfile setting
		self._objref = self._this()
		OpenRTM.CORBA_SeqUtil.push_back(self._properties,
										OpenRTM.NVUtil.newNV("dataport.corba_any.outport_ref",
															 self._objref))
    
	def __del__(self):
		"""
		\if jp
		\brief �ǥ��ȥ饯��
		\else
		\brief Destructor
		\endif
		"""
		pass


	def get(self):
		"""
		 \return CORBA.Any
		"""
		data = [None]
		self._buffer.read(data)
		try:
			retval = any.to_any(data[0])
		except:
			return None

		return retval
