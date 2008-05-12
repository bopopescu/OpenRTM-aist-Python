#!/usr/bin/env python 
# -*- coding: euc-jp -*-

"""
 \file PublisherBase.py
 \brief Publisher base class
 \date $Date: 2007/09/05$
 \author Noriaki Ando <n-ando@aist.go.jp>

 Copyright (C) 2006
     Noriaki Ando
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


class PublisherBase:
	"""
	\if jp

	\class PublisherBase

	\brief Publisher ���쥯�饹

	Publisher �δ��쥯�饹 PublisherBase.
	�Ƽ� Publisher �Ϥ��Υ��饹��Ѿ����ƾܺ٤�������롣

	\else

	\class PublisherBase

	\brief Base class of Publisher.

	A base class of Publisher.
	Variation of Publisher which implements details of Publisher
	inherits this PublisherBase class.

	\endif
	"""
	def __init__(self):
		pass

	def update(self):
		pass

	def release(self):
		pass
