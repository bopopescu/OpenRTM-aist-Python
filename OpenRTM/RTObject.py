#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file RTObject.py
 \brief RT component base class
 \date $Date: $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


from omniORB import any
from omniORB import CORBA
import string
import sys
import traceback

import RTC,RTC__POA
import SDOPackage,SDOPackage__POA
import OpenRTM

default_conf = [
	"implementation_id","",
	"type_name",         "",
	"description",       "",
	"version",           "",
	"vendor",            "",
	"category",          "",
	"activity_type",     "",
	"max_instance",      "",
	"language",          "",
	"lang_type",         "",
	"conf",              "",
	"" ]

class RTObject_impl(RTC__POA.DataFlowComponent):
	def __init__(self, manager=None, orb=None, poa=None):
		"""
		 \param manager(OpenRTM.Manager)
		 \param orb(CORBA.ORB)
		 \param poa(CORBA.POA)
		"""
		if manager != None:
			self._manager = manager
			self._orb = self._manager.getORB()
			self._poa = self._manager.getPOA()
			self._portAdmin = OpenRTM.PortAdmin(self._manager.getORB(),self._manager.getPOA())
		else:
			self._manager = None
			self._orb = orb
			self._poa = poa
			self._portAdmin = OpenRTM.PortAdmin(self._orb,self._poa)
			
		self._created = True
		self._alive = False
		self._properties = OpenRTM.Properties(defaults_str=default_conf)
		self._configsets = OpenRTM.ConfigAdmin(self._properties.getNode("conf"))
		self._profile = RTC.ComponentProfile("","","","","","",[],None,[])
		
		self._SdoConfigImpl = OpenRTM.Configuration_impl(self._configsets)
		self._SdoConfig = self._SdoConfigImpl.getObjRef()
		self._execContexts = []
		self._objref = None
		self._sdoOwnedOrganizations = [] #SDOPackage.OrganizationList()
		self._sdoSvcProfiles        = [] #SDOPackage.ServiceProfileList()
		self._sdoOrganizations      = [] #SDOPackage.OrganizationList()
		self._sdoStatus             = [] #SDOPackage.NVList()

		return


	def __del__(self):
		return

    #============================================================
    # Overridden functions
    #============================================================
	def onInitialize(self):
		"""
		The initialize action (on CREATED->ALIVE transition)
		formaer rtc_init_entry() 
		"""
		return RTC.RTC_OK


	def onFinalize(self):
		"""
		The finalize action (on ALIVE->END transition)
		formaer rtc_exiting_entry()
		"""
		return RTC.RTC_OK


	def onStartup(self, ec_id):
		"""
		The startup action when ExecutionContext startup
		former rtc_starting_entry()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onShutdown(self, ec_id):
		"""
		The shutdown action when ExecutionContext stop
		former rtc_stopping_entry()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onActivated(self, ec_id):
		"""
		The activated action (Active state entry action)
		former rtc_active_entry()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onDeactivated(self, ec_id):
		"""
		The deactivated action (Active state exit action)
		former rtc_active_exit()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onExecute(self, ec_id):
		"""
		The execution action that is invoked periodically
		former rtc_active_do()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onAborting(self, ec_id):
		"""
		The aborting action when main logic error occurred.
		former rtc_aborting_entry()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onError(self, ec_id):
		"""
		The error action in ERROR state
		former rtc_error_do()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onReset(self, ec_id):
		"""
		The reset action that is invoked resetting
		This is same but different the former rtc_init_entry()

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onStateUpdate(self, ec_id):
		"""
		The state update action that is invoked after onExecute() action
		no corresponding operation exists in OpenRTm-aist-0.2.0

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK


	def onRateChanged(self, ec_id):
		"""
		The action that is invoked when execution context's rate is changed
		no corresponding operation exists in OpenRTm-aist-0.2.0

		\param ec_id(long)
		\return RTC.ReturnCode_t
		"""
		return RTC.RTC_OK 

    #============================================================
    # RTC::LightweightRTObject
    #============================================================

	def initialize(self):
		"""
		\if jp

		\breif RTC����������

		���Υ��ڥ졼�����ƤӽФ��η�̤Ȥ��ơ�ComponentAction::on_initialize
		������Хå��ؿ����ƤФ�롣
		����
		Created���֤ˤ���Ȥ��ˤΤߡ���������Ԥ��롣¾�ξ��֤ˤ�����ˤ�
		ReturnCode_t::PRECONDITION_NOT_MET ���֤���ƤӽФ��ϼ��Ԥ��롣
		���Υ��ڥ졼������RTC�Υߥɥ륦��������ƤФ�뤳�Ȥ����ꤷ�Ƥ��ꡢ
		���ץꥱ�������ȯ�Ԥ�ľ�ܤ��Υ��ڥ졼������Ƥ֤��Ȥ�����
		����Ƥ��ʤ���

		\else

		\breif Initialize the RTC that realizes this interface.

		The invocation of this operation shall result in the invocation of the
		callback ComponentAction::on_initialize.

		Constraints
		- An RTC may be initialized only while it is in the Created state. Any
			attempt to invoke this operation while in another state shall fail
			with ReturnCode_t::PRECONDITION_NOT_MET.
		- Application developers are not expected to call this operation
			directly; it exists for use by the RTC infrastructure.

		\endif
		"""
		ret = self.on_initialize()
		self._created = False

		if ret == RTC.RTC_OK:
			if len(self._execContexts) > 0:
				self._execContexts[0].start()
			self._alive = True
		
		return ret


	def finalize(self):
		"""
		\if jp

		\brief RTC����ν����Τ��Ὢλ������

		���Υ��ڥ졼�����ƤӽФ��Ϸ�̤Ȥ���ComponentAction::on_finalize()
		��ƤӽФ���

		����
		- ���� RTC ��°���� Running ���֤μ¹ԥ���ƥ������桢Active ���֤ˤ���
			��Τ�����Ф��� RTC �Ͻ�λ����ʤ������ξ�硢���Υ��ڥ졼�����Ƥ�
			�Ф��Ϥ����ʤ���� ReturnCode_t::PRECONDITION_NOT_ME �Ǽ��Ԥ��롣
		- ���� RTC �� Created ���֤Ǥ����硢��λ�����ϹԤ��ʤ���
			���ξ�硢���Υ��ڥ졼�����ƤӽФ��Ϥ����ʤ���� 
			ReturnCode_t::PRECONDITION_NOT_MET �Ǽ��Ԥ��롣
		- ���ץꥱ�������ȯ�ԤϤ��Υ��ڥ졼������ľ��Ū�˸ƤӽФ����Ȥ�
			�ޤ�Ǥ��ꡢ�����Ƥ���RTC����ե饹�ȥ饯���㤫��ƤӽФ���롣

		\else

		\brief Finalize the RTC for preparing it for destruction

		This invocation of this operation shall result in the invocation of the
		callback ComponentAction::on_finalize.

		Constraints
		- An RTC may not be finalized while it is Active in any Running
			execution context. Any attempt to invoke this operation at such a time
			shall fail with ReturnCode_t::PRECONDITION_NOT_MET.
		- An RTC may not be finalized while it is in the Created state.
			Any attempt to invoke this operation while in that state shall fail
			with ReturnCode_t::PRECONDITION_NOT_MET.
		- Application developers are not expected to call this operation
			directly; it exists for use by the RTC infrastructure.

		\endif
		"""
		if self._created:
			return RTC.PRECONDITION_NOT_MET

		for execContext in self._execContexts:
			if execContext.is_running():
				return RTC.PRECONDITION_NOT_MET

		ret = self.on_finalize()
		self.shutdown()
		return ret


	def exit(self):
		"""
		\if jp

		\brief RTC����ߤ��������Υ���ƥ�Ĥȶ��˽�λ������

		���� RTC �������ʡ��Ǥ��뤹�٤Ƥμ¹ԥ���ƥ����Ȥ���ߤ���롣
		���� RTC ��¾�μ¹ԥ���ƥ����Ȥ��ͭ���� RTC ��°����¹ԥ���ƥ�����
		(i.e. �¹ԥ���ƥ����Ȥ��ͭ���� RTC �Ϥ��ʤ�����μ¹ԥ���ƥ����Ȥ�
		�����ʡ��Ǥ��롣)�˻��ä��Ƥ����硢���� RTC �Ϥ����Υ���ƥ����Ⱦ�
		�������������ʤ���Фʤ�ʤ���

		����
		- RTC �����������Ƥ��ʤ���С���λ�����뤳�ȤϤǤ��ʤ���
			Created ���֤ˤ��� RTC �� exit() ��ƤӽФ�����硢
			ReturnCode_t::PRECONDITION_NOT_MET �Ǽ��Ԥ��롣

		\else

		\brief Stop the RTC's and finalize it along with its contents.

		Any execution contexts for which the RTC is the owner shall be stopped. 
		If the RTC participates in any execution contexts belonging to another
		RTC that contains it, directly or indirectly (i.e. the containing RTC
		is the owner of the ExecutionContext), it shall be deactivated in those
		contexts.
		After the RTC is no longer Active in any Running execution context, it
		and any RTCs contained transitively within it shall be finalized.

		Constraints
		- An RTC cannot be exited if it has not yet been initialized. Any
			attempt to exit an RTC that is in the Created state shall fail with
			ReturnCode_t::PRECONDITION_NOT_MET.

		\endif
		"""
		if len(self._execContexts) > 0:
			self._execContexts[0].stop()
			self._alive = False

		OpenRTM.CORBA_SeqUtil.for_each(self._execContexts,
									   self.deactivate_comps(self._objref))
		return self.finalize()


	def is_alive(self):
		"""
		\if jp
		\brief
		\else
		\brief
		A component is alive or not regardless of the execution context from
		which it is observed. However, whether or not it is Active, Inactive,
		or in Error is dependent on the execution context(s) in which it is
		running. That is, it may be Active in one context but Inactive in
		another. Therefore, this operation shall report whether this RTC is
		either Active, Inactive or in Error; which of those states a component
		is in with respect to a particular context may be queried from the
		context itself.
		\endif
		"""
		return self._alive


	def get_contexts(self):
		"""
		\if jp
		\brief [CORBA interface] ExecutionContextList���������
		\else
		\brief [CORBA interface] Get ExecutionContextList.
		\endif
		"""
		execlist = []
		OpenRTM.CORBA_SeqUtil.for_each(self._execContexts, self.ec_copy(execlist))
		return execlist


	def get_context(self, ec_id):
		"""
		\if jp
		\brief [CORBA interface] ExecutionContext���������
		\param ec_id(long)
		\else
		\brief [CORBA interface] Get ExecutionContext.
		\param ec_id(long)
		\endif
		"""
		if ec_id > (len(self._execContexts) - 1):
			return RTC.ExecutionContext._nil

		return self._execContexts[ec_id]
    

    #============================================================
    # RTC::RTObject
    #============================================================

	def get_component_profile(self):
		"""
		\if jp
		\brief [RTObject CORBA interface] ����ݡ��ͥ�ȥץ�ե�����μ���

		��������ݡ��ͥ�ȤΥץ�ե����������֤��� 
		\else
		\brief [RTObject CORBA interface] Get RTC's profile

		This operation returns the ComponentProfile of the RTC
		\endif
		"""
		try:
			return RTC.ComponentProfile(self._profile.instance_name,
										self._profile.type_name,
										self._profile.description,
										self._profile.version,
										self._profile.vendor,
										self._profile.category,
										self._profile.port_profiles,
										self._profile.parent,
										self._profile.properties)
		
		except:
			traceback.print_exception(*sys.exc_info())
		assert(False)
		return 0


	def get_ports(self):
		"""
		\if jp
		\brief [RTObject CORBA interface] �ݡ��Ȥμ���

		��������ݡ��ͥ�Ȥ���ͭ����ݡ��Ȥλ��Ȥ��֤���
		\else
		\brief [RTObject CORBA interface] Get Ports

		This operation returns a list of the RTCs ports.
		\endif
		"""
		try:
			return self._portAdmin.getPortList()
		except:
			traceback.print_exception(*sys.exc_info())

		assert(False)
		return 0


	def get_execution_context_services(self):
		"""
		\if jp
		\brief [RTObject CORBA interface] ExecutionContextAdmin �μ���

		���Υ��ڥ졼������������RTC ����°���� ExecutionContext�˴�Ϣ����
		ExecutionContextAdmin �Υꥹ�Ȥ��֤���
		\else
		\brief [RTObject CORBA interface] Get ExecutionContextAdmin

		This operation returns a list containing an ExecutionContextAdmin for
		every ExecutionContext owned by the RTC.	
		\endif
		"""
		try:
			return self._execContexts
		except:
			traceback.print_exception(*sys.exc_info())

		assert(False)
		return 0


    # RTC::ComponentAction
	def attach_executioncontext(self, exec_context):
		"""
		 \param exec_context(RTC.ExecutionContext)
		"""
		ecs = exec_context._narrow(RTC.ExecutionContextService)
		if CORBA.is_nil(ecs):
			return -1

		self._execContexts.append(ecs)

		return long(len(self._execContexts) -1)

	
	def detach_executioncontext(self, ec_id):
		"""
		 \param exec_context(RTC.ExecutionContext)
		"""
		if ec_id > (len(self._execContexts) - 1):
			return RTC.BAD_PARAMETER

		if CORBA.is_nil(self._execContexts[ec_id]):
			return RTC.BAD_PARAMETER
		
		self._execContexts[ec_id] = RTC.ExecutionContextService._nil
		return RTC.RTC_OK

	
	def on_initialize(self):
		ret = RTC.RTC_ERROR
		try:
			ret = self.onInitialize()
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_finalize(self):
		ret = RTC.RTC_ERROR
		try:
			ret = self.onFinalize()
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_startup(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onStartup(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_shutdown(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onShutdown(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_activated(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			self._configsets.update()
			ret = self.onActivated(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_deactivated(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onDeactivated(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_aborting(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onAborting(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret


	def on_error(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onError(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret


	def on_reset(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onReset(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret

	
	def on_execute(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onExecute(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret


	def on_state_update(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onStateUpdate(ec_id)
			self._configsets.update()
		except:
			return RTC.RTC_ERROR
		
		return ret


	def on_rate_changed(self, ec_id):
		"""
		 \param ec_id(long)
		"""
		ret = RTC.RTC_ERROR
		try:
			ret = self.onRateChanged(ec_id)
		except:
			return RTC.RTC_ERROR
		
		return ret


    #============================================================
    # SDOPackage::SdoSystemElement
    #============================================================
	def get_owned_organizations(self):
		"""
		\if jp
		\brief [CORBA interface] Organization �ꥹ�Ȥμ��� 

		SDOSystemElement ��0�Ĥ⤷���Ϥ���ʾ�� Organization ���ͭ���뤳�Ȥ�
		����롣 SDOSystemElement ��1�İʾ�� Organization ���ͭ���Ƥ�����
		�ˤϡ����Υ��ڥ졼�����Ͻ�ͭ���� Organization �Υꥹ�Ȥ��֤���
		�⤷Organization���Ĥ��ͭ���Ƥ��ʤ�����ж��Υꥹ�Ȥ��֤���
		\else
		\brief [CORBA interface] Getting Organizations

		SDOSystemElement can be the owner of zero or more organizations.
		If the SDOSystemElement owns one or more Organizations, this operation
		returns the list of Organizations that the SDOSystemElement owns.
		If it does not own any Organization, it returns empty list.
		\endif
		"""
		try:
			return self._sdoOwnedOrganizations
		except:
			raise SDOPackage.NotAvailable

		return []


    #============================================================
    # SDOPackage::SDO
    #============================================================
	def get_sdo_id(self):
		"""
		\if jp

		\brief [CORBA interface] SDO ID �μ���

		SDO ID ���֤����ڥ졼�����
		���Υ��ڥ졼�����ϰʲ��η����㳰��ȯ�������롣

		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\return    �꥽�����ǡ�����ǥ���������Ƥ��� SDO �� ID

		\else

		\brief [CORBA interface] Getting SDO ID

		This operation returns id of the SDO.
		This operation throws SDOException with one of the following types.

		\exception SDONotExists if the target SDO does not exist.
		\exception NotAvailable if the target SDO is reachable but cannot
			respond.
		\exception InternalError if the target SDO cannot execute the operation
			completely due to some internal error.
		\return    id of the SDO defined in the resource data model.

		\endif
		"""
		try:
			return self._profile.instance_name
		except:
			raise SDOPackage.InternalError("get_sdo_id()")


	def get_sdo_type(self):
		"""
		\if jp

		\brief [CORBA interface] SDO �����פμ���

		SDO Type ���֤����ڥ졼�����
		���Υ��ڥ졼�����ϰʲ��η����㳰��ȯ�������롣

		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\return    �꥽�����ǡ�����ǥ���������Ƥ��� SDO �� Type

		\else

		\brief [CORBA interface] Getting SDO type

		This operation returns sdoType of the SDO.
		This operation throws SDOException with one of the following types.

		\exception SDONotExists if the target SDO does not exist.
		\exception NotAvailable if the target SDO is reachable but cannot
			respond.
		\exception InternalError if the target SDO cannot execute the operation
			completely due to some internal error.
		\return    Type of the SDO defined in the resource data model.

		\endif
		"""
		try:
			return self._profile.description
		except:
			raise SDOPackage.InternalError("get_sdo_type()")
		return ""


	def get_device_profile(self):
		"""
		\if jp

		\brief [CORBA interface] SDO DeviceProfile �ꥹ�Ȥμ��� 

		SDO �� DeviceProfile ���֤����ڥ졼����� SDO ���ϡ��ɥ������ǥХ���
		�˴�Ϣ�դ����Ƥ��ʤ����ˤϡ����� DeviceProfile ���֤���롣
		���Υ��ڥ졼�����ϰʲ��η����㳰��ȯ�������롣

		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\return    SDO DeviceProfile

		\else

		\brief [CORBA interface] Getting SDO DeviceProfile

		This operation returns the DeviceProfile of the SDO. If the SDO does not
		represent any hardware device, then a DeviceProfile with empty values
		are returned.
		This operation throws SDOException with one of the following types.

		\exception NotAvailable if the target SDO is reachable but cannot
			respond.
		\exception InternalError if the target SDO cannot execute the operation
			completely due to some internal error.
		\return    The DeviceProfile of the SDO.

		\endif
		"""
		try:
			dprofile = SDOPackage.DeviceProfile(self._profile.category,
												self._profile.vendor,
												self._profile.type_name,
												self._profile.version,
												self._profile.properties)
			return dprofile
		except:
			raise SDOPackage.InternalError("get_device_profile()")

		return SDOPackage.DeviceProfile("","","","",[])


	def get_service_profiles(self):
		"""
		\if jp

		\brief [CORBA interface] SDO ServiceProfile �μ��� 

		SDO ����ͭ���Ƥ��� Service �� ServiceProfile ���֤����ڥ졼�����
		SDO �������ӥ����Ĥ��ͭ���Ƥ��ʤ����ˤϡ����Υꥹ�Ȥ��֤���
		���Υ��ڥ졼�����ϰʲ��η����㳰��ȯ�������롣

		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\return    SDO ���󶡤������Ƥ� Service �� ServiceProfile��

		\else

		\brief [CORBA interface] Getting SDO ServiceProfile

		This operation returns a list of ServiceProfiles that the SDO has.
		If the SDO does not provide any service, then an empty list is returned.
		This operation throws SDOException with one of the following types.

		\exception NotAvailable if the target SDO is reachable but cannot
			respond.
		\exception InternalError if the target SDO cannot execute the operation
			completely due to some internal error.
		\return    List of ServiceProfiles of all the services the SDO is
			providing.

		\endif
		"""
		try:
			return self._sdoSvcProfiles
		except:
			raise SDOPackage.InternalError("get_service_profiles()")

		return []


	def get_service_profile(self, _id):
		"""
		\if jp

		\brief [CORBA interface] �����ServiceProfile�μ��� 

		���� "id" �ǻ��ꤵ�줿̾���Υ����ӥ��� ServiceProfile ���֤���

		\param     _id(string) SDO Service �� ServiceProfile �˴�Ϣ�դ���줿���̻ҡ�
		\return    ���ꤵ�줿 SDO Service �� ServiceProfile��
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������

		\else

		\brief [CORBA interface] Getting Organizations

		This operation returns the ServiceProfile that is specified by the
		argument "id."

		\param     _id(string) The identifier referring to one of the ServiceProfiles.
		\return    The profile of the specified service.
		\exception NotAvailable If the target SDO is reachable but cannot
			respond.
		\exception InternalError If the target SDO cannot execute the operation
			completely due to some internal error.

		\endif
		"""
		if not _id:
			raise SDOPackage.InvalidParameter("get_service_profile(): Empty name.")

		try:
			index = OpenRTM.CORBA_SeqUtil.find(self._sdoSvcProfiles, self.svc_name(_id))

			if index < 0:
				raise SDOPackage.InvalidParameter("get_service_profile(): Not found")

			return self._sdoSvcProfiles[index]
		except:
			raise SDOPackage.InternalError("get_service_profile()")

		return SDOPackage.ServiceProfile("", "", [], None)


	def get_sdo_service(self, _id):
		"""
		\if jp

		\brief [CORBA interface] ���ꤵ�줿 SDO Service �μ���

		���Υ��ڥ졼�����ϰ��� "id" �ǻ��ꤵ�줿̾���ˤ�äƶ��̤����
		SDO �� Service �ؤΥ��֥������Ȼ��Ȥ��֤��� SDO �ˤ���󶡤����
		Service �Ϥ��줾���դμ��̻Ҥˤ����̤���롣

		\param _id(string) SDO Service �˴�Ϣ�դ���줿���̻ҡ�
		\return �׵ᤵ�줿 SDO Service �ؤλ��ȡ�

		\else

		\brief [CORBA interface] Getting specified SDO Service's reference

		This operation returns an object implementing an SDO's service that
		is identified by the identifier specified as an argument. Different
		services provided by an SDO are distinguished with different
		identifiers. See OMG SDO specification Section 2.2.8, "ServiceProfile,"
		on page 2-12 for more details.

		\param _id(string) The identifier referring to one of the SDO Service
		\return The object implementing the requested service.

		\endif
		"""
		if not _id:
			raise SDOPackage.InvalidParameter("get_service(): Empty name.")

		try:
			index = OpenRTM.CORBA_SeqUtil.find(self._sdoSvcProfiles, self.svc_name(_id))

			if index < 0:
				raise SDOPackage.InvalidParameter("get_service(): Not found")

			return self._sdoSvcProfiles[index].service
		except:
			raise SDOPackage.InternalError("get_service()")
		return SDOPackage.SDOService._nil


	def get_configuration(self):
		"""
		\if jp

		\brief [CORBA interface] Configuration ���֥������Ȥμ��� 

		���Υ��ڥ졼������ Configuration interface �ؤλ��Ȥ��֤���
		Configuration interface �ϳ� SDO ��������뤿��Υ��󥿡��ե�������
		�ҤȤĤǤ��롣���Υ��󥿡��ե������� DeviceProfile, ServiceProfile,
		Organization ��������줿 SDO ��°���ͤ����ꤹ�뤿��˻��Ѥ���롣
		Configuration ���󥿡��ե������ξܺ٤ˤĤ��Ƥϡ�OMG SDO specification
		�� 2.3.5��, p.2-24 �򻲾ȤΤ��ȡ�

		\return SDO �� Configuration ���󥿡��ե������ؤλ���
		\exception InterfaceNotImplemented SDO��Configuration���󥿡��ե�������
			�����ʤ���
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������

		\else

		\brief [CORBA interface] Getting Configuration object

		This operation returns an object implementing the Configuration
		interface. The Configuration interface is one of the interfaces thatreturn RTC.BAD_PARAMETER
		each SDO maintains. The interface is used to configure the attributes
		defined in DeviceProfile, ServiceProfile, and Organization.
		See OMG SDO specification Section 2.3.5, "Configuration Interface,"
		on page 2-24 for more details about the Configuration interface.

		\return The Configuration interface of an SDO.
		\exception InterfaceNotImplemented The target SDO has no Configuration
			interface.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		if self._SdoConfig == None:
			raise SODPackage.InterfaceNotImplemented()
		try:
			return self._SdoConfig
		except:
			raise SDOPackage.InternalError("get_configuration()")
		return SDOPackage.Configuration._nil


	def get_monitoring(self):
		"""
		\if jp

		\brief [CORBA interface] Monitoring ���֥������Ȥμ��� 

		���Υ��ڥ졼������ Monitoring interface �ؤλ��Ȥ��֤���
		Monitoring interface �� SDO ���������륤�󥿡��ե������ΰ�ĤǤ��롣
		���Υ��󥿡��ե������� SDO �Υץ�ѥƥ����˥���󥰤��뤿���
		���Ѥ���롣
		Monitoring interface �ξܺ٤ˤĤ��Ƥ� OMG SDO specification ��
		2.3.7�� "Monitoring Interface" p.2-35 �򻲾ȤΤ��ȡ�

		\return SDO �� Monitoring interface �ؤλ���
		\exception InterfaceNotImplemented SDO��Configuration���󥿡��ե�������
			�����ʤ���
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������

		\else

		\brief [CORBA interface] Get Monitoring object

		This operation returns an object implementing the Monitoring interface.
		The Monitoring interface is one of the interfaces that each SDO
		maintains. The interface is used to monitor the properties of an SDO.
		See OMG SDO specification Section 2.3.7, "Monitoring Interface," on
		page 2-35 for more details about the Monitoring interface.

		\return The Monitoring interface of an SDO.
		\exception InterfaceNotImplemented The target SDO has no Configuration
			interface.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		raise SDOPackage.InterfaceNotImplemented("Exception: get_monitoring")
		return SDOPackage.Monitoring._nil


	def get_organizations(self):
		"""
		\if jp

		\brief [CORBA interface] Organization �ꥹ�Ȥμ��� 

		SDO ��0�İʾ�� Organization (�ȿ�)�˽�°���뤳�Ȥ��Ǥ��롣 �⤷ SDO ��
		1�İʾ�� Organization �˽�°���Ƥ����硢���Υ��ڥ졼�����Ͻ�°����
		Organization �Υꥹ�Ȥ��֤���SDO �� �ɤ� Organization �ˤ��°���Ƥ��ʤ�
		���ˤϡ����Υꥹ�Ȥ��֤���롣

		\return SDO ����°���� Organization �Υꥹ�ȡ�
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Getting Organizations

		An SDO belongs to zero or more organizations. If the SDO belongs to one
		or more organizations, this operation returns the list of organizations
		that the SDO belongs to. An empty list is returned if the SDO does not
		belong to any Organizations.

		\return The list of Organizations that the SDO belong to.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.
		\endif
		"""
		try:
			return self._sdoOrganizations
		except:
			raise SDOPackage.InternalError("get_organizations()")
		return []


	def get_status_list(self):
		"""
		\if jp

		\brief [CORBA interface] SDO Status �ꥹ�Ȥμ��� 

		���Υ��ڥ졼������ SDO �Υ��ơ�������ɽ�� NVList ���֤���

		\return SDO �Υ��ơ�������
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InternalError ����Ū���顼��ȯ��������

		\else

		\brief [CORBA interface] Get SDO Status

		This operation returns an NVlist describing the status of an SDO.

		\return The actual status of an SDO.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.

		\endif
		"""
		try:
			return self._sdoStatus
		except:
			raise SDOPackage.InternalError("get_status_list()")
		return []


	def get_status(self, name):
		"""
		\if jp

		\brief [CORBA interface] SDO Status �μ��� 

		This operation returns the value of the specified status parameter.

		\param name(string) SDO �Υ��ơ��������������ѥ�᡼����
		\return ���ꤵ�줿�ѥ�᡼���Υ��ơ������͡�
		\exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���
		\exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
		\exception InvalidParameter ���� "name" �� null ���뤤��¸�ߤ��ʤ���
		\exception InternalError ����Ū���顼��ȯ��������
		\else

		\brief [CORBA interface] Get SDO Status

		\param name(string) One of the parameters defining the "status" of an SDO.
		\return The value of the specified status parameter.
		\exception SDONotExists The target SDO does not exist.
		\exception NotAvailable The target SDO is reachable but cannot respond.
		\exception InvalidParameter The parameter defined by "name" is null or
			does not exist.
		\exception InternalError The target SDO cannot execute the operation
			completely due to some internal error.


		\endif
		"""
		index = OpenRTM.CORBA_SeqUtil.find(self._sdoStatus, self.nv_name(name))
		if index < 0:
			raise SDOPackage.InvalidParameter("get_status(): Not found")

		try:
			return any.to_any(self._sdoStatus[index].value)
		except:
			raise SDOPackage.InternalError("get_status()")
		return any.to_any("")


    #============================================================
    # Local interfaces
    #============================================================
	def getInstanceName(self):
		return self._profile.instance_name

	
	def setInstanceName(self, instance_name):
		"""
		 \param instance_name(string)
		"""
		self._properties.setProperty("instance_name",instance_name)
		self._profile.instance_name = self._properties.getProperty("instance_name")

	
	def getTypeName(self):
		return self._profile.type_name

	
	def getDescription(self):
		return self._profile.description

	
	def getVersion(self):
		return self._profile.version

	
	def getVendor(self):
		return self._profile.vendor

	
	def getCategory(self):
		return self._profile.category


	def getNamingNames(self):
		return string.split(self._properties.getProperty("naming.names"), ",")

	
	def setObjRef(self, rtobj):
		"""
		 \param rtobj(RTC.RTObject)
		"""
		self._objref = rtobj
		return

	
	def getObjRef(self):
		return self._objref


	def setProperties(self, prop):
		"""
		\if jp

		\brief [local interface] RTC �Υץ�ѥƥ������ꤹ��

		RTC ���ݻ����٤��ץ�ѥƥ������ꤹ�롣Ϳ������ץ�ѥƥ��ϡ�
		ComponentProfile �������ꤵ���٤����������ʤ���Фʤ�ʤ���
		���Υ��ڥ졼�������̾� RTC ������������ݤ� Manager ����
		�ƤФ�뤳�Ȥ�տޤ��Ƥ��롣

		\param prop(OpenRTM.Properties) RTC �Υץ�ѥƥ�

		\else

		\brief [local interface] Set RTC property

		This operation sets the properties to the RTC. The given property
		values should include information for ComponentProfile.
		Generally, this operation is designed to be called from Manager, when
		RTC is initialized

		\param prop(OpenRTM.Properties) Property for RTC.

		\endif
		"""
		self._properties = self._properties.mergeProperties(prop)
		self._profile.instance_name = self._properties.getProperty("instance_name")
		self._profile.type_name     = self._properties.getProperty("type_name")
		self._profile.description   = self._properties.getProperty("description")
		self._profile.version       = self._properties.getProperty("version")
		self._profile.vendor        = self._properties.getProperty("vendor")
		self._profile.category      = self._properties.getProperty("category")


	def getProperties(self):
		"""
		\if jp

		\brief [local interface] RTC �Υץ�ѥƥ����������

		RTC ���ݻ����Ƥ���ץ�ѥƥ����֤���
		RTC���ץ�ѥƥ�������ʤ����϶��Υץ�ѥƥ����֤���롣

		\return RTC �Υץ�ѥƥ�

		\else

		\brief [local interface] Get RTC property

		This operation returns the properties of the RTC.
		Empty property would be returned, if RTC has no property.

		\return Property for RTC.

		\endif
		"""
		return self._properties


	def bindParameter(self, param_name, var,
					  def_val, trans=None):
		"""
		\brief
	    var �ϥꥹ�Ȥ��Ϥ�ɬ�פ����롣
		\param param_name(string) name of Parameter.
		\param var(variable) object.
		\param def_val(string) stirng of parameter.
		"""
		if trans == None:
			_trans = OpenRTM.stringTo
		else:
			_trans = trans
		self._configsets.bindParameter(param_name, var, def_val, _trans)
		return True


	def updateParameters(self, config_set):
		self._configsets.update(config_set)
		return


	def registerPort(self, port):
		"""
		\if jp

		\brief [local interface] Port ����Ͽ����

		RTC ���ݻ�����Port����Ͽ���롣
		Port �������饢��������ǽ�ˤ��뤿��ˤϡ����Υ��ڥ졼�����ˤ��
		��Ͽ����Ƥ��ʤ���Фʤ�ʤ�����Ͽ����� Port �Ϥ��� RTC �����ˤ�����
		PortProfile.name �ˤ����̤���롣�������äơ�Port �� RTC ��ˤ����ơ�
		��ˡ����� PortProfile.name ������ʤ���Фʤ�ʤ���
		��Ͽ���줿 Port ��������Ŭ�ڤ˥����ƥ��ֲ����줿�塢���λ��Ȥ�
		���֥������Ȼ��Ȥ��ꥹ�������¸����롣

		\param port(OpenRTM.PortBase) RTC ����Ͽ���� Port

		\else

		\brief [local interface] Register Port

		This operation registers a Port to be held by this RTC.
		In order to enable access to the Port from outside of RTC, the Port
		must be registered by this operation. The Port that is registered by
		this operation would be identified by PortProfile.name in the inside of
		RTC. Therefore, the Port should have unique PortProfile.name in the RTC.
		The registering Port would be activated properly, and the reference
		and the object reference would be stored in lists in RTC.

		\param port(OpenRTM.PortBase) Port which is registered in the RTC

		\endif
		"""
		self._portAdmin.registerPort(port)
		return


	def registerInPort(self, name, inport):
		"""
		 \param name(string)
		 \param inport(OpenRTM.InPort)
		"""
		port = OpenRTM.DataInPort(name, inport)
		self.registerPort(port)
		return


	def registerOutPort(self, name, outport):
		"""
		 \param name(string)
		 \param outport(OpenRTM.OutPort)
		"""
		port = OpenRTM.DataOutPort(name, outport)
		self.registerPort(port)
		return


	def deletePort(self, port):
		"""
		\if jp
		\brief [local interface] Port ����Ͽ��������

		RTC ���ݻ�����Port����Ͽ�������롣
		\param port(OpenRTM.PortBase) RTC ����Ͽ���� Port
		\else
		\brief [local interface] Register Port

		This operation registers a Port to be held by this RTC.
		In order to enable access to the Port from outside of RTC, the Port
		must be registered by this operation. The Port that is registered by
		this operation would be identified by PortProfile.name in the inside of
		RTC. Therefore, the Port should have unique PortProfile.name in the RTC.
		The registering Port would be activated properly, and the reference
		and the object reference would be stored in lists in RTC.
		\param port(OpenRTM.PortBase) Port which is registered in the RTC
		\endif
		"""
		self._portAdmin.deletePort(port)
		return


	def deletePortByName(self, port_name):
		"""
		 \param port_name(string)
		"""
		self._portAdmin.deletePortByName(port_name)
		return

	
	def finalizePorts(self):
		self._portAdmin.finalizePorts()
		return



	def shutdown(self):
		try:
			self.finalizePorts()
			self._poa.deactivate_object(self._poa.servant_to_id(self._SdoConfigImpl))
			self._poa.deactivate_object(self._poa.servant_to_id(self))
		except:
			traceback.print_exception(*sys.exc_info())

		if self._manager != None:
			self._manager.cleanupComponent(self)
			
		return



	class svc_name:
		"""
		\brief SDOService �Υץ�ե�����ꥹ�Ȥ���id�ǥ��������뤿���
		�ե��󥯥����饹
		"""
		def __init__(self, _id):
			self._id= _id

		def __call__(self, prof):
			return self._id == prof.id

    #------------------------------------------------------------
    # Functor
    #------------------------------------------------------------
	class nv_name:
		def __init__(self, _name):
			self._name = _name

		def __call__(self, nv):
			return self._name == nv.name


	class ec_copy:
		def __init__(self, eclist):
			self._eclist = eclist

		def __call__(self, ecs):
			self._eclist.append(ecs)


	class deactivate_comps:
		def __init__(self, comp):
			self._comp = comp

		def __call__(self, ec):
			ec.deactivate_component(self._comp)


# RtcBase = RTObject_impl
