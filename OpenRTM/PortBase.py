#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
  \file PortBase.py
  \brief RTC's Port base class
  \date $Date: 2007/09/18 $
  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
 
  Copyright (C) 2006
      Task-intelligence Research Group,
      Intelligent Systems Research Institute,
      National Institute of
          Advanced Industrial Science and Technology (AIST), Japan
      All rights reserved.
"""


import threading

import OpenRTM
import RTC, RTC__POA


class ScopedLock:
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()



class PortBase(RTC__POA.Port):
	"""
	\if jp
	\class PortBase
	\brief Port �δ��쥯�饹

	RTC::Port �δ���Ȥʤ륯�饹��
	RTC::Port �Ϥۤ� UML Port �γ�ǰ��Ѿ����Ƥ��ꡢ�ۤ�Ʊ���Τ�ΤȤߤʤ�
	���Ȥ��Ǥ��롣RT ����ݡ��ͥ�ȤΥ��󥻥ץȤˤ����Ƥϡ�
	Port �ϥ���ݡ��ͥ�Ȥ���°��������ݡ��ͥ�Ȥ�¾�Υ���ݡ��ͥ�Ȥ���ߺ���
	��Ԥ������Ǥ��ꡢ�̾���Ĥ��Υ��󥿡��ե������ȴ�Ϣ�դ����롣
	����ݡ��ͥ�Ȥ� Port ���̤��Ƴ������Ф����󥿡��ե��������󶡤ޤ����׵�
	���뤳�Ȥ��Ǥ���Port�Ϥ�����³�������������ô����
	<p>
	Port �ζ�ݥ��饹�ϡ��̾� RT ����ݡ��ͥ�ȥ��󥹥�����������Ʊ����
	�������졢�󶡡��׵ᥤ�󥿡��ե���������Ͽ�����塢RT ����ݡ��ͥ�Ȥ�
	��Ͽ���졢�������饢��������ǽ�� Port �Ȥ��Ƶ�ǽ���뤳�Ȥ����ꤷ�Ƥ��롣
	<p>
	RTC::Port �� CORBA ���󥿡��ե������Ȥ��ưʲ��Υ��ڥ졼�������󶡤��롣

	- get_port_profile()
	- get_connector_profiles()
	- get_connector_profile()
	- connect()
	- notify_connect()
	- disconnect()
	- notify_disconnect()
	- disconnect_all()

	���Υ��饹�Ǥϡ������Υ��ڥ졼�����μ������󶡤��롣
	<p>
	�����Υ��ڥ졼�����Τ�����get_port_profile(), get_connector_profiles(),
	get_connector_profile(), connect(), disconnect(), disconnect_all() �ϡ�
	���֥��饹�ˤ������ä˿����񤤤��ѹ�����ɬ�פ��ʤ����ᡢ�����С��饤��
	���뤳�ȤϿ侩����ʤ���
	<p>
	notify_connect(), notify_disconnect() �ˤĤ��Ƥϡ����֥��饹���󶡡��׵�
	���륤�󥿡��ե������μ���˱����ơ������񤤤��ѹ�����ɬ�פ�������
	���⤷��ʤ�����������ľ�ܥ����С��饤�ɤ��뤳�ȤϿ侩���줺��
	��Ҥ� notify_connect(), notify_disconnect() �ι�ˤ����Ƥ�Ҥ٤����̤�
	�����δؿ��˴�Ϣ���� protected �ؿ��򥪡��С��饤�ɤ��뤳�Ȥˤ��
	�����񤤤��ѹ����뤳�Ȥ��侩����롣

	\else


	\endif
	"""


	def __init__(self, name=None):
		"""
		\if jp
		\brief ���󥹥ȥ饯��

		PortBase �Υ��󥹥ȥ饯���� Port ̾ name ������˼��������Ԥ�
		��Ʊ���ˡ���ʬ���Ȥ� CORBA Object �Ȥ��Ƴ������������Ȥ� PortProfile
		�� port_ref �˼��ȤΥ��֥������ȥ�ե���󥹤��Ǽ���롣

		\param name(string) Port ��̾��

		\else

		\brief Constructor

		The constructor of the ProtBase class is given the name of this Port
		and initialized. At the same time, the PortBase activates itself
		as CORBA object and stores its object reference to the PortProfile's 
		port_ref member.

		\param name(string) The name of Port 

		\endif
		"""
		self._profile = RTC.PortProfile("", [], RTC.Port._nil, [], RTC.RTObject._nil,[])
		
		if name == None:
			self._profile.name = ""
		else:
			self._profile.name = name
			
		self._objref = self._this()
		self._profile.port_ref = self._objref
		self._profile.owner = RTC.RTObject._nil
		self._profile_mutex = threading.RLock()


	def __del__(self):
		"""
		\if jp
		\brief �ǥ��ȥ饯��
		\else
		\brief Destructor
		\endif
		"""
		pass


	def get_port_profile(self):
		"""
		\if jp

		\brief [CORBA interface] PortProfile���������

		Port���ݻ�����PortProfile���֤���
		PortProfile ��¤�Τϰʲ��Υ��С�����ġ�

		- name              [string ��] Port ��̾����
		- interfaces        [PortInterfaceProfileList ��] Port ���ݻ�����
			PortInterfaceProfile �Υ�������
		- port_ref          [Port Object ��] Port ���ȤΥ��֥������ȥ�ե����
		- connector_profile [ConnectorProfileList ��] Port �������ݻ�����
			ConnectorProfile �Υ�������
		- owner             [RTObject Object ��] ���� Port ���ͭ����
			RTObject�Υ�ե����
		- properties        [NVList ��] ����¾�Υץ�ѥƥ���

		\return ���� Port �� PortProfile

		\else

		\brief [CORBA interface] Get the PortProfile of the Port

		This operation returns the PortProfile of the Port.
		PortProfile struct has the following members,

		- name              [string ] The name of the Port.
		- interfaces        [PortInterfaceProfileList ��] The sequence of 
			PortInterfaceProfile owned by the Port
		- port_ref          [Port Object] The object reference of the Port.
		- connector_profile [ConnectorProfileList ��] The sequence of 
			ConnectorProfile owned by the Port.
		- owner             [RTObject Object] The object reference of 
			RTObject that is owner of the Port.
		- properties        [NVList] The other properties.

		\return the PortProfile of the Port

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		prof = RTC.PortProfile(self._profile.name,
							   self._profile.interfaces,
							   self._profile.port_ref,
							   self._profile.connector_profiles,
							   self._profile.owner,
							   self._profile.properties)

		return prof


	def get_connector_profiles(self):
		"""
		\if jp

		\brief [CORBA interface] ConnectorProfileList���������

		Port���ݻ����� ConnectorProfile �� sequence ���֤���
		ConnectorProfile �� Port �֤���³�ץ�ե����������ݻ����빽¤�ΤǤ��ꡢ
		��³����Port�֤Ǿ���򴹤�Ԥ�����Ϣ���뤹�٤Ƥ� Port ��Ʊ����ͤ�
		�ݻ�����롣
		ConnectorProfile �ϰʲ��Υ��С����ݻ����Ƥ��롣

		- name         [string ��] ���Υ��ͥ�����̾����
		- connector_id [string ��] ��ˡ�����ID
		- ports        [Port sequnce] ���Υ��ͥ����˴�Ϣ���� Port �Υ��֥�������
			��ե���󥹤Υ������󥹡�
		- properties   [NVList ��] ����¾�Υץ�ѥƥ���

		\return ���� Port �� ConnectorProfile

		\else

		\brief [CORBA interface] Get the ConnectorProfileList of the Port

		This operation returns a list of the ConnectorProfiles of the Port.
		ConnectorProfile includes the connection information that describes 
		relation between (among) Ports, and Ports exchange the ConnectionProfile
		on connection process and hold the same information in each Port.
		ConnectionProfile has the following members,

		- name         [string] The name of the connection.
		- connector_id [string] Unique identifier.
		- ports        [Port sequnce] The sequence of Port's object reference
			that are related the connection.
		- properties   [NVList] The other properties.

		\return the ConnectorProfileList of the Port

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		return self._profile.connector_profiles


	def get_connector_profile(self, connector_id):
		"""
		\if jp

		\brief [CORBA interface] ConnectorProfile ���������

		connector_id �ǻ��ꤵ�줿 ConnectorProfile ���֤���

		\param connector_id(string) ConnectorProfile �� ID
		\return connector_id ����� ConnectorProfile

		\else

		\brief [CORBA interface] Get the ConnectorProfile

		This operation returns the ConnectorProfiles specified connector_id.

		\param connector_id(string) ID of the ConnectorProfile
		\return the ConnectorProfile identified by the connector_id

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		index = OpenRTM.CORBA_SeqUtil.find(self._profile.connector_profiles,
										   self.find_conn_id(connector_id))
		if index < 0:
			conn_prof = RTC.ConnectorProfile("","",[],[])
			return conn_prof

		conn_prof = RTC.ConnectorProfile(self._profile.connector_profiles[index].name,
										 self._profile.connector_profiles[index].connector_id,
										 self._profile.connector_profiles[index].ports,
										 self._profile.connector_profiles[index].properties)
		return conn_prof


	def connect(self, connector_profile):
		"""
		\if jp

		\brief [CORBA interface] Port ����³��Ԥ�

		Ϳ����줿 ConnectoionProfile �ˤ������äơ�Port�֤���³���Ω���롣
		���ץꥱ�������ץ����¦�ϡ����Ĥ��Υ���ݡ��ͥ�Ȥ�����ʣ����
		Port ����³��������硢Ŭ�ڤ��ͤ򥻥åȤ��� ConnectorProfile ��
		connect() �ΰ����Ȥ���Ϳ���ƥ����뤹�뤳�Ȥˤ�ꡢ��Ϣ���� Port ��
		��³���Ω���롣

		connect() ��Ϳ���� ConnectorProfile �Υ��С��Τ�����name, ports, 
		(properties) ���С����Ф��ƥǡ����򥻥åȤ��ʤ���Фʤ�ʤ���

		\param connector_profile(RTC.ConnectorProfile) ConnectorProfile
		\return ReturnCode_t ���ڥ졼�����Υ꥿���󥳡���

		\else

		\brief [CORBA interface] Connect the Port

		This operation establishes connection according to the given 
		ConnectionProfile inforamtion. 
		Application programs, which is going to establish the connection 
		among Ports owned by RT-Components, have to set valid values to the 
		ConnectorProfile and give it to the argument of connect() operation.

		name, ports, (properties) members of ConnectorProfile should be set
		valid values before giving to the argument of connect() operation.

		\param connector_profile(RTC.ConnectorProfile) The ConnectorProfile.
		\return ReturnCode_t The return code of this operation.

		\endif
		"""
		if self.isEmptyId(connector_profile):
			self.setUUID(connector_profile)
			assert(not self.isExistingConnId(connector_profile.connector_id))

		try:
			retval,connector_profile = connector_profile.ports[0].notify_connect(connector_profile)
			return (retval, connector_profile)
			#return connector_profile.ports[0].notify_connect(connector_profile)
		except:
			return (RTC.BAD_PARAMETER, connector_profile)

		return (RTC.RTC_ERROR, connector_profile)


	def notify_connect(self, connector_profile):
		"""
		\if jp

		\brief [CORBA interface] Port ����³���Τ�Ԥ�

		���Υ��ڥ졼�����ϡ�Port�֤���³���Ԥ���ݤˡ�Port�֤�����Ū��
		�ƤФ�륪�ڥ졼�����Ǥ��롣

		\param connector_profile(RTC.ConnectorProfile) ConnectorProfile
		\return ReturnCode_t ���ڥ졼�����Υ꥿���󥳡���

		\else

		\brief [CORBA interface] Notify the Ports connection

		This operation is invoked between Ports internally when the connection
		is established.

		\param connector_profile(RTC.ConnectorProfile) The ConnectorProfile.
		\return ReturnCode_t The return code of this operation.

		\endif
		"""
		# publish owned interface information to the ConnectorProfile
		retval = self.publishInterfaces(connector_profile)

		if retval != RTC.RTC_OK:
			return (retval, connector_profile)

		# call notify_connect() of the next Port
		retval, connector_profile = self.connectNext(connector_profile)
		if retval != RTC.RTC_OK:
			return (retval, connector_profile)

		# subscribe interface from the ConnectorProfile's information
		retval = self.subscribeInterfaces(connector_profile)
		if retval != RTC.RTC_OK:
			#cleanup this connection for downstream ports
			self.notify_disconnect(connector_profile.connector_id)
			return (retval, connector_profile)

		# update ConnectorProfile
		index = self.findConnProfileIndex(connector_profile.connector_id)
		if index < 0:
			OpenRTM.CORBA_SeqUtil.push_back(self._profile.connector_profiles,
											connector_profile)
		else:
			self._profile.connector_profiles[index] = connector_profile

		return (retval, connector_profile)


	def disconnect(self, connector_id):
		"""
		\if jp

		\brief [CORBA interface] Port ����³��������

		���Υ��ڥ졼��������³��Ω������³���Ф���Ϳ������ connector_id ��
		�б�����ԥ� Port �Ȥ���³�������롣

		\param connector_id(string) ConnectorProfile �� ID
		\return ReturnCode_t ���ڥ졼�����Υ꥿���󥳡���

		\else

		\brief [CORBA interface] Connect the Port

		This operation destroys connection between this port and the peer port
		according to given id that is given when the connection established.

		\param connector_id(string) The ID of the ConnectorProfile.
		\return ReturnCode_t The return code of this operation.

		\endif
		"""
		# find connector_profile
		if not self.isExistingConnId(connector_id):
			return RTC.BAD_PARAMETER

		index = self.findConnProfileIndex(connector_id)
		prof = RTC.ConnectorProfile(self._profile.connector_profiles[index].name,
									self._profile.connector_profiles[index].connector_id,
									self._profile.connector_profiles[index].ports,
									self._profile.connector_profiles[index].properties)
		return prof.ports[0].notify_disconnect(connector_id)


	def notify_disconnect(self, connector_id):
		"""
		\if jp

		\brief [CORBA interface] Port ����³������Τ�Ԥ�

		���Υ��ڥ졼�����ϡ�Port�֤���³������Ԥ���ݤˡ�Port�֤�����Ū��
		�ƤФ�륪�ڥ졼�����Ǥ��롣

		\param connector_id(string) ConnectorProfile �� ID
		\return ReturnCode_t ���ڥ졼�����Υ꥿���󥳡���

		\else

		\brief [CORBA interface] Notify the Ports disconnection

		This operation is invoked between Ports internally when the connection
		is destroied.

		\param connector_id(string) The ID of the ConnectorProfile.
		\return ReturnCode_t The return code of this operation.

		\endif
		"""

		# The Port of which the reference is stored in the beginning of
		# connectorProfile's PortList is master Port.
		# The master Port has the responsibility of disconnecting all Ports.
		# The slave Ports have only responsibility of deleting its own
		# ConnectorProfile.

		# find connector_profile
		if not self.isExistingConnId(connector_id):
			return RTC.BAD_PARAMETER

		index = self.findConnProfileIndex(connector_id)
		prof = RTC.ConnectorProfile(self._profile.connector_profiles[index].name,
									self._profile.connector_profiles[index].connector_id,
									self._profile.connector_profiles[index].ports,
									self._profile.connector_profiles[index].properties)

		self.unsubscribeInterfaces(prof)
		retval = self.disconnectNext(prof)

		OpenRTM.CORBA_SeqUtil.erase(self._profile.connector_profiles, index)
    
		return retval


	def disconnect_all(self):
		"""
		\if jp

		\brief [CORBA interface] Port ������³��������

		���Υ��ڥ졼�����Ϥ��� Port �˴�Ϣ�������Ƥ���³�������롣

		\return ReturnCode_t ���ڥ졼�����Υ꥿���󥳡���

		\else

		\brief [CORBA interface] Connect the Port

		This operation destroys all connection channels owned by the Port.

		\return ReturnCode_t The return code of this operation.

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		# disconnect all connections
		# Call disconnect() for each ConnectorProfile.
		f = OpenRTM.CORBA_SeqUtil.for_each(self._profile.connector_profiles,
										   self.disconnect_all_func(self))
		return f.return_code



	#============================================================
	# Local operations
	#============================================================

	def setName(self, name):
		"""
		\if jp
		\brief Port ��̾�������ꤹ��

		Port ��̾�������ꤹ�롣����̾���� Port ���ݻ����� PortProfile.name
		��ȿ�Ǥ���롣

		\param name(string) Port ��̾��

		\else
		\brief Set the name of this Port

		This operation sets the name of this Port. The given Port's name is
		applied to Port's PortProfile.name.

		\param name(string) The name of this Port.

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		self._profile.name = name


	def getProfile(self):
		"""
		\if jp
		\brief PortProfile���������

		Port���ݻ����� PortProfile �� const ���Ȥ��֤���

		\return ���� Port �� PortProfile

		\else
		\brief Get the PortProfile of the Port

		This operation returns const reference of the PortProfile.

		\return the PortProfile of the Port

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		return self._profile


	def setPortRef(self, port_ref):
		"""
		\if jp

		\brief Port �Υ��֥������Ȼ��Ȥ����ꤹ��

		���Υ��ڥ졼������ Port �� PortProfile �ˤ��� Port ���Ȥ�
		���֥������Ȼ��Ȥ����ꤹ�롣

		\param port_ref(RTC.Port) ���� Port �Υ��֥������Ȼ���

		\else

		\brief Set the object reference of this Port

		This operation sets the object reference itself
		to the Port's PortProfile.

		\param port_ref(RTC.Port) The object reference of this Port.

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		self._profile.port_ref = port_ref


	def getPortRef(self):
		"""
		\if jp

		\brief Port �Υ��֥������Ȼ��Ȥ��������

		���Υ��ڥ졼������ Port �� PortProfile ���ݻ����Ƥ���
		���� Port ���ȤΥ��֥������Ȼ��Ȥ�������롣

		\return ���� Port �Υ��֥������Ȼ���

		\else

		\brief Get the object reference of this Port

		This operation returns the object reference
		that is stored in the Port's PortProfile.

		\return The object reference of this Port.

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		return self._profile.port_ref


	def setOwner(self, owner):
		"""
		\if jp

		\brief Port �� owner �� RTObject ����ꤹ��

		���Υ��ڥ졼������ Port �� PortProfile.owner �����ꤹ�롣

		\param owner(RTC.RTObject) ���� Port ���ͭ���� RTObject �λ���

		\else

		\brief Set the owner RTObject of the Port

		This operation sets the owner RTObject of this Port.

		\param owner(RTC.RTObject) The owner RTObject's reference of this Port

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)
		self._profile.owner = owner


	"""
      \if jp
     
      \brief Interface ������������
     
      ���Υ��ڥ졼�����ϡ�notify_connect() �����������󥹤λϤ�˥�����
      ������貾�۴ؿ��Ǥ��롣
      notify_connect() �Ǥϡ�
     
      - publishInterfaces()
      - connectNext()
      - subscribeInterfaces()
      - updateConnectorProfile()
     
      �ν�� protected �ؿ��������뤵����³�������Ԥ��롣
      <br>
      ��� Port �ǤϤ��Υ��ڥ졼�����򥪡��С��饤�ɤ��������Ȥ���
      Ϳ����줿 ConnectorProfile �˽���������Ԥ����ѥ�᡼������Ŭ��
      �Ǥ���С�RteurnCode_t ���Υ��顼�����ɤ��֤���
      �̾� publishInterafaces() ��ˤ����Ƥϡ����� Port ��°����
      ���󥿡��ե������˴ؤ������� ConnectorProfile ���Ф���Ŭ�ڤ����ꤷ
      ¾�� Port �����Τ��ʤ���Фʤ�ʤ���
      <br>
      �ޤ������δؿ��������뤵����ʳ��Ǥϡ�¾�� Port �� Interface �˴ؤ���
      ����Ϥ��٤ƴޤޤ�Ƥ��ʤ��Τǡ�¾�� Port �� Interface ������������
      �� subscribeInterfaces() ��ǹԤ���٤��Ǥ��롣
      <br>
      ���Υ��ڥ졼�����ϡ������� connector_id ���Ф��Ƥ���³��������
      ��¸�� connector_id ���Ф��ƤϹ�����Ŭ�ڤ˹Ԥ���ɬ�פ����롣
     
      \param connector_profile ��³�˴ؤ���ץ�ե��������
      \return ReturnCode_t ���Υ꥿���󥳡���
     
      \else
     
      \brief Publish interface information
     
      This operation is pure virutal method that would be called at the
      beginning of the notify_connect() process sequence.
      In the notify_connect(), the following methods would be called in order.
     
      - publishInterfaces()
      - connectNext()
      - subscribeInterfaces()
      - updateConnectorProfile() 
     
      In the concrete Port, this method should be overridden. This method
      processes the given ConnectorProfile argument and if the given parameter
      is invalid, it would return error code of ReturnCode_t.
      Usually, publishInterfaces() method should set interfaces information
      owned by this Port, and publish it to the other Ports.
      <br>
      When this method is called, other Ports' interfaces information may not
      be completed. Therefore, the process to obtain other Port's interfaces
      information should be done in the subscribeInterfaces() method.
      <br>
      This operation should create the new connection for the new
      connector_id, and should update the connection for the existing
      connection_id.
     
      \param connector_profile The connection profile information
      \return The return code of ReturnCode_t type.
     
      \endif

	def publishInterfaces(self, connector_profile):
		pass
	"""    


	def connectNext(self, connector_profile):
		"""
		\if jp

		\brief ���� Port ���Ф��� notify_connect() �򥳡��뤹��

		ConnectorProfile �� port_ref ��˳�Ǽ����Ƥ��� Port �Υ��֥�������
		��ե���󥹤Υ������󥹤��椫�顢���Ȥ� Port �μ��� Port ���Ф���
		notify_connect() �򥳡��뤹�롣

		\param connector_profile(RTC.ConnectorProfile) ��³�˴ؤ���ץ�ե��������
		\return ReturnCode_t ���Υ꥿���󥳡���

		\else

		\brief Call notify_connect() of the next Port

		This operation calls the notify_connect() of the next Port's 
		that stored in ConnectorProfile's port_ref sequence.

		\param connector_profile(RTC.ConnectorProfile) The connection profile information
		\return The return code of ReturnCode_t type.

		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(connector_profile.ports,
										   self.find_port_ref(self._profile.port_ref))
		if index < 0:
			return RTC.BAD_PARAMETER, connector_profile

		index += 1
		if index < len(connector_profile.ports):
			p = connector_profile.ports[index]
			return p.notify_connect(connector_profile)

		return RTC.RTC_OK, connector_profile


	def disconnectNext(self, connector_profile):
		"""
		\if jp

		\brief ���� Port ���Ф��� notify_disconnect() �򥳡��뤹��

		ConnectorProfile �� port_ref ��˳�Ǽ����Ƥ��� Port �Υ��֥�������
		��ե���󥹤Υ������󥹤��椫�顢���Ȥ� Port �μ��� Port ���Ф���
		notify_disconnect() �򥳡��뤹�롣

		\param connector_profile(RTC.ConnectorProfile) ��³�˴ؤ���ץ�ե��������
		\return ReturnCode_t ���Υ꥿���󥳡���

		\else

		\brief Call notify_disconnect() of the next Port

		This operation calls the notify_disconnect() of the next Port's 
		that stored in ConnectorProfile's port_ref sequence.

		\param connector_profile(RTC.ConnectorProfile) The connection profile information
		\return The return code of ReturnCode_t type.

		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(connector_profile.ports,
										   self.find_port_ref(self._profile.port_ref))
		if index < 0:
			return RTC.BAD_PARAMETER

		index += 1
		
		if index < len(connector_profile.ports):
			p = connector_profile.ports[index]
			return p.notify_disconnect(connector_profile.connector_id)

		self.unsubscribeInterfaces(connector_profile)
		return RTC.RTC_OK


	"""
      \if jp
     
      \brief Interface ������������
     
      ���Υ��ڥ졼�����ϡ�notify_connect() �����������󥹤���֤˥�����
      ������貾�۴ؿ��Ǥ��롣
      notify_connect() �Ǥϡ�
     
      - publishInterfaces()
      - connectNext()
      - subscribeInterfaces()
      - updateConnectorProfile()
     
      �ν�� protected �ؿ��������뤵����³�������Ԥ��롣
      <br>
      ��� Port �ǤϤ��Υ��ڥ졼�����򥪡��С��饤�ɤ��������Ȥ���
      Ϳ����줿 ConnectorProfile �˽���������Ԥ����ѥ�᡼������Ŭ��
      �Ǥ���С�RteurnCode_t ���Υ��顼�����ɤ��֤���
      ���� ConnectorProfile �ˤ�¾�� Port �� Interface �˴ؤ������
      ���ƴޤޤ�Ƥ��롣
      �̾� subscribeInterafaces() ��ˤ����Ƥϡ����� Port �����Ѥ���
      Interface �˴ؤ���������������׵�¦�Υ��󥿡��ե��������Ф���
      ��������ꤷ�ʤ���Фʤ�ʤ���
      <br>
      ���Υ��ڥ졼�����ϡ������� connector_id ���Ф��Ƥ���³��������
      ��¸�� connector_id ���Ф��ƤϹ�����Ŭ�ڤ˹Ԥ���ɬ�פ����롣
     
      \param connector_profile ��³�˴ؤ���ץ�ե��������
      \return ReturnCode_t ���Υ꥿���󥳡���
     
      \else
     
      \brief Publish interface information
     
      This operation is pure virutal method that would be called at the
      mid-flow of the notify_connect() process sequence.
      In the notify_connect(), the following methods would be called in order.
     
      - publishInterfaces()
      - connectNext()
      - subscribeInterfaces()
      - updateConnectorProfile()
     
      In the concrete Port, this method should be overridden. This method
      processes the given ConnectorProfile argument and if the given parameter
      is invalid, it would return error code of ReturnCode_t.
      The given argument ConnectorProfile includes all the interfaces
      information in it.
      Usually, subscribeInterafaces() method obtains information of interfaces
      from ConnectorProfile, and should set it to the interfaces that require
      them.
      <br>
      This operation should create the new connection for the new
      connector_id, and should update the connection for the existing
      connection_id.
     
      \param connector_profile The connection profile information
      \return The return code of ReturnCode_t type.
     
      \endif

	def subscribeInterfaces(self, connector_profile):
		pass
	"""    
    
	"""
      \if jp
     
      \brief Interface ����³��������
     
      ���Υ��ڥ졼�����ϡ�notify_disconnect() �����������󥹤ν����˥�����
      ������貾�۴ؿ��Ǥ��롣
      notify_disconnect() �Ǥϡ�
      - disconnectNext()
      - unsubscribeInterfaces()
      - eraseConnectorProfile()
      �ν�� protected �ؿ��������뤵����³����������Ԥ��롣
      <br>
      ��� Port �ǤϤ��Υ��ڥ졼�����򥪡��С��饤�ɤ��������Ȥ���
      Ϳ����줿 ConnectorProfile �˽�����³���������Ԥ���
     
      \param connector_profile ��³�˴ؤ���ץ�ե��������
     
      \else
     
      \brief Disconnect interface connection
     
      This operation is pure virutal method that would be called at the
      end of the notify_disconnect() process sequence.
      In the notify_disconnect(), the following methods would be called.
      - disconnectNext()
      - unsubscribeInterfaces()
      - eraseConnectorProfile() 
       <br>
      In the concrete Port, this method should be overridden. This method
      processes the given ConnectorProfile argument and disconnect interface
      connection.
     
      \param connector_profile The connection profile information
     
      \endif

	def unsubscribeInterfaces(self, connector_profile):
		pass
	"""


	def isEmptyId(self, connector_profile):
		"""
		\if jp
		\brief ConnectorProfile �� connector_id �ե�����ɤ������ɤ���Ƚ��
		\param connector_profile(RTC.ConnectorProfile)
		\return ������Ϳ����줿 ConnectorProfile �� connector_id �����Ǥ���С�
			true�������Ǥʤ���� false ���֤���

		\else
		\brief Whether connector_id of ConnectorProfile is empty
		\param connector_profile(RTC.ConnectorProfile)
		\return If the given ConnectorProfile's connector_id is empty string,
			it returns true.
		\endif
		"""
		return connector_profile.connector_id == ""


	def getUUID(self):
		"""
		\if jp

		\brief UUID����������

		���Υ��ڥ졼������ UUID ���������롣

		\return uuid

		\else

		\brief Get the UUID

		This operation generates UUID.

		\return uuid

		\endif
		"""
		return str(OpenRTM.uuid1())


	def setUUID(self, connector_profile):
		"""
		\if jp

		\brief UUID�������� ConnectorProfile �˥��åȤ���

		���Υ��ڥ졼������ UUID ����������ConnectorProfile �˥��åȤ��롣

		\param connector_profile(RTC.ConnectorProfile) connector_id �򥻥åȤ��� ConnectorProfile

		\else

		\brief Create and set the UUID to the ConnectorProfile

		This operation generates and set UUID to the ConnectorProfile.

		\param connector_profile(RTC.ConnectorProfile) ConnectorProfile to be set connector_id

		\endif
		"""
		connector_profile.connector_id = self.getUUID()
		assert(connector_profile.connector_id != "")


	def isExistingConnId(self, id_):
		"""
		\if jp

		\brief id ����¸�� ConnectorProfile �Τ�Τ��ɤ���Ƚ�ꤹ��

		���Υ��ڥ졼������Ϳ����줿 ID ����¸�� ConnectorProfile �Υꥹ�����
		¸�ߤ��뤫�ɤ���Ƚ�ꤹ�롣

		\param id_(string) Ƚ�ꤹ�� connector_id

		\else

		\brief Whether the given id exists in stored ConnectorProfiles

		This operation returns boolean whether the given id exists in 
		the Port's ConnectorProfiles.

		\param id_(string) connector_id to be find in Port's ConnectorProfiles

		\endif
		"""
		return OpenRTM.CORBA_SeqUtil.find(self._profile.connector_profiles,
										  self.find_conn_id(id_)) >= 0


	def findConnProfile(self, id_):
		"""
		\if jp

		\brief id ����� ConnectorProfile ��õ��

		���Υ��ڥ졼������Ϳ����줿 ID ����� ConnectorProfile �� Port ��
		��� ConnectorProfile �Υꥹ���椫��õ����
		�⤷��Ʊ��� id ����� ConnectorProfile ���ʤ���С����� ConnectorProfile
		���֤���롣

		\param id_(string) �������� connector_id
		\return connector_id ����� ConnectorProfile

		\else

		\brief Find ConnectorProfile with id

		This operation returns ConnectorProfile with the given id from Port's
		ConnectorProfiles' list.
		If the ConnectorProfile with connector id that is identical with the
		given id does not exist, empty ConnectorProfile is returned.

		\param id_(string) the connector_id to be searched in Port's ConnectorProfiles
		\return CoonectorProfile with connector_id

		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._profile.connector_profiles,
										   self.find_conn_id(id_))
		if index < 0 or index >= len(self._profile.connector_profiles):
			return RTC.ConnectorProfile("","",[],[])

		return self._profile.connector_profiles[index]


	def findConnProfileIndex(self, id_):
		"""
		\if jp

		\brief id ����� ConnectorProfile ��õ��

		���Υ��ڥ졼������Ϳ����줿 ID ����� ConnectorProfile �� Port ��
		��� ConnectorProfile �Υꥹ���椫��õ������ǥå������֤���
		�⤷��Ʊ��� id ����� ConnectorProfile ���ʤ���С�-1 ���֤���

		\param id_(string) �������� connector_id
		\return Port �� ConnectorProfile �ꥹ�ȤΥ���ǥå���

		\else

		\brief Find ConnectorProfile with id

		This operation returns ConnectorProfile with the given id from Port's
		ConnectorProfiles' list.
		If the ConnectorProfile with connector id that is identical with the
		given id does not exist, empty ConnectorProfile is returned.

		\param id_(string) the connector_id to be searched in Port's ConnectorProfiles
		\return The index of ConnectorProfile of the Port

		\endif
		"""
		return OpenRTM.CORBA_SeqUtil.find(self._profile.connector_profiles,
										  self.find_conn_id(id_))


	def updateConnectorProfile(self, connector_profile):
		"""
		\if jp

		\brief ConnectorProfile ���ɲä⤷���Ϲ���

		���Υ��ڥ졼������Ϳ����줿 ConnectorProfile ��Port ���ɲä⤷����
		������¸���롣
		Ϳ����줿 ConnectorProfile �� connector_id ��Ʊ�� ID �����
		ConnectorProfile ���ꥹ�Ȥˤʤ���С��ꥹ�Ȥ��ɲä���
		Ʊ�� ID ��¸�ߤ���� ConnectorProfile ������¸���롣

		\param coonector_profile(RTC.ConnectorProfile) �ɲä⤷���Ϲ������� ConnectorProfile

		\else

		\brief Append or update the ConnectorProfile list

		This operation appends or updates ConnectorProfile of the Port
		by the given ConnectorProfile.
		If the connector_id of the given ConnectorProfile does not exist
		in the Port's ConnectorProfile list, the given ConnectorProfile would be
		append to the list. If the same id exists, the list would be updated.

		\param connector_profile(RTC.ConnectorProfile) the ConnectorProfile to be appended or updated

		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._profile.connector_profiles,
										   self.find_conn_id(connector_profile.connector_id))

		if index < 0:
			OpenRTM.CORBA_SeqUtil.push_back(self._profile.connector_profiles,
											self.connector_profile)
		else:
			self._profile.connector_profiles[index] = connector_profile


	def eraseConnectorProfile(self, id_):
		"""
		\if jp

		\brief ConnectorProfile ��������

		���Υ��ڥ졼������ Port �� PortProfile ���ݻ����Ƥ���
		ConnectorProfileList �Τ���Ϳ����줿 id ����� ConnectorProfile
		�������롣

		\param id_(string) ������� ConnectorProfile �� id

		\else

		\brief Delete the ConnectorProfile

		This operation deletes a ConnectorProfile specified by id from
		ConnectorProfileList owned by PortProfile of this Port.

		\param id_(string) The id of the ConnectorProfile to be deleted.

		\endif
		"""
		guard = ScopedLock(self._profile_mutex)

		index = OpenRTM.CORBA_SeqUtil.find(self._profile.connector_profiles,
										   self.find_conn_id(id_))

		if index < 0:
			return False

		OpenRTM.CORBA_SeqUtil.erase(self._profile.connector_profiles, index)

		return True


	def appendInterface(self, instance_name, type_name, pol):
		"""
		\if jp

		\brief PortInterfaceProfile �� ���󥿡��ե���������Ͽ����

		���Υ��ڥ졼������ Port ������ PortProfile �Ρ�PortInterfaceProfile
		�˥��󥿡��ե������ξ�����ɲä��롣
		���ξ���ϡ�get_port_profile() �ˤ�ä������� PortProfile �Τ���
		PortInterfaceProfile ���ͤ��ѹ�����ΤߤǤ��ꡢ�ºݤ˥��󥿡��ե�������
		�󶡤������׵ᤷ���ꤹ����ˤϡ����֥��饹�ǡ�publishInterface(),
		subscribeInterface() ���δؿ���Ŭ�ڤ˥����С��饤�ɤ����󥿡��ե�������
		�󶡡��׵������Ԥ�ʤ���Фʤ�ʤ���

		���󥿡��ե�����(�Υ��󥹥���)̾�� Port ��ǰ�դǤʤ���Фʤ�ʤ���
		Ʊ̾�Υ��󥿡��ե����������Ǥ���Ͽ����Ƥ����硢���δؿ��� false ��
		�֤���

		\param name(string) ���󥿡��ե������Υ��󥹥��󥹤�̾��
		\param type_name(string) ���󥿡��ե������η���̾��
		\param pol(RTC.PortInterfacePolarity) ���󥿡��ե�������°�� (RTC::PROVIDED �⤷���� RTC:REQUIRED)
		\return Ʊ̾�Υ��󥿡��ե�������������Ͽ����Ƥ���� false ���֤���

		\else

		\brief Append an interface to the PortInterfaceProfile

		This operation appends interface information to the PortInterfaceProfile
		that is owned by the Port.
		The given interfaces information only updates PortInterfaceProfile of
		PortProfile that is obtained through get_port_profile().
		In order to provide and require interfaces, proper functions (for
		example publishInterface(), subscribeInterface() and so on) should be
		overridden in subclasses, and these functions provide concrete interface
		connection and disconnection functionality.

		The interface (instance) name have to be unique in the Port.
		If the given interface name is identical with stored interface name,
		this function returns false.

		\param name(string) The instance name of the interface.
		\param type_name(string) The type name of the interface.
		\param pol(RTC.PortInterfacePolarity) The interface's polarity (RTC::PROVIDED or RTC:REQUIRED)
		\return false would be returned if the same name is already registered.

		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._profile.interfaces,
										   self.find_interface(instance_name, pol))

		if index >= 0:
			return False

		# setup PortInterfaceProfile
		prof = RTC.PortInterfaceProfile(instance_name, type_name, pol)
		OpenRTM.CORBA_SeqUtil.push_back(self._profile.interfaces, prof)

		return True


	def deleteInterface(self, name, pol):
		"""
		\if jp

		\brief PortInterfaceProfile ���饤�󥿡��ե�������Ͽ��������

		���Υ��ڥ졼������ Port ������ PortProfile �Ρ�PortInterfaceProfile
		���饤�󥿡��ե������ξ���������롣

		\param name(string) ���󥿡��ե������Υ��󥹥��󥹤�̾��
		\param pol(RTC.PortInterfacePolarity) ���󥿡��ե�������°�� (RTC::PROVIDED �⤷���� RTC:REQUIRED)
		\return ���󥿡��ե���������Ͽ����Ƥ��ʤ���� false ���֤���

		\else

		\brief Delete an interface from the PortInterfaceProfile

		This operation deletes interface information from the
		PortInterfaceProfile that is owned by the Port.

		\param name(string) The instance name of the interface.
		\param pol(RTC.PortInterfacePolarity) The interface's polarity (RTC::PROVIDED or RTC:REQUIRED)
		\return false would be returned if the given name is not registered.

		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._profile.interfaces,
										   self.find_interface(name, pol))

		if index < 0:
			return False

		OpenRTM.CORBA_SeqUtil.erase(self._profile.interfaces, index)
		return True


	def addProperty(self, key, value):
		"""
		\if jp

		\brief PortProfile �� properties �� NameValue �ͤ��ɲä���

		\param key(string) properties �� name
		\param value(data) properties �� value

		\else

		\brief Add NameValue data to PortProfile's properties

		\param key(string) The name of properties
		\param value(data) The value of properties

		\endif
		"""
		OpenRTM.CORBA_SeqUtil.push_back(self._profile.properties,
										OpenRTM.NVUtil.newNV(key, value))


	#============================================================
	# Functor
	#============================================================

	class if_name:
		"""
		\if jp
		\brief instance_name ����� PortInterfaceProfile ��õ�� Functor
		\else
		\brief A functor to find a PortInterfaceProfile named instance_name
		\endif
		"""
		def __init__(self, name):
			self._name = name

		def __call__(self, prof):
			return str(self._name) == str(prof.instance_name)
    

	class find_conn_id:
		"""
		\if jp
		\brief id ����� ConnectorProfile ��õ�� Functor
		\else
		\brief A functor to find a ConnectorProfile named id
		\endif
		"""
		def __init__(self, id_):
			"""
			 \param id_(string)
			"""
			self._id = id_

		def __call__(self, cprof):
			"""
			 \param cprof(RTC.ConnectorProfile)
			"""
			return str(self._id) == str(cprof.connector_id)


	class find_port_ref:
		"""
		\if jp
		\brief ���󥹥ȥ饯������ port_ref ��Ʊ�����֥������Ȼ��Ȥ�õ�� Functor
		\else
		\brief A functor to find the object reference that is identical port_ref
		\endif
		"""
		def __init__(self, port_ref):
			"""
			 \param port_ref(RTC.Port)
			"""
			self._port_ref = port_ref

		def __call__(self, port_ref):
			"""
			 \param port_ref(RTC.Port)
			"""
			return self._port_ref._is_equivalent(port_ref)


	class connect_func:
		"""
		\if jp
		\brief Port ����³��Ԥ� Functor
		\else
		\brief A functor to connect Ports
		\endif
		"""
		def __init__(self, p, prof):
			"""
			 \param p(RTC.Port)
			 \param prof(RTC.ConnectorProfile)
			"""
			self._port_ref = p
			self._connector_profile = prof
			self.return_code = RTC.RTC_OK

		def __call__(self, p):
			"""
			 \param p(RTC.Port)
			"""
			if not self._port_ref._is_equivalent(p):
				retval = p.notify_connect(self._connector_profile)
				if retval != RTC.RTC_OK:
					self.return_code = retval


	class disconnect_func:
		"""
		\if jp
		\brief Port ����³�����Ԥ� Functor
		\else
		\brief A functor to disconnect Ports
		\endif
		"""
		def __init__(self, p, prof):
			"""
			 \param p(RTC.Port)
			 \param prof(RTC.ConnectorProfile)
			"""
			self._port_ref = p
			self._connector_profile = prof
			self.return_code = RTC.RTC_OK
			
		def __call__(self, p):
			"""
			 \param p(RTC.Port)
			"""
			if not self._port_ref._is_equivalent(p):
				retval = p.disconnect(self._connector_profile.connector_id)
				if retval != RTC.RTC_OK:
					self.return_code = retval


	class disconnect_all_func:
		"""
		\if jp
		\brief Port ������³�����Ԥ� Functor
		\else
		\brief A functor to disconnect all Ports
		\endif
		"""
		def __init__(self, p):
			"""
			 \param p(OpenRTM.PortBase)
			"""
			self.return_code = RTC.RTC_OK
			self._port = p

		def __call__(self, p):
			"""
			 \param p(RTC.ConnectorProfile)
			"""
			retval = self._port.disconnect(p.connector_id)
			if retval != RTC.RTC_OK:
				self.return_code = retval
				
	class find_interface:
		"""
		\if jp
		\brief name �� polarity ���� interface ��õ�� Functor
		\else
		\brief A functor to find interface from name and polarity
		\endif
		"""
		def __init__(self, name, pol):
			"""
			 \param name(string)
			 \param pol(RTC.PortInterfacePolarity)
			"""
			self._name = name
			self._pol = pol

		def __call__(self, prof):
			"""
			 \param prof(RTC.PortInterfaceProfile)
			"""
			name = prof.instance_name
			return (str(self._name) == str(name)) and (self._pol == prof.polarity)
