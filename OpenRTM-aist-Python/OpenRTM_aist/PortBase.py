#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file PortBase.py
# @brief RTC's Port base class
# @date $Date: 2007/09/18 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import threading
import copy

import OpenRTM_aist
import RTC, RTC__POA



##
# @if jp
# @class PortBase
# @brief Port �δ��쥯�饹
#
# RTC::Port �δ���Ȥʤ륯�饹��
# RTC::Port �Ϥۤ� UML Port �γ�ǰ��Ѿ����Ƥ��ꡢ�ۤ�Ʊ���Τ�ΤȤߤʤ�
# ���Ȥ��Ǥ��롣RT ����ݡ��ͥ�ȤΥ��󥻥ץȤˤ����Ƥϡ�
# Port �ϥ���ݡ��ͥ�Ȥ���°��������ݡ��ͥ�Ȥ�¾�Υ���ݡ��ͥ�Ȥ���ߺ���
# ��Ԥ������Ǥ��ꡢ�̾���Ĥ��Υ��󥿡��ե������ȴ�Ϣ�դ����롣
# ����ݡ��ͥ�Ȥ� Port ���̤��Ƴ������Ф����󥿡��ե��������󶡤ޤ����׵�
# ���뤳�Ȥ��Ǥ���Port�Ϥ�����³�������������ô����
# <p>
# Port �ζ�ݥ��饹�ϡ��̾� RT ����ݡ��ͥ�ȥ��󥹥�����������Ʊ����
# �������졢�󶡡��׵ᥤ�󥿡��ե���������Ͽ�����塢RT ����ݡ��ͥ�Ȥ�
# ��Ͽ���졢�������饢��������ǽ�� Port �Ȥ��Ƶ�ǽ���뤳�Ȥ����ꤷ�Ƥ��롣
# <p>
# RTC::Port �� CORBA ���󥿡��ե������Ȥ��ưʲ��Υ��ڥ졼�������󶡤��롣
#
# - get_port_profile()
# - get_connector_profiles()
# - get_connector_profile()
# - connect()
# - notify_connect()
# - disconnect()
# - notify_disconnect()
# - disconnect_all()
#
# ���Υ��饹�Ǥϡ������Υ��ڥ졼�����μ������󶡤��롣
# <p>
# �����Υ��ڥ졼�����Τ�����get_port_profile(), get_connector_profiles(),
# get_connector_profile(), connect(), disconnect(), disconnect_all() �ϡ�
# ���֥��饹�ˤ������ä˿����񤤤��ѹ�����ɬ�פ��ʤ����ᡢ�����С��饤��
# ���뤳�ȤϿ侩����ʤ���
# <p>
# notify_connect(), notify_disconnect() �ˤĤ��Ƥϡ����֥��饹���󶡡��׵�
# ���륤�󥿡��ե������μ���˱����ơ������񤤤��ѹ�����ɬ�פ�������
# ���⤷��ʤ�����������ľ�ܥ����С��饤�ɤ��뤳�ȤϿ侩���줺��
# ��Ҥ� notify_connect(), notify_disconnect() �ι�ˤ����Ƥ�Ҥ٤����̤�
# �����δؿ��˴�Ϣ���� �ؿ��򥪡��С��饤�ɤ��뤳�Ȥˤ�꿶���񤤤��ѹ�����
# ���Ȥ��侩����롣
#
# @since 0.4.0
#
# @else
#
#
# @endif
class PortBase(RTC__POA.PortService):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # PortBase �Υ��󥹥ȥ饯���� Port ̾ name ������˼��������Ԥ�
  # ��Ʊ���ˡ���ʬ���Ȥ� CORBA Object �Ȥ��Ƴ������������Ȥ� PortProfile
  # �� port_ref �˼��ȤΥ��֥������ȥ�ե���󥹤��Ǽ���롣
  #
  # @param self
  # @param name Port ��̾��(�ǥե������:None)
  #
  # @else
  #
  # @brief Constructor
  #
  # The constructor of the ProtBase class is given the name of this Port
  # and initialized. At the same time, the PortBase activates itself
  # as CORBA object and stores its object reference to the PortProfile's 
  # port_ref member.
  #
  # @param name The name of Port 
  #
  # @endif
  def __init__(self, name=None):
    self._profile = RTC.PortProfile("", [], RTC.PortService._nil, [], RTC.RTObject._nil,[])
    
    if name is None:
      self._profile.name = ""
    else:
      self._profile.name = name
      
    self._objref = self._this()
    self._profile.port_ref = self._objref
    self._profile.owner = RTC.RTObject._nil
    self._profile_mutex = threading.RLock()
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf(name)
    self._onPublishInterfaces = None
    self._onSubscribeInterfaces = None
    self._onConnected = None
    self._onUnsubscribeInterfaces = None
    self._onDisconnected = None
    self._onConnectionLost = None


  def __del__(self):
    self._rtcout.RTC_TRACE("PortBase.__del__()")
    try:
      mgr = OpenRTM_aist.Manager.instance().getPOA()
      oid = mgr.servant_to_id(self)
      mgr.deactivate_object(oid)
    except:
      self._rtcout.RTC_WARN("Unknown exception caught.")
    

  ##
  # @if jp
  #
  # @brief [CORBA interface] PortProfile���������
  #
  # Port���ݻ�����PortProfile���֤���
  # PortProfile ��¤�Τϰʲ��Υ��С�����ġ�
  #
  # - name              [string ��] Port ��̾����
  # - interfaces        [PortInterfaceProfileList ��] Port ���ݻ�����
  #                     PortInterfaceProfile �Υ�������
  # - port_ref          [Port Object ��] Port ���ȤΥ��֥������ȥ�ե����
  # - connector_profile [ConnectorProfileList ��] Port �������ݻ�����
  #                     ConnectorProfile �Υ�������
  # - owner             [RTObject Object ��] ���� Port ���ͭ����
  #                     RTObject�Υ�ե����
  # - properties        [NVList ��] ����¾�Υץ�ѥƥ���
  #
  # @param self
  #
  # @return PortProfile
  #
  # @else
  #
  # @brief [CORBA interface] Get the PortProfile of the Port
  #
  # This operation returns the PortProfile of the Port.
  # PortProfile struct has the following members,
  #
  # - name              [string ] The name of the Port.
  # - interfaces        [PortInterfaceProfileList ��] The sequence of 
  #                     PortInterfaceProfile owned by the Port
  # - port_ref          [Port Object] The object reference of the Port.
  # - connector_profile [ConnectorProfileList ��] The sequence of 
  #                     ConnectorProfile owned by the Port.
  # - owner             [RTObject Object] The object reference of 
  #                     RTObject that is owner of the Port.
  # - properties        [NVList] The other properties.
  #
  # @return the PortProfile of the Port
  #
  # @endif
  def get_port_profile(self):
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)

    prof = RTC.PortProfile(self._profile.name,
                           self._profile.interfaces,
                           self._profile.port_ref,
                           self._profile.connector_profiles,
                           self._profile.owner,
                           self._profile.properties)

    return prof


  def getPortProfile(self):
    self._rtcout.RTC_TRACE("getPortProfile()")
    return self._profile


  ##
  # @if jp
  #
  # @brief [CORBA interface] ConnectorProfileList���������
  #
  # Port���ݻ����� ConnectorProfile �� sequence ���֤���
  # ConnectorProfile �� Port �֤���³�ץ�ե����������ݻ����빽¤�ΤǤ��ꡢ
  # ��³����Port�֤Ǿ���򴹤�Ԥ�����Ϣ���뤹�٤Ƥ� Port ��Ʊ����ͤ�
  # �ݻ�����롣
  # ConnectorProfile �ϰʲ��Υ��С����ݻ����Ƥ��롣
  #
  # - name         [string ��] ���Υ��ͥ�����̾����
  # - connector_id [string ��] ��ˡ�����ID
  # - ports        [Port sequnce] ���Υ��ͥ����˴�Ϣ���� Port �Υ��֥�������
  #                ��ե���󥹤Υ������󥹡�
  # - properties   [NVList ��] ����¾�Υץ�ѥƥ���
  #
  # @param self
  #
  # @return ���� Port ���ݻ����� ConnectorProfile
  #
  # @else
  #
  # @brief [CORBA interface] Get the ConnectorProfileList of the Port
  #
  # This operation returns a list of the ConnectorProfiles of the Port.
  # ConnectorProfile includes the connection information that describes 
  # relation between (among) Ports, and Ports exchange the ConnectionProfile
  # on connection process and hold the same information in each Port.
  # ConnectionProfile has the following members,
  #
  # - name         [string] The name of the connection.
  # - connector_id [string] Unique identifier.
  # - ports        [Port sequnce] The sequence of Port's object reference
  #                that are related the connection.
  # - properties   [NVList] The other properties.
  #
  # @return the ConnectorProfileList of the Port
  #
  # @endif
  # virtual ConnectorProfileList* get_connector_profiles()
  def get_connector_profiles(self):
    self._rtcout.RTC_TRACE("get_connector_profiles()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    return self._profile.connector_profiles


  ##
  # @if jp
  #
  # @brief [CORBA interface] ConnectorProfile ���������
  #
  # connector_id �ǻ��ꤵ�줿 ConnectorProfile ���֤���
  # ���ꤷ�� connector_id ����� ConnectorProfile ���ݻ����Ƥ��ʤ����ϡ�
  # ���� ConnectorProfile ���֤���
  #
  # @param self
  # @param connector_id ConnectorProfile �� ID
  #
  # @return connector_id �ǻ��ꤵ�줿 ConnectorProfile
  #
  # @else
  #
  # @brief [CORBA interface] Get the ConnectorProfile
  #
  # This operation returns the ConnectorProfiles specified connector_id.
  #
  # @param connector_id ID of the ConnectorProfile
  #
  # @return the ConnectorProfile identified by the connector_id
  #
  # @endif
  def get_connector_profile(self, connector_id):
    self._rtcout.RTC_TRACE("get_connector_profile(%s)", connector_id)
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                            self.find_conn_id(connector_id))
    if index < 0:
      conn_prof = RTC.ConnectorProfile("","",[],[])
      return conn_prof

    conn_prof = RTC.ConnectorProfile(self._profile.connector_profiles[index].name,
                                     self._profile.connector_profiles[index].connector_id,
                                     self._profile.connector_profiles[index].ports,
                                     self._profile.connector_profiles[index].properties)
    return conn_prof


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port ����³��Ԥ�
  #
  # Ϳ����줿 ConnectoionProfile �ξ�����ˡ�Port�֤���³���Ω���롣
  # ���ץꥱ�������ץ����¦�ϡ����Ĥ��Υ���ݡ��ͥ�Ȥ�����ʣ����
  # Port ����³��������硢Ŭ�ڤ��ͤ򥻥åȤ��� ConnectorProfile ��
  # connect() �ΰ����Ȥ���Ϳ���ƥ����뤹�뤳�Ȥˤ�ꡢ��Ϣ���� Port ��
  # ��³���Ω���롣
  #
  # connect() ��Ϳ���� ConnectorProfile �Υ��С��Τ�����name, ports, 
  # properties ���С����Ф��ƥǡ����򥻥åȤ��ʤ���Фʤ�ʤ���
  #
  # OutPort ¦�� connect() �Ǥϰʲ��Υ������󥹤ǽ������Ԥ��롣
  #
  # 1. OutPort �˴�Ϣ���� connector �������������ӥ��å�
  #
  # 2. InPort�˴�Ϣ���� connector ����μ���
  #  - ConnectorProfile::properties["dataport.corba_any.inport_ref"]��
  #    OutPortAny �Υ��֥������ȥ�ե���󥹤����ꤵ��Ƥ����硢
  #    ��ե���󥹤��������Consumer���֥������Ȥ˥��åȤ��롣
  #    ��ե���󥹤����åȤ���Ƥ��ʤ����̵�뤷�Ʒ�³��
  #    (OutPort��connect() �ƤӽФ��Υ���ȥ�ݥ���Ȥξ��ϡ�
  #    InPort�Υ��֥������ȥ�ե���󥹤ϥ��åȤ���Ƥ��ʤ��Ϥ��Ǥ��롣)
  #
  # 3. PortBase::connect() �򥳡���
  #    Port����³�δ��ܽ������Ԥ��롣
  #
  # 4. �嵭2.��InPort�Υ�ե���󥹤������Ǥ��ʤ���С�����InPort��
  #    ��Ϣ���� connector �����������롣
  #
  # 5. ConnectorProfile::properties ��Ϳ����줿���󤫤顢
  #    OutPort¦�ν����������Ԥ���
  #
  # - [dataport.interface_type]<BR>
  # -- CORBA_Any �ξ��: 
  #    InPortAny ���̤��ƥǡ����򴹤���롣
  #    ConnectorProfile::properties["dataport.corba_any.inport_ref"]��
  #    InPortAny �Υ��֥������ȥ�ե���󥹤򥻥åȤ��롣<BR>
  #
  # - [dataport.dataflow_type]<BR>
  # -- Push�ξ��: Subscriber���������롣Subscriber�Υ����פϡ�
  #    dataport.subscription_type �����ꤵ��Ƥ��롣<BR>
  # -- Pull�ξ��: InPort¦���ǡ�����Pull���Ǽ������뤿�ᡢ
  #    �ä˲��⤹��ɬ�פ�̵����
  #
  # - [dataport.subscription_type]<BR>
  # -- Once�ξ��: SubscriberOnce���������롣<BR>
  # -- New�ξ��: SubscriberNew���������롣<BR>
  # -- Periodic�ξ��: SubscriberPeriodic���������롣
  #
  # - [dataport.push_rate]<BR>
  # -- dataport.subscription_type=Periodic�ξ����������ꤹ�롣
  #
  # 6. �嵭�ν����Τ�����ĤǤ⥨�顼�Ǥ���С����顼�꥿���󤹤롣
  #    ����˽������Ԥ�줿���� RTC::RTC_OK �ǥ꥿���󤹤롣
  #  
  # @param self
  # @param connector_profile ConnectorProfile
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [CORBA interface] Connect the Port
  #
  # This operation establishes connection according to the given 
  # ConnectionProfile inforamtion. 
  # Application programs, which is going to establish the connection 
  # among Ports owned by RT-Components, have to set valid values to the 
  # ConnectorProfile and give it to the argument of connect() operation.
  # 
  # name, ports, properties members of ConnectorProfile should be set
  # valid values before giving to the argument of connect() operation.
  #
  # @param connector_profile The ConnectorProfile.
  #
  # @return ReturnCode_t The return code of this operation.
  #
  # @endif
  # virtual ReturnCode_t connect(ConnectorProfile& connector_profile)
  def connect(self, connector_profile):
    self._rtcout.RTC_TRACE("connect()")
    if self.isEmptyId(connector_profile):
      guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
      self.setUUID(connector_profile)
      assert(not self.isExistingConnId(connector_profile.connector_id))
      del guard
    else:
      guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
      if self.isExistingConnId(connector_profile.connector_id):
        self._rtcout.RTC_ERROR("Connection already exists.")
        return (RTC.PRECONDITION_NOT_MET,connector_profile)
      del guard

    try:
      retval,connector_profile = connector_profile.ports[0].notify_connect(connector_profile)
      if retval != RTC.RTC_OK:
        self._rtcout.RTC_ERROR("Connection failed. cleanup.")
        self.disconnect(connector_profile.connector_id)
    
      return (retval, connector_profile)
      #return connector_profile.ports[0].notify_connect(connector_profile)
    except:
      return (RTC.BAD_PARAMETER, connector_profile)

    return (RTC.RTC_ERROR, connector_profile)


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port ����³���Τ�Ԥ�
  #
  # ���Υ��ڥ졼�����ϡ�Port�֤���³���Ԥ���ݤˡ�Port�֤�����Ū��
  # �ƤФ�륪�ڥ졼�����Ǥ��롣
  # ConnectorProfile �ˤ���³�о� Port �Υꥹ�Ⱦ����ݻ�����Ƥ��롣Port ��
  # ConnectorProfile ���ݻ�����ȤȤ�ˡ��ꥹ����μ� Port �� notify_connect 
  # ��ƤӽФ��������ơ��ݡ��Ȥ򥳥ͥ������ɲä����塢ConnectorProfile ��
  # �ƤӤ������ Port �����ꤷ���ƤӤ��������֤������Τ褦�� ConnectorProfile
  # ����Ѥ�����³���Τ���ã����Ƥ�����
  #
  # @param self
  # @param connector_profile ConnectorProfile
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [CORBA interface] Notify the Ports connection
  #
  # This operation is invoked between Ports internally when the connection
  # is established.
  # This operation notifies this PortService of the connection between its 
  # corresponding port and the other ports and propagates the given 
  # ConnectionProfile.
  # A ConnectorProfile has a sequence of port references. This PortService 
  # stores the ConnectorProfile and invokes the notify_connect operation of 
  # the next PortService in the sequence. As ports are added to the 
  # connector, PortService references are added to the ConnectorProfile and
  # provided to the caller. In this way, notification of connection is 
  # propagated with the ConnectorProfile.
  #
  # @param connector_profile The ConnectorProfile.
  #
  # @return ReturnCode_t The return code of this operation.
  #
  # @endif
  def notify_connect(self, connector_profile):
    self._rtcout.RTC_TRACE("notify_connect()")

    # publish owned interface information to the ConnectorProfile
    retval = [RTC.RTC_OK for i in range(3)]

    retval[0] = self.publishInterfaces(connector_profile)
    if retval[0] != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("publishInterfaces() in notify_connect() failed.")

    if self._onPublishInterfaces:
      self._onPublishInterfaces(connector_profile)

    # call notify_connect() of the next Port
    retval[1], connector_profile = self.connectNext(connector_profile)
    if retval[1] != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("connectNext() in notify_connect() failed.")

    # subscribe interface from the ConnectorProfile's information
    if self._onSubscribeInterfaces:
      self._onSubscribeInterfaces(connector_profile)
    retval[2] = self.subscribeInterfaces(connector_profile)
    if retval[2] != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("subscribeInterfaces() in notify_connect() failed.")
      #self.notify_disconnect(connector_profile.connector_id)

    self._rtcout.RTC_PARANOID("%d connectors are existing",
                              len(self._profile.connector_profiles))

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    # update ConnectorProfile
    index = self.findConnProfileIndex(connector_profile.connector_id)
    if index < 0:
      OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.connector_profiles,
                                           connector_profile)
      self._rtcout.RTC_PARANOID("New connector_id. Push backed.")

    else:
      self._profile.connector_profiles[index] = connector_profile
      self._rtcout.RTC_PARANOID("Existing connector_id. Updated.")

    for ret in retval:
      if ret != RTC.RTC_OK:
        return (ret, connector_profile)

    # connection established without errors
    if self._onConnected:
      self._onConnected(connector_profile)

    return (RTC.RTC_OK, connector_profile)


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port ����³��������
  #
  # ���Υ��ڥ졼��������³��Ω������³���Ф���Ϳ������ connector_id ��
  # �б�����ԥ� Port �Ȥ���³�������롣
  # Port �� ConnectorProfile ��Υݡ��ȥꥹ�Ȥ˴ޤޤ�룱�ĤΥݡ��Ȥ�
  # notify_disconnect ��ƤӤ�������³��������Τ� notify_disconnect �ˤ�ä�
  # �¹Ԥ���롣
  #
  # @param self
  # @param connector_id ConnectorProfile �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [CORBA interface] Connect the Port
  #
  # This operation destroys connection between this port and the peer port
  # according to given id that is given when the connection established.
  # This port invokes the notify_disconnect operation of one of the ports 
  # included in the sequence of the ConnectorProfile stored when the 
  # connection was established. The notification of disconnection is 
  # propagated by the notify_disconnect operation.
  #
  # @param connector_id The ID of the ConnectorProfile.
  #
  # @return ReturnCode_t The return code of this operation.
  #
  # @endif
  # virtual ReturnCode_t disconnect(const char* connector_id)
  def disconnect(self, connector_id):
    self._rtcout.RTC_TRACE("disconnect(%s)", connector_id)

    index = self.findConnProfileIndex(connector_id)

    if index < 0:
      self._rtcout.RTC_ERROR("Invalid connector id: %s", connector_id)
      return RTC.BAD_PARAMETER

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    prof = self._profile.connector_profiles[index]
    del guard
    
    if len(prof.ports) < 1:
      self._rtcout.RTC_FATAL("ConnectorProfile has empty port list.")
      return RTC.PRECONDITION_NOT_MET

    for i in range(len(prof.ports)):
      p = prof.ports[i]
      try:
        return p.notify_disconnect(connector_id)
      except:
        self._rtcout.RTC_WARN("Unknown exception caught.")
        continue

    self._rtcout.RTC_ERROR("notify_disconnect() for all ports failed.")
    return RTC.RTC_ERROR


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port ����³������Τ�Ԥ�
  #
  # ���Υ��ڥ졼�����ϡ�Port�֤���³������Ԥ���ݤˡ�Port�֤�����Ū��
  # �ƤФ�륪�ڥ졼�����Ǥ��롣
  # ���Υ��ڥ졼�����ϡ��������� Port ����³����Ƥ���¾�� Port ����³���
  # �����Τ��롣��³����оݤ� Port ��ID�ˤ�äƻ��ꤵ��롣Port ��
  # ConnectorProfile ��Υݡ��ȥꥹ����μ� Port �� notify_disconnect ��Ƥ�
  # �Ф����ݡ��Ȥ���³����������� ConnectorProfile ���鳺������ Port ��
  # ���󤬺������롣���Τ褦�� notify_disconnect ����Ѥ�����³������Τ�
  # ��ã����Ƥ�����
  #
  # @param self
  # @param connector_id ConnectorProfile �� ID
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [CORBA interface] Notify the Ports disconnection
  #
  # This operation is invoked between Ports internally when the connection
  # is destroied.
  # This operation notifies a PortService of a disconnection between its 
  # corresponding port and the other ports. The disconnected connector is 
  # identified by the given ID, which was given when the connection was 
  # established.
  # This port invokes the notify_disconnect operation of the next PortService
  # in the sequence of the ConnectorProfile that was stored when the 
  # connection was established. As ports are disconnected, PortService 
  # references are removed from the ConnectorProfile. In this way, 
  # the notification of disconnection is propagated by the notify_disconnect
  # operation.
  #
  # @param connector_id The ID of the ConnectorProfile.
  #
  # @return ReturnCode_t The return code of this operation.
  #
  # @endif
  # virtual ReturnCode_t notify_disconnect(const char* connector_id)
  def notify_disconnect(self, connector_id):
    self._rtcout.RTC_TRACE("notify_disconnect(%s)", connector_id)

    # The Port of which the reference is stored in the beginning of
    # connectorProfile's PortServiceList is master Port.
    # The master Port has the responsibility of disconnecting all Ports.
    # The slave Ports have only responsibility of deleting its own
    # ConnectorProfile.

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)

    index = self.findConnProfileIndex(connector_id)

    if index < 0:
      self._rtcout.RTC_ERROR("Invalid connector id: %s", connector_id)
      return RTC.BAD_PARAMETER

    prof = RTC.ConnectorProfile(self._profile.connector_profiles[index].name,
                                self._profile.connector_profiles[index].connector_id,
                                self._profile.connector_profiles[index].ports,
                                self._profile.connector_profiles[index].properties)

    retval = self.disconnectNext(prof)

    if self._onUnsubscribeInterfaces:
      self._onUnsubscribeInterfaces(prof)
    self.unsubscribeInterfaces(prof)

    if self._onDisconnected:
      self._onDisconnected(prof)

    OpenRTM_aist.CORBA_SeqUtil.erase(self._profile.connector_profiles, index)
    
    return retval


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port ������³��������
  #
  # ���Υ��ڥ졼�����Ϥ��� Port �˴�Ϣ�������Ƥ���³�������롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [CORBA interface] Connect the Port
  #
  # This operation destroys all connection channels owned by the Port.
  #
  # @return ReturnCode_t The return code of this operation.
  #
  # @endif
  # virtual ReturnCode_t disconnect_all()
  def disconnect_all(self):
    self._rtcout.RTC_TRACE("disconnect_all()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    plist = copy.deepcopy(self._profile.connector_profiles)
    del guard
    
    retcode = RTC.RTC_OK
    len_ = len(plist)
    self._rtcout.RTC_DEBUG("disconnecting %d connections.", len_)

    # disconnect all connections
    # Call disconnect() for each ConnectorProfile.
    for i in range(len_):
      tmpret = self.disconnect(plist[i].connector_id)
      if tmpret != RTC.RTC_OK:
        retcode = tmpret

    return retcode


  #============================================================
  # Local operations
  #============================================================

  ##
  # @if jp
  # @brief Port ��̾�������ꤹ��
  #
  # Port ��̾�������ꤹ�롣����̾���� Port ���ݻ����� PortProfile.name
  # ��ȿ�Ǥ���롣
  #
  # @param self
  # @param name Port ��̾��
  #
  # @else
  # @brief Set the name of this Port
  #
  # This operation sets the name of this Port. The given Port's name is
  # applied to Port's PortProfile.name.
  #
  # @param name The name of this Port.
  #
  # @endif
  # void setName(const char* name);
  def setName(self, name):
    self._rtcout.RTC_TRACE("setName(%s)", name)
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    self._profile.name = name


  ##
  # @if jp
  # @brief PortProfile���������
  #
  # Port���ݻ����� PortProfile �� const ���Ȥ��֤���
  #
  # @param self
  #
  # @return ���� Port �� PortProfile
  #
  # @else
  # @brief Get the PortProfile of the Port
  #
  # This operation returns const reference of the PortProfile.
  #
  # @return the PortProfile of the Port
  #
  # @endif
  # const PortProfile& getProfile() const;
  def getProfile(self):
    self._rtcout.RTC_TRACE("getProfile()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    return self._profile


  ##
  # @if jp
  #
  # @brief Port �Υ��֥������Ȼ��Ȥ����ꤹ��
  #
  # ���Υ��ڥ졼������ Port �� PortProfile �ˤ��� Port ���Ȥ�
  # ���֥������Ȼ��Ȥ����ꤹ�롣
  #
  # @param self
  # @param port_ref ���� Port �Υ��֥������Ȼ���
  #
  # @else
  #
  # @brief Set the object reference of this Port
  #
  # This operation sets the object reference itself
  # to the Port's PortProfile.
  #
  # @param The object reference of this Port.
  #
  # @endif
  # void setPortRef(PortService_ptr port_ref);
  def setPortRef(self, port_ref):
    self._rtcout.RTC_TRACE("setPortRef()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    self._profile.port_ref = port_ref


  ##
  # @if jp
  #
  # @brief Port �Υ��֥������Ȼ��Ȥ��������
  #
  # ���Υ��ڥ졼������ Port �� PortProfile ���ݻ����Ƥ���
  # ���� Port ���ȤΥ��֥������Ȼ��Ȥ�������롣
  #
  # @param self
  #
  # @return ���� Port �Υ��֥������Ȼ���
  #
  # @else
  #
  # @brief Get the object reference of this Port
  #
  # This operation returns the object reference
  # that is stored in the Port's PortProfile.
  #
  # @return The object reference of this Port.
  #
  # @endif
  # PortService_ptr getPortRef();
  def getPortRef(self):
    self._rtcout.RTC_TRACE("getPortRef()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    return self._profile.port_ref


  ##
  # @if jp
  #
  # @brief Port �� owner �� RTObject ����ꤹ��
  #
  # ���Υ��ڥ졼������ Port �� PortProfile.owner �����ꤹ�롣
  #
  # @param self
  # @param owner ���� Port ���ͭ���� RTObject �λ���
  #
  # @else
  #
  # @brief Set the owner RTObject of the Port
  #
  # This operation sets the owner RTObject of this Port.
  #
  # @param owner The owner RTObject's reference of this Port
  #
  # @endif
  # void setOwner(RTObject_ptr owner);
  def setOwner(self, owner):
    self._rtcout.RTC_TRACE("setOwner()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    self._profile.owner = owner


  #============================================================
  # callbacks
  #============================================================

  ##
  # @if jp
  #
  # @brief ���󥿡��ե��������������ݤ˸ƤФ�륳����Хå��򥻥åȤ���
  #
  # ���Υ��ڥ졼�����ϡ����Υݡ��Ȥ���³���ˡ��ݡ��ȼ��Ȥ����ĥ���
  # �ӥ����󥿡��ե����������������륿���ߥ󥰤ǸƤФ�륳����Х�
  # ���ե��󥯥��򥻥åȤ��롣
  #
  # ������Хå��ե��󥯥��ν�ͭ���ϡ��ƤӽФ�¦�ˤ��ꡢ���֥�������
  # ��ɬ�פʤ��ʤä����˲��Τ���ΤϸƤӽФ�¦����Ǥ�Ǥ��롣
  #
  # ���Υ�����Хå��ե��󥯥��ϡ�PortBase���饹�β��۴ؿ��Ǥ���
  # publishInterfaces() ���ƤФ줿���Ȥˡ�Ʊ������ ConnectorProfile ��
  # �Ȥ�˸ƤӽФ���롣���Υ�����Хå������Ѥ��ơ�
  # publishInterfaces() ���������� ConnectorProfile ���ѹ����뤳�Ȥ���
  # ǽ�Ǥ��뤬����³�ط���������򾷤��ʤ��褦��ConnectorProfile ��
  # �ѹ��ˤ���դ��פ��롣
  #
  # @param on_publish ConnectionCallback �Υ��֥��饹���֥������ȤΥݥ���
  #
  # @else
  #
  # @brief Setting callback called on publish interfaces
  #
  # This operation sets a functor that is called after publishing
  # interfaces process when connecting between ports.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called after calling
  # publishInterfaces() that is virtual member function of the
  # PortBase class with an argument of ConnectorProfile type that
  # is same as the argument of publishInterfaces() function.
  # Although by using this functor, you can modify the ConnectorProfile
  # published by publishInterfaces() function, the modification
  # should be done carefully for fear of causing connection
  # inconsistency.
  #
  # @param on_publish a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setOnPublishInterfaces(ConnectionCallback* on_publish);
  def setOnPublishInterfaces(self, on_publish):
    self._onPublishInterfaces = on_publish
    return

  ##
  # @if jp
  #
  # @brief ���󥿡��ե��������������ݤ˸ƤФ�륳����Хå��򥻥åȤ���
  #
  # ���Υ��ڥ졼�����ϡ����Υݡ��Ȥ���³���ˡ����Υݡ��Ȥ����ĥ���
  # �ӥ����󥿡��ե����������������륿���ߥ󥰤ǸƤФ�륳����Х�
  # ���ե��󥯥��򥻥åȤ��롣
  #
  # ������Хå��ե��󥯥��ν�ͭ���ϡ��ƤӽФ�¦�ˤ��ꡢ���֥�������
  # ��ɬ�פʤ��ʤä����˲��Τ���ΤϸƤӽФ�¦����Ǥ�Ǥ��롣
  #
  # ���Υ�����Хå��ե��󥯥��ϡ�PortBase���饹�β��۴ؿ��Ǥ���
  # subscribeInterfaces() ���ƤФ�����ˡ�Ʊ������ ConnectorProfile ��
  # �Ȥ�˸ƤӽФ���롣���Υ�����Хå������Ѥ��ơ�
  # subscribeInterfaces() ��Ϳ���� ConnectorProfile ���ѹ����뤳�Ȥ���
  # ǽ�Ǥ��뤬����³�ط���������򾷤��ʤ��褦��ConnectorProfile ��
  # �ѹ��ˤ���դ��פ��롣
  #
  # @param on_subscribe ConnectionCallback �Υ��֥��饹���֥������ȤΥݥ���
  #
  # @else
  #
  # @brief Setting callback called on publish interfaces
  #
  # This operation sets a functor that is called before subscribing
  # interfaces process when connecting between ports.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called before calling
  # subscribeInterfaces() that is virtual member function of the
  # PortBase class with an argument of ConnectorProfile type that
  # is same as the argument of subscribeInterfaces() function.
  # Although by using this functor, you can modify ConnectorProfile
  # argument for subscribeInterfaces() function, the modification
  # should be done carefully for fear of causing connection
  # inconsistency.
  #
  # @param on_subscribe a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  #void setOnSubscribeInterfaces(ConnectionCallback* on_subscribe);
  def setOnSubscribeInterfaces(self, on_subscribe):
    self._onSubscribeInterfaces = on_subscribe
    return


  ##
  # @if jp
  #
  # @brief ��³��λ���˸ƤФ�륳����Хå��򥻥åȤ���
  #
  # ���Υ��ڥ졼�����ϡ����Υݡ��Ȥ���³��λ���˸ƤФ�롢������Х�
  # ���ե��󥯥��򥻥åȤ��롣
  #
  # ������Хå��ե��󥯥��ν�ͭ���ϡ��ƤӽФ�¦�ˤ��ꡢ���֥�������
  # ��ɬ�פʤ��ʤä����˲��Τ���ΤϸƤӽФ�¦����Ǥ�Ǥ��롣
  #
  # ���Υ�����Хå��ե��󥯥��ϡ��ݡ��Ȥ���³�¹Դؿ��Ǥ���
  # notify_connect() �ν�λľ���ˡ���³���������ｪλ����ݤ˸¤ä�
  # �ƤӽФ���륳����Хå��Ǥ��롣��³�����β����ǥ��顼��ȯ������
  # ���ˤϸƤӽФ���ʤ���
  # 
  # ���Υ�����Хå��ե��󥯥��� notify_connect() �� out �ѥ�᡼��
  # �Ȥ����֤��Τ�Ʊ������ ConnectorProfile �ȤȤ�˸ƤӽФ����Τǡ�
  # ������³�ˤ����Ƹ������줿���٤ƤΥ��󥿡��ե�������������뤳��
  # ���Ǥ��롣���Υ�����Хå������Ѥ��ơ�notify_connect() ���֤�
  # ConnectorProfile ���ѹ����뤳�Ȥ���ǽ�Ǥ��뤬����³�ط���������
  # �򾷤��ʤ��褦��ConnectorProfile ���ѹ��ˤ���դ��פ��롣
  #
  # @param on_subscribe ConnectionCallback �Υ��֥��饹���֥������ȤΥݥ���
  #
  # @else
  #
  # @brief Setting callback called on connection established
  #
  # This operation sets a functor that is called when connection
  # between ports established.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called only when notify_connect()
  # function successfully returns. In case of error, the functor
  # will not be called.
  #
  # Since this functor is called with ConnectorProfile argument
  # that is same as out-parameter of notify_connect() function, you
  # can get all the information of published interfaces of related
  # ports in the connection.  Although by using this functor, you
  # can modify ConnectorProfile argument for out-paramter of
  # notify_connect(), the modification should be done carefully for
  # fear of causing connection inconsistency.
  #
  # @param on_subscribe a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setOnConnected(ConnectionCallback* on_connected);
  def setOnConnected(self, on_connected):
    self._onConnected = on_connected
    return


  ##
  # @if jp
  #
  # @brief ���󥿡��ե��������������ݤ˸ƤФ�륳����Хå��򥻥åȤ���
  #
  # ���Υ��ڥ졼�����ϡ����Υݡ��Ȥ���³���ˡ����Υݡ��Ȥ����ĥ���
  # �ӥ����󥿡��ե����������������륿���ߥ󥰤ǸƤФ�륳����Х�
  # ���ե��󥯥��򥻥åȤ��롣
  #
  # ������Хå��ե��󥯥��ν�ͭ���ϡ��ƤӽФ�¦�ˤ��ꡢ���֥�������
  # ��ɬ�פʤ��ʤä����˲��Τ���ΤϸƤӽФ�¦����Ǥ�Ǥ��롣
  #
  # ���Υ�����Хå��ե��󥯥��ϡ�PortBase���饹�β��۴ؿ��Ǥ���
  # unsubscribeInterfaces() ���ƤФ�����ˡ�Ʊ������ ConnectorProfile ��
  # �Ȥ�˸ƤӽФ���롣���Υ�����Хå������Ѥ��ơ�
  # unsubscribeInterfaces() ��Ϳ���� ConnectorProfile ���ѹ����뤳�Ȥ���
  # ǽ�Ǥ��뤬����³�ط���������򾷤��ʤ��褦��ConnectorProfile ��
  # �ѹ��ˤ���դ��פ��롣
  #
  # @param on_unsubscribe ConnectionCallback �Υ��֥��饹���֥�����
  # �ȤΥݥ���
  #
  # @else
  #
  # @brief Setting callback called on unsubscribe interfaces
  #
  # This operation sets a functor that is called before unsubscribing
  # interfaces process when disconnecting between ports.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called before calling
  # unsubscribeInterfaces() that is virtual member function of the
  # PortBase class with an argument of ConnectorProfile type that
  # is same as the argument of unsubscribeInterfaces() function.
  # Although by using this functor, you can modify ConnectorProfile
  # argument for unsubscribeInterfaces() function, the modification
  # should be done carefully for fear of causing connection
  # inconsistency.
  #
  # @param on_unsubscribe a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setOnUnsubscribeInterfaces(ConnectionCallback* on_subscribe);
  def setOnUnsubscribeInterfaces(self, on_subscribe):
    self._onUnsubscribeInterfaces = on_unsubscribe
    return


  ##
  # @if jp
  #
  # @brief ��³����˸ƤФ�륳����Хå��򥻥åȤ���
  #
  # ���Υ��ڥ졼�����ϡ����Υݡ��Ȥ���³������˸ƤФ�롢������Х�
  # ���ե��󥯥��򥻥åȤ��롣
  #
  # ������Хå��ե��󥯥��ν�ͭ���ϡ��ƤӽФ�¦�ˤ��ꡢ���֥�������
  # ��ɬ�פʤ��ʤä����˲��Τ���ΤϸƤӽФ�¦����Ǥ�Ǥ��롣
  #
  # ���Υ�����Хå��ե��󥯥��ϡ��ݡ��Ȥ���³����¹Դؿ��Ǥ���
  # notify_disconnect() �ν�λľ���ˡ��ƤӽФ���륳����Хå��Ǥ��롣
  # 
  # ���Υ�����Хå��ե��󥯥�����³���б����� ConnectorProfile �Ȥ�
  # ��˸ƤӽФ���롣���� ConnectorProfile �Ϥ��Υե��󥯥��ƽФ���
  # ���˴������Τǡ��ѹ����ۤ��˱ƶ���Ϳ���뤳�ȤϤʤ���
  #
  # @param on_disconnected ConnectionCallback �Υ��֥��饹���֥�����
  # �ȤΥݥ���
  #
  # @else
  #
  # @brief Setting callback called on disconnected
  #
  # This operation sets a functor that is called when connection
  # between ports is destructed.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called just before notify_disconnect()
  # that is disconnection execution function returns.
  #
  # This functor is called with argument of corresponding
  # ConnectorProfile.  Since this ConnectorProfile will be
  # destructed after calling this functor, modifications never
  # affect others.
  #
  # @param on_disconnected a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setOnDisconnected(ConnectionCallback* on_disconnected);
  def setOnDisconnected(self, on_disconnected):
    self._onDisconnected = on_disconnected
    return

  # void setOnConnectionLost(ConnectionCallback* on_connection_lost);
  def setOnConnectionLost(self, on_connection_lost):
    self._onConnectionLost = on_connection_lost
    return

  ##
  # @if jp
  #
  # @brief Interface ������������(���֥��饹������)
  #
  # ���Υ��ڥ졼�����ϡ�notify_connect() �����������󥹤λϤ�˥�����
  # �����ؿ��Ǥ��롣
  # notify_connect() �Ǥϡ�
  #
  # - publishInterfaces()
  # - connectNext()
  # - subscribeInterfaces()
  # - updateConnectorProfile()
  #
  # �ν�� protected �ؿ��������뤵����³�������Ԥ��롣
  # <br>
  # ��� Port �ǤϤ��Υ��ڥ졼�����򥪡��С��饤�ɤ��������Ȥ���
  # Ϳ����줿 ConnectorProfile �˽���������Ԥ����ѥ�᡼������Ŭ��
  # �Ǥ���С�RteurnCode_t ���Υ��顼�����ɤ��֤���
  # �̾� publishInterafaces() ��ˤ����Ƥϡ����� Port ��°����
  # ���󥿡��ե������˴ؤ������� ConnectorProfile ���Ф���Ŭ�ڤ����ꤷ
  # ¾�� Port �����Τ��ʤ���Фʤ�ʤ���
  # <br>
  # �ޤ������δؿ��������뤵����ʳ��Ǥϡ�¾�� Port �� Interface �˴ؤ���
  # ����Ϥ��٤ƴޤޤ�Ƥ��ʤ��Τǡ�¾�� Port �� Interface ������������
  # �� subscribeInterfaces() ��ǹԤ���٤��Ǥ��롣
  # <br>
  # ���Υ��ڥ졼�����ϡ������� connector_id ���Ф��Ƥ���³��������
  # ��¸�� connector_id ���Ф��ƤϹ�����Ŭ�ڤ˹Ԥ���ɬ�פ����롣<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Publish interface information
  #
  # This operation is pure virutal method that would be called at the
  # beginning of the notify_connect() process sequence.
  # In the notify_connect(), the following methods would be called in order.
  #
  # - publishInterfaces()
  # - connectNext()
  # - subscribeInterfaces()
  # - updateConnectorProfile() 
  #
  # In the concrete Port, this method should be overridden. This method
  # processes the given ConnectorProfile argument and if the given parameter
  # is invalid, it would return error code of ReturnCode_t.
  # Usually, publishInterfaces() method should set interfaces information
  # owned by this Port, and publish it to the other Ports.
  # <br>
  # When this method is called, other Ports' interfaces information may not
  # be completed. Therefore, the process to obtain other Port's interfaces
  # information should be done in the subscribeInterfaces() method.
  # <br>
  # This operation should create the new connection for the new
  # connector_id, and should update the connection for the existing
  # connection_id.
  #
  # @param connector_profile The connection profile information
  # @return The return code of ReturnCode_t type.
  #
  #@endif
  def publishInterfaces(self, connector_profile):
    pass


  ##
  # @if jp
  #
  # @brief ���� Port ���Ф��� notify_connect() �򥳡��뤹��
  #
  # ConnectorProfile �� port_ref ��˳�Ǽ����Ƥ��� Port �Υ��֥�������
  # ��ե���󥹤Υ������󥹤��椫�顢���Ȥ� Port �μ��� Port ���Ф���
  # notify_connect() �򥳡��뤹�롣
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Call notify_connect() of the next Port
  #
  # This operation calls the notify_connect() of the next Port's 
  # that stored in ConnectorProfile's port_ref sequence.
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  # @endif
  # virtual ReturnCode_t connectNext(ConnectorProfile& connector_profile);
  def connectNext(self, connector_profile):
    index = OpenRTM_aist.CORBA_SeqUtil.find(connector_profile.ports,
                                            self.find_port_ref(self._profile.port_ref))
    if index < 0:
      return RTC.BAD_PARAMETER, connector_profile

    index += 1
    if index < len(connector_profile.ports):
      p = connector_profile.ports[index]
      return p.notify_connect(connector_profile)

    return (RTC.RTC_OK, connector_profile)


  ##
  # @if jp
  #
  # @brief ���� Port ���Ф��� notify_disconnect() �򥳡��뤹��
  #
  # ConnectorProfile �� port_ref ��˳�Ǽ����Ƥ��� Port �Υ��֥�������
  # ��ե���󥹤Υ������󥹤��椫�顢���Ȥ� Port �μ��� Port ���Ф���
  # notify_disconnect() �򥳡��뤹�롣
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Call notify_disconnect() of the next Port
  #
  # This operation calls the notify_disconnect() of the next Port's 
  # that stored in ConnectorProfile's port_ref sequence.
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  # @endif
  # virtual ReturnCode_t disconnectNext(ConnectorProfile& connector_profile);
  def disconnectNext(self, connector_profile):
    index = OpenRTM_aist.CORBA_SeqUtil.find(connector_profile.ports,
                                            self.find_port_ref(self._profile.port_ref))
    if index < 0:
      return RTC.BAD_PARAMETER

    index += 1

    while index < len(connector_profile.ports):
      p = connector_profile.ports[index]
      index += 1
      try:
        return p.notify_disconnect(connector_profile.connector_id)
      except:
        self._rtcout.RTC_WARN("Unknown exception caught.")
        continue

    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief Interface ������������(���֥��饹������)
  #
  # ���Υ��ڥ졼�����ϡ�notify_connect() �����������󥹤���֤˥�����
  # �����ؿ��Ǥ��롣
  # notify_connect() �Ǥϡ�
  #
  #  - publishInterfaces()
  #  - connectNext()
  #  - subscribeInterfaces()
  #  - updateConnectorProfile()
  #
  # �ν�� protected �ؿ��������뤵����³�������Ԥ��롣
  # <br>
  # ��� Port �ǤϤ��Υ��ڥ졼�����򥪡��С��饤�ɤ��������Ȥ���
  # Ϳ����줿 ConnectorProfile �˽���������Ԥ����ѥ�᡼������Ŭ��
  # �Ǥ���С�RteurnCode_t ���Υ��顼�����ɤ��֤���
  # ���� ConnectorProfile �ˤ�¾�� Port �� Interface �˴ؤ������
  # ���ƴޤޤ�Ƥ��롣
  # �̾� subscribeInterafaces() ��ˤ����Ƥϡ����� Port �����Ѥ���
  # Interface �˴ؤ���������������׵�¦�Υ��󥿡��ե��������Ф���
  # ��������ꤷ�ʤ���Фʤ�ʤ���
  # <br>
  # ���Υ��ڥ졼�����ϡ������� connector_id ���Ф��Ƥ���³��������
  # ��¸�� connector_id ���Ф��ƤϹ�����Ŭ�ڤ˹Ԥ���ɬ�פ����롣<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Publish interface information
  #
  # This operation is pure virutal method that would be called at the
  # mid-flow of the notify_connect() process sequence.
  # In the notify_connect(), the following methods would be called in order.
  #
  #  - publishInterfaces()
  #  - connectNext()
  #  - subscribeInterfaces()
  #  - updateConnectorProfile()
  #
  # In the concrete Port, this method should be overridden. This method
  # processes the given ConnectorProfile argument and if the given parameter
  # is invalid, it would return error code of ReturnCode_t.
  # The given argument ConnectorProfile includes all the interfaces
  # information in it.
  # Usually, subscribeInterafaces() method obtains information of interfaces
  # from ConnectorProfile, and should set it to the interfaces that require
  # them.
  # <br>
  # This operation should create the new connection for the new
  # connector_id, and should update the connection for the existing
  # connection_id.
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  #@endif
  def subscribeInterfaces(self, connector_profile):
    pass


  ##
  # @if jp
  #
  # @brief Interface ����³��������(���֥��饹������)
  #
  # ���Υ��ڥ졼�����ϡ�notify_disconnect() �����������󥹤ν����˥�����
  # �����ؿ��Ǥ��롣
  # notify_disconnect() �Ǥϡ�
  #  - disconnectNext()
  #  - unsubscribeInterfaces()
  #  - eraseConnectorProfile()
  # �ν�� protected �ؿ��������뤵����³����������Ԥ��롣
  # <br>
  # ��� Port �ǤϤ��Υ��ڥ졼�����򥪡��С��饤�ɤ��������Ȥ���
  # Ϳ����줿 ConnectorProfile �˽�����³���������Ԥ���<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @else
  #
  # @brief Disconnect interface connection
  #
  # This operation is pure virutal method that would be called at the
  # end of the notify_disconnect() process sequence.
  # In the notify_disconnect(), the following methods would be called.
  #  - disconnectNext()
  #  - unsubscribeInterfaces()
  #  - eraseConnectorProfile() 
  # <br>
  # In the concrete Port, this method should be overridden. This method
  # processes the given ConnectorProfile argument and disconnect interface
  # connection.
  #
  # @param connector_profile The connection profile information
  #
  # @endif
  def unsubscribeInterfaces(self, connector_profile):
    pass


  ##
  # @if jp
  #
  # @brief ConnectorProfile �� connector_id �ե�����ɤ������ɤ���Ƚ��
  #
  # ���ꤵ�줿 ConnectorProfile �� connector_id �����Ǥ��뤫�ɤ�����Ƚ���
  # �Ԥ���
  #
  # @param self
  # @param connector_profile Ƚ���оݥ��ͥ����ץ�ե�����
  #
  # @return ������Ϳ����줿 ConnectorProfile �� connector_id �����Ǥ���С�
  #         true�������Ǥʤ���� false ���֤���
  #
  # @else
  #
  # @brief Whether connector_id of ConnectorProfile is empty
  #
  # @return If the given ConnectorProfile's connector_id is empty string,
  #         it returns true.
  #
  # @endif
  # bool isEmptyId(const ConnectorProfile& connector_profile) const;
  def isEmptyId(self, connector_profile):
    return connector_profile.connector_id == ""


  ##
  # @if jp
  #
  # @brief UUID����������
  #
  # ���Υ��ڥ졼������ UUID ���������롣
  #
  # @param self
  #
  # @return uuid
  #
  # @else
  #
  # @brief Get the UUID
  #
  # This operation generates UUID.
  #
  # @return uuid
  #
  # @endif
  # const std::string getUUID() const;
  def getUUID(self):
    return str(OpenRTM_aist.uuid1())


  ##
  # @if jp
  #
  # @brief UUID�������� ConnectorProfile �˥��åȤ���
  #
  # ���Υ��ڥ졼������ UUID ����������ConnectorProfile �˥��åȤ��롣
  #
  # @param self
  # @param connector_profile connector_id �򥻥åȤ��� ConnectorProfile
  #
  # @else
  #
  # @brief Create and set the UUID to the ConnectorProfile
  #
  # This operation generates and set UUID to the ConnectorProfile.
  #
  # @param connector_profile ConnectorProfile to be set connector_id
  #
  # @endif
  # void setUUID(ConnectorProfile& connector_profile) const;
  def setUUID(self, connector_profile):
    connector_profile.connector_id = self.getUUID()
    assert(connector_profile.connector_id != "")


  ##
  # @if jp
  #
  # @brief id ����¸�� ConnectorProfile �Τ�Τ��ɤ���Ƚ�ꤹ��
  #
  # ���Υ��ڥ졼������Ϳ����줿 ID ����¸�� ConnectorProfile �Υꥹ�����
  # ¸�ߤ��뤫�ɤ���Ƚ�ꤹ�롣
  #
  # @param self
  # @param id_ Ƚ�ꤹ�� connector_id
  #
  # @return id ��¸��Ƚ����
  #
  # @else
  #
  # @brief Whether the given id exists in stored ConnectorProfiles
  #
  # This operation returns boolean whether the given id exists in 
  # the Port's ConnectorProfiles.
  #
  # @param id connector_id to be find in Port's ConnectorProfiles
  #
  # @endif
  # bool isExistingConnId(const char* id);
  def isExistingConnId(self, id_):
    return OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                           self.find_conn_id(id_)) >= 0


  ##
  # @if jp
  #
  # @brief id ����� ConnectorProfile ��õ��
  #
  # ���Υ��ڥ졼������Ϳ����줿 ID ����� ConnectorProfile �� Port ��
  # ��� ConnectorProfile �Υꥹ���椫��õ����
  # �⤷��Ʊ��� id ����� ConnectorProfile ���ʤ���С����� ConnectorProfile
  # ���֤���롣
  #
  # @param self
  # @param id_ �������� connector_id
  #
  # @return connector_id ����� ConnectorProfile
  #
  # @else
  #
  # @brief Find ConnectorProfile with id
  #
  # This operation returns ConnectorProfile with the given id from Port's
  # ConnectorProfiles' list.
  # If the ConnectorProfile with connector id that is identical with the
  # given id does not exist, empty ConnectorProfile is returned.
  #
  # @param id the connector_id to be searched in Port's ConnectorProfiles
  #
  # @return CoonectorProfile with connector_id
  #
  # @endif
  # ConnectorProfile findConnProfile(const char* id);
  def findConnProfile(self, id_):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                            self.find_conn_id(id_))
    if index < 0 or index >= len(self._profile.connector_profiles):
      return RTC.ConnectorProfile("","",[],[])

    return self._profile.connector_profiles[index]


  ##
  # @if jp
  #
  # @brief id ����� ConnectorProfile ��õ��
  #
  # ���Υ��ڥ졼������Ϳ����줿 ID ����� ConnectorProfile �� Port ��
  # ��� ConnectorProfile �Υꥹ���椫��õ������ǥå������֤���
  # �⤷��Ʊ��� id ����� ConnectorProfile ���ʤ���С�-1 ���֤���
  #
  # @param self
  # @param id_ �������� connector_id
  #
  # @return Port �� ConnectorProfile �ꥹ�ȤΥ���ǥå���
  #
  # @else
  #
  # @brief Find ConnectorProfile with id
  #
  # This operation returns ConnectorProfile with the given id from Port's
  # ConnectorProfiles' list.
  # If the ConnectorProfile with connector id that is identical with the
  # given id does not exist, empty ConnectorProfile is returned.
  #
  # @param id the connector_id to be searched in Port's ConnectorProfiles
  #
  # @return The index of ConnectorProfile of the Port
  #
  # @endif
  # CORBA::Long findConnProfileIndex(const char* id);
  def findConnProfileIndex(self, id_):
    return OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                           self.find_conn_id(id_))


  ##
  # @if jp
  #
  # @brief ConnectorProfile ���ɲä⤷���Ϲ���
  #
  # ���Υ��ڥ졼������Ϳ����줿Ϳ����줿 ConnectorProfile ��
  # Port ���ɲä⤷���Ϲ�����¸���롣
  # Ϳ����줿 ConnectorProfile �� connector_id ��Ʊ�� ID �����
  # ConnectorProfile ���ꥹ�Ȥˤʤ���С��ꥹ�Ȥ��ɲä���
  # Ʊ�� ID ��¸�ߤ���� ConnectorProfile ������¸���롣
  #
  # @param self
  # @param connector_profile �ɲä⤷���Ϲ������� ConnectorProfile
  #
  # @else
  #
  # @brief Append or update the ConnectorProfile list
  #
  # This operation appends or updates ConnectorProfile of the Port
  # by the given ConnectorProfile.
  # If the connector_id of the given ConnectorProfile does not exist
  # in the Port's ConnectorProfile list, the given ConnectorProfile would be
  # append to the list. If the same id exists, the list would be updated.
  #
  # @param connector_profile the ConnectorProfile to be appended or updated
  #
  # @endif
  # void updateConnectorProfile(const ConnectorProfile& connector_profile);
  def updateConnectorProfile(self, connector_profile):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                            self.find_conn_id(connector_profile.connector_id))

    if index < 0:
      OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.connector_profiles,
                                           connector_profile)
    else:
      self._profile.connector_profiles[index] = connector_profile


  ##
  # @if jp
  #
  # @brief ConnectorProfile ��������
  #
  # ���Υ��ڥ졼������ Port �� PortProfile ���ݻ����Ƥ���
  # ConnectorProfileList �Τ���Ϳ����줿 id ����� ConnectorProfile
  # �������롣
  #
  # @param self
  # @param id_ ������� ConnectorProfile �� id
  #
  # @return ����˺���Ǥ������� true��
  #         ���ꤷ�� ConnectorProfile �����Ĥ���ʤ����� false ���֤�
  #
  # @else
  #
  # @brief Delete the ConnectorProfile
  #
  # This operation deletes a ConnectorProfile specified by id from
  # ConnectorProfileList owned by PortProfile of this Port.
  #
  # @param id The id of the ConnectorProfile to be deleted.
  #
  # @endif
  # bool eraseConnectorProfile(const char* id);
  def eraseConnectorProfile(self, id_):
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)

    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                            self.find_conn_id(id_))

    if index < 0:
      return False

    OpenRTM_aist.CORBA_SeqUtil.erase(self._profile.connector_profiles, index)

    return True


  ##
  # @if jp
  #
  # @brief PortInterfaceProfile �� ���󥿡��ե���������Ͽ����
  #
  # ���Υ��ڥ졼������ Port ������ PortProfile �Ρ�PortInterfaceProfile
  # �˥��󥿡��ե������ξ�����ɲä��롣
  # ���ξ���ϡ�get_port_profile() ����ä������� PortProfile �Τ���
  # PortInterfaceProfile ���ͤ��ѹ�����ΤߤǤ��ꡢ�ºݤ˥��󥿡��ե�������
  # �󶡤������׵ᤷ���ꤹ����ˤϡ����֥��饹�ǡ� publishInterface() ,
  #  subscribeInterface() ���δؿ���Ŭ�ڤ˥����С��饤�ɤ����󥿡��ե�������
  # �󶡡��׵������Ԥ�ʤ���Фʤ�ʤ���
  #
  # ���󥿡��ե�����(�Υ��󥹥���)̾�� Port ��ǰ�դǤʤ���Фʤ�ʤ���
  # Ʊ̾�Υ��󥿡��ե����������Ǥ���Ͽ����Ƥ����硢���δؿ��� false ��
  # �֤���
  #
  # @param self
  # @param instance_name ���󥿡��ե������Υ��󥹥��󥹤�̾��
  # @param type_name ���󥿡��ե������η���̾��
  # @param pol ���󥿡��ե�������°�� (RTC::PROVIDED �⤷���� RTC:REQUIRED)
  #
  # @return ���󥿡��ե�������Ͽ������̡�
  #         Ʊ̾�Υ��󥿡��ե�������������Ͽ����Ƥ���� false ���֤���
  #
  # @else
  #
  # @brief Append an interface to the PortInterfaceProfile
  #
  # This operation appends interface information to the PortInterfaceProfile
  # that is owned by the Port.
  # The given interfaces information only updates PortInterfaceProfile of
  # PortProfile that is obtained through get_port_profile().
  # In order to provide and require interfaces, proper functions (for
  # example publishInterface(), subscribeInterface() and so on) should be
  # overridden in subclasses, and these functions provide concrete interface
  # connection and disconnection functionality.
  #
  # The interface (instance) name have to be unique in the Port.
  # If the given interface name is identical with stored interface name,
  # this function returns false.
  #
  # @param name The instance name of the interface.
  # @param type_name The type name of the interface.
  # @param pol The interface's polarity (RTC::PROVIDED or RTC:REQUIRED)
  #
  # @return false would be returned if the same name is already registered.
  #
  # @endif
  # bool appendInterface(const char* name, const char* type_name,
  #			 PortInterfacePolarity pol);
  def appendInterface(self, instance_name, type_name, pol):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.interfaces,
                                            self.find_interface(instance_name, pol))

    if index >= 0:
      return False

    # setup PortInterfaceProfile
    prof = RTC.PortInterfaceProfile(instance_name, type_name, pol)
    OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.interfaces, prof)

    return True


  ##
  # @if jp
  #
  # @brief PortInterfaceProfile ���饤�󥿡��ե�������Ͽ��������
  #
  # ���Υ��ڥ졼������ Port ������ PortProfile �Ρ�PortInterfaceProfile
  # ���饤�󥿡��ե������ξ���������롣
  #
  # @param self
  # @param name ���󥿡��ե������Υ��󥹥��󥹤�̾��
  # @param pol ���󥿡��ե�������°�� (RTC::PROVIDED �⤷���� RTC:REQUIRED)
  #
  # @return ���󥿡��ե��������������̡�
  #         ���󥿡��ե���������Ͽ����Ƥ��ʤ���� false ���֤���
  #
  # @else
  #
  # @brief Delete an interface from the PortInterfaceProfile
  #
  # This operation deletes interface information from the
  # PortInterfaceProfile that is owned by the Port.
  #
  # @param name The instance name of the interface.
  # @param pol The interface's polarity (RTC::PROVIDED or RTC:REQUIRED)
  #
  # @return false would be returned if the given name is not registered.
  #
  # @endif
  # bool deleteInterface(const char* name, PortInterfacePolarity pol);
  def deleteInterface(self, name, pol):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.interfaces,
                                            self.find_interface(name, pol))

    if index < 0:
      return False

    OpenRTM_aist.CORBA_SeqUtil.erase(self._profile.interfaces, index)
    return True


  ##
  # @if jp
  #
  # @brief PortProfile �� properties �� NameValue �ͤ��ɲä���
  #
  # PortProfile �� properties �� NameValue �ͤ��ɲä��롣
  # �ɲä���ǡ����η���ValueType�ǻ��ꤹ�롣
  #
  # @param self
  # @param key properties �� name
  # @param value properties �� value
  #
  # @else
  #
  # @brief Add NameValue data to PortProfile's properties
  #
  # @param key The name of properties
  # @param value The value of properties
  #
  # @endif
  #  template <class ValueType>
  #  void addProperty(const char* key, ValueType value)
  def addProperty(self, key, value):
    OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.properties,
                                         OpenRTM_aist.NVUtil.newNV(key, value))

  # void appendProperty(const char* key, const char* value)
  def appendProperty(self, key, value):
    OpenRTM_aist.NVUtil.appendStringValue(self._profile.properties, key, value)


  #============================================================
  # Functor
  #============================================================

  ##
  # @if jp
  # @class if_name
  # @brief instance_name ����� PortInterfaceProfile ��õ�� Functor
  # @else
  # @brief A functor to find a PortInterfaceProfile named instance_name
  # @endif
  class if_name:
    def __init__(self, name):
      self._name = name

    def __call__(self, prof):
      return str(self._name) == str(prof.instance_name)
    

  ##
  # @if jp
  # @class find_conn_id
  # @brief id ����� ConnectorProfile ��õ�� Functor
  # @else
  # @brief A functor to find a ConnectorProfile named id
  # @endif
  class find_conn_id:
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

  ##
  # @if jp
  # @class find_port_ref
  # @brief ���󥹥ȥ饯������ port_ref ��Ʊ�����֥������Ȼ��Ȥ�õ�� Functor
  # @else
  # @brief A functor to find the object reference that is identical port_ref
  # @endif
  class find_port_ref:
    def __init__(self, port_ref):
      """
       \param port_ref(RTC.PortService)
      """
      self._port_ref = port_ref

    def __call__(self, port_ref):
      """
       \param port_ref(RTC.PortService)
      """
      return self._port_ref._is_equivalent(port_ref)

  ##
  # @if jp
  # @class connect_func
  # @brief Port ����³��Ԥ� Functor
  # @else
  # @brief A functor to connect Ports
  # @endif
  class connect_func:
    def __init__(self, p, prof):
      """
       \param p(RTC.PortService)
       \param prof(RTC.ConnectorProfile)
      """
      self._port_ref = p
      self._connector_profile = prof
      self.return_code = RTC.RTC_OK

    def __call__(self, p):
      """
       \param p(RTC.PortService)
      """
      if not self._port_ref._is_equivalent(p):
        retval = p.notify_connect(self._connector_profile)
        if retval != RTC.RTC_OK:
          self.return_code = retval

  ##
  # @if jp
  # @class disconnect_func
  # @brief Port ����³�����Ԥ� Functor
  # @else
  # @brief A functor to disconnect Ports
  # @endif
  class disconnect_func:
    def __init__(self, p, prof):
      """
       \param p(RTC.PortService)
       \param prof(RTC.ConnectorProfile)
      """
      self._port_ref = p
      self._connector_profile = prof
      self.return_code = RTC.RTC_OK
      
    def __call__(self, p):
      """
       \param p(RTC.PortService)
      """
      if not self._port_ref._is_equivalent(p):
        retval = p.disconnect(self._connector_profile.connector_id)
        if retval != RTC.RTC_OK:
          self.return_code = retval

  ##
  # @if jp
  # @class disconnect_all_func
  # @brief Port ������³�����Ԥ� Functor
  # @else
  # @brief A functor to disconnect all Ports
  # @endif
  class disconnect_all_func:
    def __init__(self, p):
      """
       \param p(OpenRTM_aist.PortBase)
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

  ##
  # @if jp
  # @class find_interface
  # @brief name �� polarity ���� interface ��õ�� Functor
  # @else
  # @brief A functor to find interface from name and polarity
  # @endif
  class find_interface:
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
