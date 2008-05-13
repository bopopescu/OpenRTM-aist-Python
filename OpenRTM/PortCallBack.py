#!/usr/bin/env python
# -*- coding: euc-jp -*-


"""
  \file PortCallBack.py
  \brief PortCallBack class
  \date $Date: 2007/09/20 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2006
      Noriaki Ando
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""
 

#============================================================
# callback functor base classes
#

class OnWrite:
	"""
	\if jp
	\class OnWrite
	\brief write() ���Υ�����Хå���ݥ��饹

	DataPort�ΥХåե��˥ǡ�����write()��������
	���Υ�����Хå����ƤФ�롣

	\else
	\class OnPut
	\brief OnPut abstract class

	\endif
	"""
	def __init__(self):
		pass

	def __call__(self, value):
		pass


class OnWriteConvert:
	"""
	\if jp
	\class OnWriteConvert
	\brief write() ���Υǡ����Ѵ�������Хå���ݥ��饹
	
	InPort�ΥХåե��˥ǡ����� write()�������ˤ��Υ�����Хå����ƤФ졢
	���Υ�����Хå�������ͤ��Хåե��˳�Ǽ����롣
	
	\else
	\class OnWriteConvert
	\brief OnWriteConvert abstract class
	
	\endif
	"""
	def __init__(self):
		pass


	def __call__(self,value):
		pass


class OnRead:
	"""
	\if jp
	\class OnRead
	\brief read() ���Υ�����Хå���ݥ��饹
	
	DataPort�ΥХåե�����ǡ�����read()��������
	���Υ�����Хå����ƤФ�롣
	
	\else
	\class OnRead
	\brief OnRead abstract class
	
	\endif
	"""
	def __init__(self):
		pass


	def __call__(self):
		pass


class OnReadConvert:
	"""
	\if jp
	\class OnReadConvert
	\brief read() ���Υǡ����Ѵ�������Хå���ݥ��饹
	
	InPort�ΥХåե�����ǡ����� read()�������ˤ��Υ�����Хå����ƤФ졢
	���Υ�����Хå�������ͤ�read()������ͤȤʤ롣
	
	\else
	\class OnReadConvert
	\brief OnReadConvert abstract class
	
	\endif
	"""
	def __init__(self):
		pass


	def __call__(self,value):
		pass
  

class OnOverflow:
	"""
	\if jp
	\class OnOverflow
	\brief �Хåե������С��ե����Υ�����Хå���ݥ��饹
	
	�Хåե��˥ǡ�����put()���������Хåե������С��ե���
	���������ˤ��Υ�����Хå����ƤФ�롣
	
	\else
	\class OnOverflow
	\brief OnOverflow abstract class
	
	\endif
	"""
	def __init__(self):
		pass


	def __call__(self,value):
		pass


class OnUnderflow:
	"""
	\if jp
	\class OnUnderflow
	\brief Underflow ���Υ�����Хå���ݥ��饹
	
	InPort�ΥХåե��˥ǡ�����put()�������ˤ��Υ�����Хå����ƤФ�롣
	
	\else
	\class OnUnderflow
	\brief OnUnderflow abstract class
    
	\endif
	"""
	def __init__(self):
		pass


	def __call__(self,value):
		pass
