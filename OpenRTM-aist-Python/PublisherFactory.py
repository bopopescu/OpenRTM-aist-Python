#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file  PublisherFactory.py
 \brief PublisherFactory class
 \date  $Date: 2007/09/05$
 \author Noriaki Ando <n-ando@aist.go.jp>

 Copyright (C) 2006
     Noriaki Ando
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""

from omniORB import any

import OpenRTM


class PublisherFactory:
	"""
	\if jp
	\class PublisherFactory
	\brief PublisherFactory ���饹

	���ƥ�ݥ��ʼ���
		����Ū�ˤ�Ǥ�դ�Publisher�������Ǥ���褦�ˤ��롣

	\else
	\class PublisherFactory
	\brief PublisherFactory class
	\endif
	"""

	def __init__(self):
		"""
		\if jp
		\brief ���󥹥ȥ饯��
		\else
		\brief Constructor
		\endif
		"""
		pass


	def __del__(self):
		"""
		\if jp
		\brief �ǥ��ȥ饯��
		\else
		\brief Destructor
		\endif
		"""
		pass


	def create(self, consumer, property):
		"""
		\if jp
		\brief Publisher������
		\param consumer(OpenRTM.InPortConsumer)
		\param property(OpenRTM.Properties)
		\else
		\brief Create Publisher
		\param consumer(OpenRTM.InPortConsumer)
		\param property(OpenRTM.Properties)
		\endif
		"""
		pub_type = property.getProperty("dataport.subscription_type", "New")

		if type(pub_type) != str :
			pub_type = str(any.from_any(pub_type,keep_structs=True))
		if pub_type == "New":
			return OpenRTM.PublisherNew(consumer, property)
		elif pub_type == "Periodic":
			return OpenRTM.PublisherPeriodic(consumer, property)
		elif pub_type == "Flush":
			return OpenRTM.PublisherFlush(consumer, property)

		return None

	def destroy(self, publisher):
		"""
		 \param publisher(OpenRTM.PublisherBase)
		"""
		if publisher:
			publisher.release()
		del publisher
