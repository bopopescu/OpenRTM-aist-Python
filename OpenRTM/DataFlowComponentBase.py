#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file DataFlowComponentBase.py
 \brief DataFlowParticipant RT-Component base class
 \date $Date: 2007/09/04$
 \author Noriaki Ando <n-ando@aist.go.jp>

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""

import RTC, RTC__POA
import OpenRTM


class DataFlowComponentBase(OpenRTM.RTObject_impl):
	
	"""
	\if jp
	\class DataFlowComponentBas
	\brief DataFlowComponentBase ���饹
	\else
	\class DataFlowComponentBase
	\brief DataFlowComponentBase class
	\endif
	"""


	def __init__(self, manager):
		"""
		\if jp
		\brief ���󥹥ȥ饯��
		\param manager(OpenRTM.Manager)
		\else
		\brief Constructor
		\param manager(OpenRTM.Manager)
		\endif
		"""
		OpenRTM.RTObject_impl.__init__(self, manager)
		self._ref = self._this()
		self._objref = self._ref


	def __del__(self):
		"""
		\if jp
		\brief �ǥ��ȥ饯��
		\else
		\brief Destructor
		\endif
		"""
		pass


	def init(self):
		"""
		\if jp
		\brief �����
		\else
		\brief Initialization
		\endif
		"""
		pass


