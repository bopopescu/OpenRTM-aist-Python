#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file DataOutPort.py
  \brief Base class of OutPort
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


import OpenRTM
import RTC, RTC__POA


class DataOutPort(OpenRTM.PortBase):
	
	"""
	\if jp
	\class DataOutPort
	\brief InPort �� Port
	\else
	\class DataOutPort
	\brief InPort abstruct class
	\endif
	"""


	def __init__(self, name, outport):
		"""
		\if jp
		\brief ���󥹥ȥ饯��
		\param name(string)
		\param outport(OpenRTM.OutPort)
		\else
		\brief Constructor
		\param name(string)
		\param outport(OpenRTM.OutPort)
		\endif
		"""
		OpenRTM.PortBase.__init__(self, name)
		self._outport = outport
		# PortProfile::properties ������
		self.addProperty("port.port_type", "DataOutPort")
		self._providers = []
		self._providers.append(OpenRTM.OutPortCorbaProvider(outport))
		self._providers[-1].publishInterfaceProfile(self._profile.properties)
		self._consumers = []
		self._consumers.append(OpenRTM.InPortCorbaConsumer(outport))
		self._pf = OpenRTM.PublisherFactory()


	def __del__(self):
		"""
		\if jp
		\brief �ǥ��ȥ饯��
		\else
		\brief Destructor
		\endif
		"""
		pass

    
	"""
      \if jp
      \brief [CORBA interface] Port ����³��Ԥ�
     
      OutPort �� InPort �Ȥ���³��Ԥ���
     
      OutPort ¦�� connect() �Ǥϰʲ��Υ������󥹤ǽ������Ԥ��롣
     
      1. OutPort �˴�Ϣ���� connector �������������ӥ��å�
     
      2. InPort�˴�Ϣ���� connector ����μ���
       - ConnectorProfile::properties["dataport.corba_any.inport_ref"]��
         OutPortAny �Υ��֥������ȥ�ե���󥹤����ꤵ��Ƥ����硢
         ��ե���󥹤��������Consumer���֥������Ȥ˥��åȤ��롣
         ��ե���󥹤����åȤ���Ƥ��ʤ����̵�뤷�Ʒ�³��
         (OutPort��connect() �ƤӽФ��Υ���ȥ�ݥ���Ȥξ��ϡ�
         InPort�Υ��֥������ȥ�ե���󥹤ϥ��åȤ���Ƥ��ʤ��Ϥ��Ǥ��롣)
      3. PortBase::connect() �򥳡���
         Port����³�δ��ܽ������Ԥ��롣
      4. �嵭2.��InPort�Υ�ե���󥹤������Ǥ��ʤ���С�����InPort��
         ��Ϣ���� connector �����������롣
     
      5. ConnectorProfile::properties ��Ϳ����줿���󤫤顢
         OutPort¦�ν����������Ԥ���
     
      - [dataport.interface_type]
      -- CORBA_Any �ξ��: 
         InPortAny ���̤��ƥǡ����򴹤���롣
         ConnectorProfile::properties["dataport.corba_any.inport_ref"]��
         InPortAny �Υ��֥������ȥ�ե���󥹤򥻥åȤ��롣
      -- RawTCP �ξ��: Raw TCP socket ���̤��ƥǡ����򴹤���롣
         ConnectorProfile::properties["dataport.raw_tcp.server_addr"]
         ��InPort¦�Υ����Х��ɥ쥹�򥻥åȤ��롣
     
      - [dataport.dataflow_type]
      -- Push�ξ��: Subscriber���������롣Subscriber�Υ����פϡ�
         dataport.subscription_type �����ꤵ��Ƥ��롣
      -- Pull�ξ��: InPort¦���ǡ�����Pull���Ǽ������뤿�ᡢ
         �ä˲��⤹��ɬ�פ�̵����
     
      - [dataport.subscription_type]
      -- Once�ξ��: SubscriberOnce���������롣
      -- New�ξ��: SubscriberNew���������롣
      -- Periodic�ξ��: SubscriberPeriodic���������롣
     
      - [dataport.push_interval]
      -- dataport.subscription_type=Periodic�ξ����������ꤹ�롣
     
      6. �嵭�ν����Τ�����ĤǤ⥨�顼�Ǥ���С����顼�꥿���󤹤롣
         ����˽������Ԥ�줿����RTC::RTC_OK�ǥ꥿���󤹤롣
       
      \else
      \brief [CORBA interface] Connect the Port
      \endif
	"""


	def publishInterfaces(self, connector_profile):
		"""
		\if jp

		\brief Interface ������������

		���Υ��ڥ졼�����ϡ�notify_connect() �����������󥹤λϤ�˥�����
		�����ؿ��Ǥ��롣
		notify_connect() �Ǥϡ�

		- publishInterfaces()
		- connectNext()
		- subscribeInterfaces()
		- updateConnectorProfile()

		�ν�˴ؿ��������뤵����³�������Ԥ��롣
		<br>
		���Υ��ڥ졼�����ϡ������� connector_id ���Ф��Ƥ���³��������
		��¸�� connector_id ���Ф��ƤϹ�����Ŭ�ڤ˹Ԥ���ɬ�פ����롣

		\param connector_profile(RTC.ConnectorProfile) ��³�˴ؤ���ץ�ե��������
		\return ReturnCode_t ���Υ꥿���󥳡���

		\else

		\brief Publish interface information

		This operation is method that would be called at the
		beginning of the notify_connect() process sequence.
		In the notify_connect(), the following methods would be called in order.

		- publishInterfaces()
		- connectNext()
		- subscribeInterfaces()
		- updateConnectorProfile() 

		This operation should create the new connection for the new
		connector_id, and should update the connection for the existing
		connection_id.

		\param connector_profile(RTC.ConnectorProfile) The connection profile information
		\return The return code of ReturnCode_t type.

		\endif
		"""
		publish = self.publish(connector_profile.properties)
		for provider in self._providers:
			publish(provider)
		return RTC.RTC_OK


	def subscribeInterfaces(self, connector_profile):
		"""
		\if jp

		\brief Interface ������������

		���Υ��ڥ졼�����ϡ�notify_connect() �����������󥹤���֤˥�����
		�����ؿ��Ǥ��롣
		notify_connect() �Ǥϡ�

		- publishInterfaces()
		- connectNext()
		- subscribeInterfaces()
		- updateConnectorProfile()

		�ν�˴ؿ��������뤵����³�������Ԥ��롣

		\param connector_profile(RTC.ConnectorProfile) ��³�˴ؤ���ץ�ե��������
		\return ReturnCode_t ���Υ꥿���󥳡���

		\else

		\brief Publish interface information

		This operation is method that would be called at the
		mid-flow of the notify_connect() process sequence.
		In the notify_connect(), the following methods would be called in order.

		- publishInterfaces()
		- connectNext()
		- subscribeInterfaces()
		- updateConnectorProfile()

		\param connector_profile(RTC.ConnectorProfile) The connection profile information
		\return The return code of ReturnCode_t type.

		\endif
		"""
		subscribe = self.subscribe(prof=connector_profile)
		for consumer in self._consumers:
			subscribe(consumer)


		if not subscribe._consumer:
			return RTC.RTC_OK

    
		# Publisher������
		prop = OpenRTM.NVUtil.toProperties(connector_profile.properties)
		publisher = self._pf.create(subscribe._consumer.clone(), prop)

		# Publisher��OutPort�˥����å�
		self._outport.attach(connector_profile.connector_id, publisher)

		return RTC.RTC_OK


	def unsubscribeInterfaces(self, connector_profile):
		"""
		\if jp

		\brief Interface ����³��������

		���Υ��ڥ졼�����ϡ�notify_disconnect() �����������󥹤ν����˥�����
		�����ؿ��Ǥ��롣
		notify_disconnect() �Ǥϡ�
		- disconnectNext()
		- unsubscribeInterfaces()
		- eraseConnectorProfile()
		�ν�� protected �ؿ��������뤵����³����������Ԥ��롣

		\param connector_profile(RTC.ConnectorProfile) ��³�˴ؤ���ץ�ե��������

		\else

		\brief Disconnect interface connection

		This operation is method that would be called at the
		end of the notify_disconnect() process sequence.
		In the notify_disconnect(), the following methods would be called.
		- disconnectNext()
		- unsubscribeInterfaces()
		- eraseConnectorProfile() 

		\param connector_profile(RTC.ConnectorProfile) The connection profile information

		\endif
		"""
		publisher = self._outport.detach(connector_profile.connector_id)
		self._pf.destroy(publisher)
		return


	class publish:
		
		def __init__(self, prop):
			"""
			 \brief functor
			 \param prop(SDOPackage::NameValue�Υꥹ��)
			"""
			self._prop = prop

		def __call__(self, provider):
			"""
			 \brief operator()�μ���
			 \param provider(OpenRTM.OutPortProvider)
			"""
			provider.publishInterface(self._prop)


	class unsubscribe:
		
		def __init__(self, prop):
			"""
			 \brief functor
			 \param prop(SDOPackage::NameValue�Υꥹ��)
			"""
			self._prop = prop

		def __call__(self, consumer):
			"""
			 \brief operator()�μ���
			 \param consumer(OpenRTM.InPortConsumer)
			"""
			consumer.unsubscribeInterface(self._prop)


	class subscribe:
		
		def __init__(self, prof=None, subs=None):
			"""
			 \brief functor
			 \param prof(RTC.ConnectorProfile)
			 \param subs(subscribe)
			"""
			if prof and not subs:
				self._prof = prof
				self._consumer = None
			elif not prof and subs:
				self._prof = subs._prof
				self._consumer = subs._consumer
			else:
				print "DataOutPort.subscribe: Invalid parameter."


		def __call__(self, cons):
			"""
			 \brief operator()�μ���
			 \param cons(OpenRTM.InPortConsumer)
			"""
			if cons.subscribeInterface(self._prof.properties):
				self._consumer = cons
