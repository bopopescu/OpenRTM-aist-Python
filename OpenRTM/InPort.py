#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file InPort.py
  \brief InPort template class
  \date $Date: 2007/09/20 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2003-2005
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""
 

from omniORB import any
import sys
import traceback

import OpenRTM

TIMEOUT_TICK_USEC = 10.0
USEC_PER_SEC      = 1000000.0
TIMEOUT_TICK_SEC = TIMEOUT_TICK_USEC/USEC_PER_SEC


import time
class Time:
	
	def __init__(self):
		tm = time.time()
		tm_f       = tm - int(tm)     # �������μ��Ф�
		self.sec   = int(tm - tm_f)   # �������μ��Ф�
		self.usec  = int(tm_f * USEC_PER_SEC) # sec -> usec (micro second)


class InPort:
	
	"""
	\if jp
	
	\class InPort
	
	\brief InPort ���饹
 
        InPort �μ����Ǥ���
        ���󥹥�����������RingBuffer�ޤ��ϡ�NullBuffer�Υ��󥹥��󥹤�
		buff_�Ȥ����Ϥ�ɬ�פ����롣
        �ǡ����ϥե饰�ˤ�ä�̤�ɡ����ɾ��֤��������졢isNew(), getNewDataLen()
        getNewList(), getNewListReverse() ���Υ᥽�åɤˤ��ϥ�ɥ�󥰤��뤳�Ȥ�
        �Ǥ��롣
	\endif
	"""


	def __init__(self, name, value, buffer_,
				 read_block=False, write_block=False,
				 read_timeout=0, write_timeout = 0):
		"""
		\if jp
		\brief InPort ���饹���󥹥ȥ饯��
		
		InPort���饹�Υ��󥹥ȥ饯����
		\param name(string) InPort ̾��InPortBase:name() �ˤ�껲�Ȥ���롣
		\param value(data) ���� InPort �˥Х���ɤ���� T �����ѿ�
		\param buffer_(OpenRTM.BufferBase) InPort �ǻ��Ѥ���Хåե��Υ��֥�������
		\param read_block(bool)
		\param write_block(bool)
		\param read_timeout(int)
		\param write_timeout(int)
		\else
		\brief A constructor.
		
		Setting channel name and registering channel value.
		\param name(string) A name of the InPort. This name is referred by
		InPortBase::name().
		\param value(data) A channel value related with the channel.
		\param buffer_(OpenRTM.BufferBase) Buffer Object which is used in InPort 
		\param read_block(bool)
		\param write_block(bool)
		\param read_timeout(int)
		\param write_timeout(int)
		\endif
		"""
		self._buffer         = buffer_
		self._name           = name
		self._value          = value
		self._readBlock      = read_block
		self._readTimeout    = read_timeout
		self._writeBlock     = write_block
		self._writeTimeout   = write_timeout
		self._OnWrite        = None
		self._OnWriteConvert = None
		self._OnRead         = None
		self._OnReadConvert  = None
		self._OnOverflow     = None
		self._OnUnderflow    = None


	def __del__(self):
		"""
		\if jp
		\brief InPort���饹�ǥ��ȥ饯��
		
		InPort���饹�Υǥ��ȥ饯����
		\else
		\brief A destructor
		\endif
		"""
		pass


	def isNew(self):
		return self._buffer.isNew()
	

	def name(self):
		return self._name


	def write(self, value):
		"""
		\if jp
		\brief DataPort ���ͤ�񤭹���

		DataPort ���ͤ�񤭹��ࡣ

		- ������Хå��ե��󥯥� OnWrite �����åȤ���Ƥ����硢
			InPort ���ݻ�����Хåե��˽񤭹������� OnWrite ���ƤФ�롣
		- InPort ���ݻ�����Хåե��������С��ե��򸡽ФǤ���Хåե��Ǥ��ꡢ
			���ġ��񤭹���ݤ˥Хåե��������С��ե��򸡽Ф�����硢
			������Хå��ե��󥯥� OnOverflow ���ƤФ�롣
		- ������Хå��ե��󥯥� OnWriteConvert �����åȤ���Ƥ����硢
			�Хåե��񤭹��߻��ˡ�OnWriteConvert �� operator()() ������ͤ�
			�Хåե��˽񤭹��ޤ�롣
		- setWriteTimeout() �ˤ��񤭹��߻��Υ����ॢ���Ȥ����ꤵ��Ƥ����硢
			�����ॢ���Ȼ��֤����Хåե��ե���֤��������Τ��Ԥ���
			OnOverflow�����åȤ���Ƥ���Ф����ƤӽФ�����롣
		\param value(data)
		\else
		\brief 
		\param value(data)
		\endif
		"""
		if self._OnWrite:
			self._OnWrite(value)

		timeout = self._writeTimeout

		tm_pre = Time()

		# blocking and timeout wait
		while self._writeBlock and self._buffer.isFull():
			if self._writeTimeout < 0:
				time.sleep(TIMEOUT_TICK_SEC)
				continue

			# timeout wait
			tm_cur = Time()

			sec  = tm_cur.sec - tm_pre.sec
			usec = tm_cur.usec - tm_pre.usec

			timeout -= (sec * USEC_PER_SEC + usec)

			if timeout < 0:
				break

			tm_pre = tm_cur
			time.sleep(TIMEOUT_TICK_USEC)

		if self._buffer.isFull() and self._OnOverflow:
			self._OnOverflow(value)
			return False

		if not self._OnWriteConvert:
			self._buffer.put(value)
		else:
			self._buffer.put(self._OnWriteConvert(value))

		return True


	def read(self):
		"""
		\if jp
		\brief DataPort �����ͤ��ɤ߽Ф�

		DataPort �����ͤ��ɤ߽Ф�

		- ������Хå��ե��󥯥� OnRead �����åȤ���Ƥ����硢
			DataPort ���ݻ�����Хåե������ɤ߽Ф����� OnRead ���ƤФ�롣
		- DataPort ���ݻ�����Хåե�����������ե��򸡽ФǤ���Хåե��ǡ�
			���ġ��ɤ߽Ф��ݤ˥Хåե�����������ե��򸡽Ф�����硢
			������Хå��ե��󥯥� OnUnderflow ���ƤФ�롣
		- ������Хå��ե��󥯥� OnReadConvert �����åȤ���Ƥ����硢
			�Хåե��񤭹��߻��ˡ�OnReadConvert �� operator()() ������ͤ�
			read()������ͤȤʤ롣
		- setReadTimeout() �ˤ���ɤ߽Ф����Υ����ॢ���Ȥ����ꤵ��Ƥ����硢
			�Хåե���������ե����֤���������ޤǥ����ॢ���Ȼ��֤����Ԥ���
			OnUnderflow�����åȤ���Ƥ���Ф����ƤӽФ������
		\else
		\brief [CORBA interface] Put data on InPort
		\endif
		"""
		if self._OnRead:
			self._OnRead()

		timeout = self._readTimeout

		tm_pre = Time()

		# blocking and timeout wait
		while self._readBlock and self._buffer.isEmpty():
			if self._readTimeout < 0:
				time.sleep(TIMEOUT_TICK_SEC)
				continue

			# timeout wait
			tm_cur = Time()

			sec  = tm_cur.sec - tm_pre.sec
			usec = tm_cur.usec - tm_pre.usec
			
			timeout -= (sec * USEC_PER_SEC + usec)

			if timeout < 0:
				break

			tm_pre = tm_cur
			time.sleep(TIMEOUT_TICK_SEC)

		if self._buffer.isEmpty():
			if self._OnUnderflow:
				self._value = self._OnUnderflow()
			return self._value

		if not self._OnReadConvert:
			self._value = self._buffer.get()
			return self._value
		else:
			self._value = self._OnReadConvert(self._buffer.get())
			return self._value

		# never comes here
		return self._value


	def init(self, value):
		"""
		\if jp
		\brief InPort ��Υ�󥰥Хåե����ͤ�����
		
		InPort ��Υ�󥰥Хåե����ͤ��������롣
		\param value(data)
		\else
		\brief Initialize ring buffer value of InPort
		\endif
		"""
		pass
    
    
	def update(self):
		"""
		\if jp
		\brief �Х���ɤ��줿�ѿ�self._value�� InPort �Хåե��κǿ��ͤ��ɤ߹���
		
		�Х���ɤ��줿�ǡ����� InPort �κǿ��ͤ��ɤ߹��ࡣ
		\else
		\brief Read data from current InPort
		\endif
		"""
		try:
			self._value = self._buffer.get()
		except:
			if self._OnUnderflow:
				self._OnUnderflow()
			else:
				traceback.print_exception(*sys.exc_info())
				
		return
    
    
	"""
      \if jp
     
      \brief ̤�ɤο������ǡ��������������
     
      \else
     
      \brief Get number of new data to be read.
     
      \endif

	def getNewDataLen(self):
		return self._buffer.new_data_len()
	"""

    
	"""
      \if jp
     
      \brief ̤�ɤο������ǡ������������
     
      \else
     
      \brief Get new data to be read.
     
      \endif

	def getNewList(self):
		return self._buffer.get_new_list()

	"""

    
	"""
      \if jp
     
      \brief ̤�ɤο������ǡ�����ս�(��->��)�Ǽ�������
     
      \else
     
      \brief Get new data to be read.
     
      \endif

	def getNewListReverse(self):
		return self._buffer.get_new_rlist()
	"""


	def setOnWrite(self, on_write):
		"""
		\if jp
		\brief InPort �Хåե��˥ǡ������ϻ��Υ�����Хå�������
		
		InPort �����ĥХåե��˥ǡ�����put���줿�Ȥ��˸ƤФ�륳����Хå�
		���֥������Ȥ����ꤹ�롣���ꤵ��륳����Хå����֥������Ȥ�
		InPort<DataType>::OnPut���饹��Ѿ��������� const DataType& ��
		����� void �� operator() �ؿ�����������Ƥ���ɬ�פ����롣
		
		struct MyOnPutCallback : public InPort<DataType> {<br>
        void operator()(const DataType data) {<br>
		����<br>
        }<br>
		};<br>
		�Τ褦�˥�����Хå����֥������Ȥ��������<br>
		<br> 
		m_inport.setOnPut(new MyOnPutCallback());<br>
		�Τ褦�˥�����Хå����֥������Ȥ򥻥åȤ��롣
		\param on_write(function object)
		
		\else
		\brief Get new data to be read.
		\param on_write(function object)
		\endif
		"""
		self._OnWrite = on_write


	def setOnWriteConvert(self, on_wconvert):
		"""
		 \brief InPort �Хåե��˥ǡ������ϻ��Υ�����Хå�������
		 \param on_wconvert(function object)
		"""
		self._OnWriteConvert = on_wconvert


	def setOnRead(self, on_read):
		"""
		 \brief InPort �Хåե�����ǡ����ɤ߹��߻��Υ�����Хå�������
		 \param on_read(function object)
		"""
		self._OnRead = on_read


	def setOnReadConvert(self, on_rconvert):
		"""
		 \brief InPort �Хåե�����ǡ����ɤ߹��߻��Υ�����Хå�������
		 \param on_rconvert(function object)
		"""
		self._OnReadConvert = on_rconvert


	def setOnOverflow(self, on_overflow):
		"""
		 \brief InPort �Хåե��˴ؤ��륳����Хå�������
		 \param on_overflow(function object)
		"""
		self._OnOverflow = on_overflow


	def setOnUnderflow(self, on_underflow):
		"""
		 \brief InPort �Хåե��˴ؤ��륳����Хå�������
		 \param on_underflow(function object)
		"""
		self._OnUnderflow = on_underflow


	def getPortDataType(self):
		"""
		\brief �ǡ��������Τ���Υ᥽�å�
		�ǡ����η�̾��������뤿�ᡢInPortCorbaProvider����ƤФ�롣
		added by kurihara
		"""
		val = any.to_any(self._value)
		return str(val.typecode().name())
