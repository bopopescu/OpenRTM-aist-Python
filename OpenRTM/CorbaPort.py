#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
#  \file  CorbaPort.py
#  \brief CorbaPort class
#  \date  $Date: 2007/09/26 $
#  \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006-2008
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.

from omniORB import any
import traceback
import sys

import OpenRTM
import RTC, RTC__POA



##
# @if jp
# @class CorbaPort
# @brief RT ����ݡ��ͥ�� CORBA provider/consumer �� Port
#
# CorbaPort �� RT ����ݡ��ͥ�Ȥˤ����ơ��桼������� CORBA ���֥�������
# �����ӥ�����ӥ��󥷥塼�ޤ��󶡤��� Port �����Ǥ��롣
# <p>
# RT ����ݡ��ͥ�Ȥϡ�Port ��𤷤ƥ桼����������� CORBA �����ӥ�����
# ���뤳�Ȥ��Ǥ�������� RT Service (Provider) �ȸƤ֡�
# �ޤ���¾�� RT ����ݡ��ͥ�ȤΥ����ӥ������Ѥ��뤿��� CORBA ���֥�������
# �Υץ졼���ۥ�����󶡤��뤳�Ȥ��Ǥ�������� RT Service Consumer �ȸƤ֡�
# <p>
# CorbaPort ��Ǥ�դο��� Provider ����� Consumer ��������뤳�Ȥ��Ǥ���
# Port Ʊ�Τ���³����ݤ��б����� Provider �� Consumer ��Ŭ�ڤ˴�Ϣ�դ���
# ���Ȥ��Ǥ��롣
# <p>
# CorbaPort ���̾�ʲ��Τ褦�����Ѥ���롣
#
# <pre>
# # CORBA�ݡ��Ȥν����
# self._myServicePort = OpenRTM.CorbaPort("MyService")
#
# // Provider¦
# # ���� Port ���󶡤��� Serivce Provider �ν����
# self._mpros = MyServiceSVC_impl()
# # Service Provider �� Port ����Ͽ
# self._myServicePort.registerProvider("myservice0", "MyService", self._mpros)
#
# // Consumer¦
# # ���� Port ���󶡤��� Serivce Consumer �ν����
# self._mycons = OpenRTM.CorbaConsumer(interfaceType=_GlobalIDL.MyService)
# # Service Consumer �� Port ����Ͽ
# self._myServicePort.registerConsumer("myservice0", "MyService", self._mycons)
#
#
# # CORBA�ݡ��Ȥؤ���Ͽ
# self.registerPort(self._myServicePort)
#
# // connect ���Ԥ�줿��
# self.my_cons._ptr().your_service_function(); // YourService �δؿ��򥳡���
#
# // connect ���줿 �̤Υ���ݡ��ͥ�Ȥˤ�����
# self.m_cons1._ptr().my_service_function(); // MyService �δؿ��򥳡���
# </pre>
#
# ���Τ褦�ˡ��󶡤����� Service Provider �� registerProvider() ����Ͽ
# ���뤳�Ȥˤ�ꡢ¾�Υ���ݡ��ͥ�Ȥ������Ѳ�ǽ�ˤ���¾����
# ���Ѥ����� Service Consumer �� registerConsumer() ����Ͽ���뤳�Ȥˤ��
# ¾�Υ���ݡ��ͥ�Ȥ� Service �򥳥�ݡ��ͥ��������Ѳ�ǽ�ˤ��뤳�Ȥ�
# �Ǥ��롣
#
# @since 0.4.0
#
# @else
# @class CorbaPort
# @brief RT Conponent CORBA service/consumer Port
#
# CorbaPort is an implementation of the Port of RT-Component's that provides
# user-defined CORBA Object Service and Consumer.
# <p>
# RT-Component can provide user-defined CORBA serivces, which is called
# RT-Serivce (Provider), through the Ports.
# RT-Component can also provide place-holder, which is called RT-Serivce
# Consumer, to use other RT-Component's service.
# <p>
# The CorbaPort can manage any number of Providers and Consumers, can
# associate Consumers with correspondent Providers when establishing
# connection among Ports.
# <p>
# Usually, CorbaPort is used like the following.
#
# <pre>
# RTC::CorbaPort m_port0; // declaration of Port
#
# MyService_impl m_mysvc0; // Serivce Provider that is provided by the Port
# RTC::CorbaConsumer<YourService> m_cons0; // Consumer of the Port
#
# // register Service Provider to the Port
# m_port0.registerProvider("MyService0", "Generic", m_mysvc0);
# // register Service Consumer to the Port
# m_port0.registerConsumer("YourService0", "Generic", m_cons0 );
#
# // after connect established
#
# m_cons0->your_service_function(); // call a YourService's function
#
# // in another component that is connected with the Port
# m_cons1->my_service_function(); // call a MyService's function
# </pre>
#
# Registering Service Provider by registerProvider(), it can be used from
# other RT-Components.
# Registering Service Consumer by registerConsumer(), other RT-Component's
# services can be used through the consumer object.
#
# @since 0.4.0
#
# @endif
class CorbaPort(OpenRTM.PortBase):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # @param self
  # @param name Port ��̾��
  #
  # @else
  #
  # @brief Constructor
  #
  # @param name The name of Port 
  #
  # @endif
  def __init__(self, name):
    OpenRTM.PortBase.__init__(self, name)
    self.addProperty("port.port_type", "CorbaPort")
    self._providers = []
    self._consumers = []


  ##
  # @if jp
  #
  # @brief Provider ����Ͽ����
  #
  # ���� Port �ˤ������󶡤����������Х�Ȥ򤳤� Port ���Ф�����Ͽ���롣
  # �����Х�Ȥϡ�������Ϳ������ instance_name, type_name ��
  # �����Х�ȼ��ȤΥ��󥹥���̾����ӥ�����̾�Ȥ��ơ������Х�Ȥ�
  # ��Ϣ�դ����롣
  #
  # @param self
  # @param instance_name �����Х�ȤΥ��󥹥���̾
  # @param type_name �����Х�ȤΥ�����̾
  # @param provider CORBA �����Х��
  #
  # @return ����Ʊ̾�� instance_name ����Ͽ����Ƥ���� false ���֤���
  #
  # @else
  #
  # @brief Register provider
  #
  # This operation registers a servant, which is provided in this Port,
  # to the Port. The servant is associated with "instance_name" and
  # "type_name" as the instance name of the servant and as the type name
  # of the servant.
  #
  # @param self
  # @param instance_name Servant instance name
  # @param type_name Servant type name
  # @param provider CORBA Servant
  #
  # @return if same instance_name is registered, this will return False
  #
  # @endif
  def registerProvider(self, instance_name, type_name, provider):
    if not self.appendInterface(instance_name, type_name, RTC.PROVIDED):
      return False

    oid = self._default_POA().activate_object(provider)
    obj = self._default_POA().id_to_reference(oid)

    key = "port"
    key = key + "." + str(type_name) + "." + str(instance_name)

    OpenRTM.CORBA_SeqUtil.push_back(self._providers,
                    OpenRTM.NVUtil.newNV(key, obj))

    return True


  ##
  # @if jp
  #
  # @brief Consumer ����Ͽ����
  #
  # ���� Port ���׵᤹�륵���ӥ��Υץ졼���ۥ���Ǥ��륳�󥷥塼��
  # (Consumer) ����Ͽ���롣
  # Consumer ����Ϣ�դ����륵���ӥ��Υ��󥹥���̾����ӥ�����̾�Ȥ��ơ�
  # ������ instance_name, type_name ����� Consumer ���Ȥ�Ϳ���뤳�Ȥˤ�ꡢ
  # �����Ǥ���餬��Ϣ�դ����롣
  # Port �֤���³ (connect) �� �ˤϡ�Ʊ��� instance_name, type_name �����
  # �����ӥ���¾�� Port ������ (Provide) ����Ƥ����硢���Υ����ӥ���
  # ���֥������Ȼ��Ȥ���ưŪ�� Consumer �˥��åȤ���롣
  #
  # @param self
  # @param instance_name Consumer ���׵᤹�륵���ӥ��Υ��󥹥���̾
  # @param type_name Consumer ���׵᤹�륵���ӥ��Υ�����̾
  # @param consumer CORBA �����ӥ����󥷥塼��
  #
  # @return ����Ʊ̾�� instance_name ����Ͽ����Ƥ���� false ���֤���
  #
  # @else
  #
  # @brief Register consumer
  #
  # This operation registers a consumer, which requiers a service,
  # to the other Port. The consumer is associated with "instance_name" and
  # "type_name" as the instance name of the service and as the type name
  # of the service that is required.
  #
  # @param self
  # @param instance_name An instance name of the service required
  # @param type_name An type name of the service required
  # @param consumer CORBA service consumer
  #
  # @return False would be returned if the same instance_name is registered
  #
  # @endif
  def registerConsumer(self, instance_name, type_name, consumer):
    if not self.appendInterface(instance_name, type_name, RTC.REQUIRED):
      return False

    cons = self.Consumer(instance_name, type_name, consumer)
    self._consumers.append(cons)

    return True


  ##
  # @if jp
  #
  # @brief Interface ������������
  #
  # ���� Port����ͭ���� Provider �˴ؤ������� ConnectorProfile::properties
  # ���������롣
  # �����������ϡ�NVList�� name �� value �Ȥ��ưʲ��Τ�Τ���Ǽ����롣
  #
  # - port.<type_name>.<instance_name>: <CORBA::Object_ptr>
  #
  # �����ǡ�
  # - <type_name>: PortInterfaceProfile::type_name
  # - <instance_name>: PortInterfaceProfile::instance_name<br>
  # �Ǥ��롣<br>
  # ConnectorProfile::properties �Ǥϡ������� .(�ɥå�)ɽ���ǡ�
  # NameValue �Υ����Ȥ��Ƥ��롣�������äơ�
  #
  # <pre>
  #  PortInterfaceProfile
  #  {
  #    instance_name = "PA10_0";
  #    type_name     = "Manipulator";
  #    polarity      = PROVIDED;
  #  }
  #</pre>
  #
  # �ʤ�С�
  #
  # <pre>
  # NameValue = { "port.Manipulator.PA10_0": <Object reference> }
  # </pre>
  #
  # �Ȥ��ä��ͤ� ConnectorProfile::properties �˳�Ǽ���졢¾�Υݡ��Ȥ��Ф���
  # ��ã����롣¾�� Port �Ǥ��Υ��󥿡��ե���������Ѥ��� Consumer ��
  # ¸�ߤ���С�ConnectorProfile ���餳�Υ������饪�֥������ȥ�ե���󥹤�
  # ���������餫�η��ǻ��Ѥ���롣
  #
  # @param self
  # @param connector_profile ���ͥ����ץ�ե�����
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Publish interface information
  #
  # @endif
  def publishInterfaces(self, connector_profile):
    OpenRTM.CORBA_SeqUtil.push_back_list(connector_profile.properties,
                       self._providers)
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief Interface ����³����
  #
  # ���� Port����ͭ���� Consumer ��Ŭ�礹�� Provider �˴ؤ�������
  # ConnectorProfile::properties ������Ф� Consumer �˥��֥������Ȼ���
  # �򥻥åȤ��롣
  #
  # ����Consumer ��
  # <pre>
  #  PortInterfaceProfile
  #  {
  #    instance_name = "PA10_0";
  #    type_name     = "Manipulator";
  #    polarity      = REQUIRED;
  #  }
  # </pre>
  # �Ȥ�����Ͽ����Ƥ���С�¾�� Port ��
  # <pre>
  #  PortInterfaceProfile
  #  {
  #    instance_name = "PA10_0";
  #    type_name     = "Manipulator";
  #    polarity      = PROVIDED;
  #  }
  # </pre> 
  # �Ȥ�����Ͽ����Ƥ��� Serivce Provider �Υ��֥������Ȼ��Ȥ�õ����
  # Consumer �˥��åȤ��롣
  # �ºݤˤϡ�ConnectorProfile::properties ��
  # <pre>
  # NameValue = { "port.Manipulator.PA10_0": <Object reference> }
  # </pre>
  # �Ȥ�����Ͽ����Ƥ��� NameValue ��õ�������Υ��֥������Ȼ��Ȥ�
  # Consumer �˥��åȤ��롣
  #
  # @param self
  # @param connector_profile ���ͥ����ץ�ե�����
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Subscribe interfaces
  #
  # @endif
  def subscribeInterfaces(self, connector_profile):
    nv = connector_profile.properties
    OpenRTM.CORBA_SeqUtil.for_each(nv, self.subscribe(self._consumers))
    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief Interface �ؤ���³��������
  #
  # Ϳ����줿 ConnectorProfile �˴�Ϣ���� Consumer �˥��åȤ��줿
  # ���٤Ƥ� Object ���������³�������롣
  #
  # @param self
  # @param connector_profile ���ͥ����ץ�ե�����
  #
  # @else
  #
  # @brief Unsubscribe interfaces
  #
  # @endif
  def unsubscribeInterfaces(self, connector_profile):
    nv = connector_profile.properties

    OpenRTM.CORBA_SeqUtil.for_each(nv, self.unsubscribe(self._consumers))



  ##
  # @if jp
  # @brief Consumer �ξ�����Ǽ���빽¤��
  # @else
  # @brief Consumer inforamtion struct
  # @endif
  class Consumer:
    def __init__(self, _instance_name, _type_name, _cons, _consumer=None):
      if _consumer:
        self.name = _consumer.name
        self.consumer = _consumer.consumer
        return
      
      self.name = "port."+str(_type_name)+"."+str(_instance_name)
      self.consumer = _cons



  ##
  # @if jp
  # @brief ConnectorProfile �� Consuemr ����Ӥ򤷥��֥������Ȼ��Ȥ�
  #        ���åȤ��뤿��� Functor
  # @else
  # @brief Subscription mutching functor for Consumer
  # @endif
  class subscribe:
    def __init__(self, cons):
      self._cons = cons
      self._len  = len(cons)

    def __call__(self, nv):
      for i in range(self._len):
        name_ = nv.name
        if self._cons[i].name == name_:
          try:
            obj = any.from_any(nv.value, keep_structs=True)
            self._cons[i].consumer.setObject(obj)
          except:
            traceback.print_exception(*sis.exc_info())



  ##
  # @if jp
  # @brief Consumer �Υ��֥������Ȥ�������뤿��� Functor
  # @else
  # @brief Unsubscription functor for Consumer
  # @endif
  class unsubscribe:
    def __init__(self, cons):
      self._cons = cons
      self._len  = len(cons)

    def __call__(self, nv):
      for i in range(self._cons):
        name_ = nv.name
        if self._cons[i].name == name_:
          self._cons[i].consumer.releaseObject()
