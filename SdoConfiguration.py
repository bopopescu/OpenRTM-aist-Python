#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file SdoConfiguration.py
# @brief RT component base class
# @date $Date: 2007/09/06$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import copy
import threading

import OpenRTM
##
# @if jp
# @namespace SDOPackage
#
# @brief SDO �ѥå�����
#
# @else
#
# @namespace SDOPackage
#
# @endif
import SDOPackage, SDOPackage__POA


##
# @if jp
# @class ScopedLock
# @brief ScopedLock ���饹
#
# ��¾�����ѥ��å����饹��
#
# @since 0.4.0
#
# @else
#
# @endif
class ScopedLock:
  def __init__(self, mutex):
    self.mutex = mutex
    self.mutex.acquire()

  def __del__(self):
    self.mutex.release()


# SdoConfiguration with SeqEx 159120
# SdoConfiguration with SeqUtil 114504 114224


##
# @if jp
# 
# @brief NVList �� Properties �إ��ԡ�����
# 
# ���Υ��ڥ졼������ NVList �� Properties �إ��ԡ����롣
# 
# @param prop NVList ���ͤ��Ǽ���� Properties
# @param nv ���ԡ����� NVList
# 
# @else
# 
# @brief Copy to Proeprties from NVList
# 
# This operation copies NVList to Properties.
# 
# @param prop Properties to store NVList values
# @param nv NVList that is copies from
# 
# @endif
def toProperties(prop, conf):
  OpenRTM.NVUtil.copyToProperties(prop, conf.configuration_data)


##
# @if jp
# 
# @brief Properties �� NVList �إ��ԡ�����
# 
# ���Υ��ڥ졼������ Properties �� NVList �إ��ԡ����롣
# NVList �� value ������ CORBA::string ���Ȥ��ƥ��ԡ����롣
# 
# @param nv Properties ���ͤ��Ǽ���� NVList
# @param prop ���ԡ����� Properties
# 
# @else
# 
# @brief Copy to NVList from Proeprties
# 
# This operation copies Properties to NVList.
# Created NVList's values are CORBA::string.
# 
# @param nv NVList to store Properties values
# @param prop Properties that is copies from
# 
# @endif
def toConfigurationSet(conf, prop):
  conf.description = prop.getProperty("description")
  conf.id = prop.getName()
  OpenRTM.NVUtil.copyFromProperties(conf.configuration_data, prop)



##
# @if jp
#
# @class Configuration_impl
# @brief SDO Configuration �������饹
#
# Configuration interface �� Resource Data Model ��������줿�ǡ�����
# �ɲá������������Ԥ�����Υ��󥿡��ե������Ǥ��롣
# DeviceProfile, ServiceProfile, ConfigurationProfile ����� Organization
# ���ѹ���Ԥ�����Υ��ڥ졼�����������Ƥ��롣SDO �λ��ͤǤϥ�����������
# ����ӥ������ƥ��˴ؤ���ܺ٤ˤĤ��Ƥϵ��ꤷ�Ƥ��ʤ���
# 
# ʣ�������� (Configuration) ���ݻ����뤳�Ȥˤ�ꡢ�ưפ������᤯��������
# ��ȿ�Ǥ����뤳�Ȥ��Ǥ��롣������������줿ʣ��������� ConfigurationSets
# ����� configuration profile �Ȥ����ݻ����뤳�Ȥ��Ǥ��롣�ҤȤĤ�
# ConfigurationSet �����������˴�Ϣ�դ���줿���ץ��ѥƥ��ͤΥꥹ�Ȥ�
# ��ˡ���ID���ܺ٤ȤȤ�˻��äƤ��롣����ˤ�ꡢ��������ܤξܺ٤򵭽Ҥ�
# ���̤��뤳�Ȥ��Ǥ��롣Configuration interface �Υ��ڥ졼�����Ϥ����
# ConfiguratioinSets �δ�����ٱ礹�롣
#
#
# - ConfigurationSet: id, description, NVList ���鹽�������1���åȤ�����
# - ConfigurationSetList: ConfigurationSet �Υꥹ��
# - Parameter: name, type, allowed_values ���鹽�������ѥ�᡼�������
# - ActiveConfigurationSet: ����ͭ���ʥ���ե�����졼������1���åȡ�
#
# �ʲ���SDO���ͤ���������Ƥ��ʤ��⤷���ϲ�᤬�狼��ʤ������ȼ����
#
# �ʲ��δؿ��� ParameterList ���Ф��ƽ�����Ԥ���
# - get_configuration_parameters()
#
# �ʲ��δؿ��ϥ����ƥ��֤�ConfigurationSet���Ф��������Ԥ�
# - get_configuration_parameter_values()
# - get_configuration_parameter_value()
# - set_configuration_parameter()
#
# �ʲ��δؿ���ConfigurationSetList���Ф��ƽ�����Ԥ�
# - get_configuration_sets()
# - get_configuration_set()
# - set_configuration_set_values()
# - get_active_configuration_set()
# - add_configuration_set()
# - remove_configuration_set()
# - activate_configuration_set()
#
# @since 0.4.0
#
# @else
#
# @class Configuration_impl
# @brief Configuration implementation class
#
# Configuration interface provides operations to add or remove data
# specified in resource data model. These operations provide functions to
# change DeviceProfile, ServiceProfile, ConfigurationProfile, and
# Organization. This specification does not address access control or
# security aspects. Access to operations that modifies or removes profiles
# should be controlled depending upon the application.
#
# Different configurations can be stored for simple and quick activation.
# Different predefined configurations are stored as different
# ConfigurationSets or configuration profile. A ConfigurationSet stores the
# value of all properties assigned for the particular configuration along
# with its unique id and description to identify and describe the
# configuration respectively. Operations in the configuration interface
# help manage these ConfigurationSets.
#
# @since 0.4.0
#
# @endif
class Configuration_impl(SDOPackage__POA.Configuration):



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param configsets ConfigurationSetList
  # 
  # @else
  #
  # @endif
  def __init__(self, configsets):
    """
     \var self._deviceProfile SDO DeviceProfile with mutex lock
    """
    self._deviceProfile = None
    self._dprofile_mutex = threading.RLock()

    """
     \var self._serviceProfiles SDO ServiceProfileList
    """
    self._serviceProfiles = []
    self._sprofile_mutex = threading.RLock()

    self._parameters = []
    self._params_mutex = threading.RLock()

    self._configsets = configsets
    self._config_mutex = threading.RLock()

    """
     \var self._organizations SDO OrganizationList
    """
    self._organizations = []
    self._org_mutex = threading.RLock()

    self._objref = self._this()


  #============================================================
  #
  # <<< CORBA interfaces >>>
  #
  #============================================================

  ##
  # @if jp
  # 
  # @brief [CORBA interface] SDO �� DeviceProfile �Υ��å�
  #
  # ���Υ��ڥ졼������ SDO �� DeviceProfile �򥻥åȤ��롣SDO ��
  # DeviceProfile ���ݻ����Ƥ��ʤ����Ͽ����� DeviceProfile ����������
  # DeviceProfile �򤹤Ǥ��ݻ����Ƥ�����ϴ�¸�Τ�Τ��֤������롣
  #
  # @param self
  # @param dProfile SDO �˴�Ϣ�դ����� DeviceProfile��
  #
  # @return ���ڥ졼����������������ɤ������֤���
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InvalidParameter ���� "dProfile" �� null �Ǥ��롣
  # @exception InternalError ����Ū���顼��ȯ��������
  # 
  # @else
  #
  # @brief [CORBA interface] Set DeviceProfile of SDO
  #
  # This operation sets the DeviceProfile of an SDO. If the SDO does not
  # have DeviceProfile, the operation will create a new DeviceProfile,
  # otherwise it will replace the existing DeviceProfile.
  #
  # @param dProfile The device profile that is to be assigned to this SDO.
  #
  # @return If the operation was successfully completed.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InvalidParameter The argument "dProfile" is null.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def set_device_profile(self, dProfile):
    if dProfile is None:
      raise SDOPackage.InvalidParameter("dProfile is empty.")

    try:
      guard = ScopedLock(self._dprofile_mutex)
      self._deviceProfile = dProfile
    except:
      raise SDOPackage.InternalError("Unknown Error")

    return True


  ##
  # @if jp
  # 
  # @brief [CORBA interface] SDO �� ServiceProfile �Υ��å�
  #
  # ���Υ��ڥ졼�����Ϥ��� Configuration interface ���ͭ�����о� SDO ��
  # ServiceProfile ���ɲä��롣�⤷������ ServiceProfile �� id �����Ǥ����
  # ������ ID ���������줽�� ServiceProfile ���Ǽ���롣�⤷ id ������
  # �ʤ���С�SDO ��Ʊ�� id ����� ServiceProfile �򸡺����롣
  # Ʊ�� id ��¸�ߤ��ʤ���Ф��� ServiceProfile ���ɲä���id ��¸�ߤ����
  # ��񤭤򤹤롣<br>
  # (���ա��ǿ��С������Ǥϥ��ڥ졼�����̾��add_service_profile�ѹ�)
  #
  # @param self
  # @param sProfile �ɲä��� ServiceProfile
  #
  # @return ���ڥ졼����������������ɤ������֤���
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "sProfile" �� null�Ǥ��롣
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Set SDO's ServiceProfile
  #
  # This operation adds ServiceProfile to the target SDO that navigates this
  # Configuration interface. If the id in argument ServiceProfile is null,
  # new id is created and the ServiceProfile is stored. If the id is not
  # null, the target SDO searches for ServiceProfile in it with the same id.
  # It adds the ServiceProfile if not exist, or overwrites if exist.
  #
  # @param sProfile ServiceProfile to be added.
  #
  # @return If the operation was successfully completed.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InvalidParameter The argument "sProfile" is null.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def set_service_profile(self, sProfile):
    if sProfile is None:
      raise SDOPackage.InvalidParameter("sProfile is empty.")

    try:
      if sProfile.id is None:
        prof = sProfile
        prof.id = self.getUUID()
        OpenRTM.CORBA_SeqUtil.push_back(self._serviceProfiles, prof)
        return True

      index = OpenRTM.CORBA_SeqUtil.find(self._serviceProfiles,
                         self.service_id(sProfile.id))
      if index >= 0:
        OpenRTM.CORBA_SeqUtil.erase(self._serviceProfiles, index)

      OpenRTM.CORBA_SeqUtil.push_back(self._serviceProfiles, sProfile)
      return True
    except:
      raise SDOPackage.InternalError("Configuration.set_service_profile")

    return True


  ##
  # @if jp
  # 
  # @brief [CORBA interface] Organization ���ɲ�
  #
  # ���Υ��ڥ졼������ Organization object �Υ�ե���󥹤��ɲä��롣
  #
  # @param self
  # @param org �ɲä��� Organization
  #
  # @return ���ڥ졼����������������ɤ������֤���
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InvalidParameter ���� "organization" �� null �Ǥ��롣
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Add Organization
  #
  # This operation adds reference of an Organization object.
  #
  # @param org Organization to be added.
  #
  # @return If the operation was successfully completed.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InvalidParameter The argument ��organization�� is null.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def add_organization(self, org):
    if org is None:
      raise SDOPackage.InvalidParameter("org is empty.")

    try:
      OpenRTM.CORBA_SeqUtil.push_back(self._organizations, org)
    except:
      raise SDOPackage.InternalError("Configuration.add_organization")

    return True


  ##
  # @if jp
  # 
  # @brief [CORBA interface] ServiceProfile �κ��
  #
  # ���Υ��ڥ졼�����Ϥ��� Configuration interface ����� SDO ��
  # Service �� ServiceProfile �������롣������� ServiceProfile
  # �ϰ����ˤ����ꤵ��롣
  #
  # @param self
  # @param id_ ������� ServcieProfile �� serviceID��
  #
  # @return ���ڥ졼����������������ɤ������֤���
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "id" �� null �Ǥ��롣�⤷���� "id" ��
  #            ��Ϣ�դ���줿 ServiceProfile ��¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Remove ServiceProfile
  #
  # This operation removes ServiceProfile object to the SDO that has this
  # Configuration interface. The ServiceProfile object to be removed is
  # specified by argument.
  #
  # @param id_ serviceID of a ServiceProfile to be removed.
  #
  # @return If the operation was successfully completed.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception InvalidParameter The argument "sProfile" is null, or if the
  #          object that is specified by argument "sProfile" does not exist.
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def remove_service_profile(self, id_):
    if id_ is None:
      raise SDOPackage.InvalidParameter("id is empty.")

    try:
      OpenRTM.CORBA_SeqUtil.erase_if(self._serviceProfiles, self.service_id(id_))
    except:
      raise SDOPackage.InternalError("Configuration.remove_service_profile")

    return True


  ##
  # @if jp
  # 
  # @brief [CORBA interface] Organization �λ��Ȥκ��
  #
  # ���Υ��ڥ졼������ Organization �λ��Ȥ������롣
  #
  # @param self
  # @param organization_id ������� Organization �ΰ�դ� id��
  #
  # @return ���ڥ졼����������������ɤ������֤���
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "organization_id" �� null �Ǥ��롣
  #            �⤷���� "organization_id" �˴�Ϣ�դ���줿 
  #            OrganizationProfile ��¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Remove the reference of Organization 
  #
  # This operation removes the reference of an Organization object.
  #
  # @param organization_id Unique id of the organization to be removed.
  #
  # @return If the operation was successfully completed.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception InvalidParameter The argument "organizationID" is null,
  #            or the object which is specified by argument "organizationID"
  #            does not exist.
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def remove_organization(self, organization_id):
    if organization_id is None:
      raise SDOPackage.InvalidParameter("organization_id is empty.")

    try:
      guard = ScopedLock(self._org_mutex)
      OpenRTM.CORBA_SeqUtil.erase_if(self._organizations,
                       self.org_id(organization_id))
    except:
      raise SDOPackage.InternalError("Configuration.remove_organization")

    return True


  ##
  # @if jp
  # 
  # @brief [CORBA interface] ����ѥ�᡼���Υꥹ�Ȥμ���
  #
  # ���Υ��ڥ졼������ configuration parameter �Υꥹ�Ȥ��֤���
  # SDO �������ǽ�ʥѥ�᡼��������ʤ���ж��Υꥹ�Ȥ��֤���
  #
  # @param self
  #
  # @return �������ħ�դ���ѥ�᡼������Υꥹ�ȡ�
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Getting a list of configuration parameter
  #
  # This operation returns a list of Parameters. An empty list is returned
  # if the SDO does not have any configurable parameter.
  #
  # @return The list with definitions of parameters characterizing the
  #          configuration.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_configuration_parameters(self):
    try:
      guard = ScopedLock(self._params_mutex)
      param = copy.copy(self._parameters)
      return param
    except:
      raise SDOPackage.InternalError("Configuration.get_configuration_parameters")

    return []


  ##
  # @if jp
  # 
  # @brief [CORBA interface] Configuration parameter ���ͤΥꥹ�Ȥμ���
  #
  # ���Υ��ڥ졼���������Ƥ� configuration �ѥ�᡼��������ͤ��֤���<br>
  # ���ܼ����ǤϾ�˶��Υꥹ�Ȥ��֤�
  #
  # @param self
  #
  # @return ���Ƥ� configuration �ѥ�᡼�����ͤΥꥹ�ȡ�
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Getting value list of configuration parameter
  #
  # This operation returns all configuration parameters and their values.
  #
  # @return List of all configuration parameters and their values.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_configuration_parameter_values(self):
    guard = ScopedLock(self._config_mutex)
    nvlist = []
    return nvlist


  ##
  # @if jp
  # 
  # @brief [CORBA interface] Configuration parameter ���ͤμ���
  #
  # ���Υ��ڥ졼�����ϰ��� "name" �ǻ��ꤵ�줿�ѥ�᡼���ͤ��֤���<br>
  # ���ܼ����ǤϾ�� None ���֤�
  #
  # @param self
  # @param name �ͤ��׵᤹��ѥ�᡼����̾����
  #
  # @return ���ꤵ�줿�ѥ�᡼�����͡�
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "name" �� null �Ǥ��롣
  #            �⤷���� "name" �˴�Ϣ�դ���줿�ѥ�᡼����¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Getting value of configuration parameter
  #
  # This operation returns a value of parameter that is specified by
  # argument "name."
  #
  # @param Name of the parameter whose value is requested.
  #
  # @return The value of the specified parameter.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception InvalidParameter if the value of the argument "name" is
  #                             empty String, or null, or if the parameter
  #                             that is specified by argument "name"
  #                             does not exist.
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_configuration_parameter_value(self, name):
    if name is None:
      raise SDOPackage.InvalidParameter("Name is empty.")

    return None


  ##
  # @if jp
  # 
  # @brief [CORBA interface] Configuration �ѥ�᡼�����ѹ�
  #
  # ���Υ��ڥ졼������ "name" �ǻ��ꤷ���ѥ�᡼�����ͤ� "value" ��
  # �ѹ����롣<br>
  # ���ܼ����ǤϾ��True���֤�
  #
  # @param self
  # @param name �ѹ��оݥѥ�᡼����̾����
  # @param value �ѹ��оݥѥ�᡼���ο������͡�
  #
  # @return ���ڥ졼����������������ɤ������֤���
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ����( "name"�⤷����"value") �� null �Ǥ��롣
  #            �⤷���� "name" �˴�Ϣ�դ���줿�ѥ�᡼����¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Modify the parameter value
  #
  # This operation sets a parameter to a value that is specified by argument
  # "value." The parameter to be modified is specified by argument " name."
  #
  # @param name The name of parameter to be modified.
  # @param value New value of the specified parameter.
  #
  # @return If the operation was successfully completed.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception InvalidParameter if arguments ("name" and/or "value") is
  #            null, or if the parameter that is specified by the argument
  #            "name" does not exist.
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def set_configuration_parameter(self, name, value):
    if name is None or value is None:
      raise SDOPackage.InvalidParameter("Name/Value is empty.")
    return True


  ##
  # @if jp
  # 
  # @brief [CORBA interface] ConfigurationSet �ꥹ�Ȥμ��� 
  #
  # ���Υ��ڥ졼������ ConfigurationProfile ������ ConfigurationSet ��
  # �ꥹ�Ȥ��֤��� SDO �� ConfigurationSet ������ʤ���ж��Υꥹ�Ȥ��֤���
  #
  # @param self
  #
  # @return �ݻ����Ƥ��� ConfigurationSet �Υꥹ�Ȥθ����͡�
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Getting list of ConfigurationSet
  #
  # This operation returns a list of ConfigurationSets that the
  # ConfigurationProfile has. An empty list is returned if the SDO does not
  # have any ConfigurationSets.
  # This operation returns a list of all ConfigurationSets of the SDO.
  # If no predefined ConfigurationSets exist, then empty list is returned.
  #
  # @return The list of stored configuration with their current values.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_configuration_sets(self):
    try:
      guard = ScopedLock(self._config_mutex)

      cf = self._configsets.getConfigurationSets()
      len_ = len(cf)

      config_sets = [SDOPackage.ConfigurationSet("","",[]) for i in range(len_)]
      for i in range(len_):
        toConfigurationSet(config_sets[i], cf[i])

      return config_sets

    except:
      raise SDOPackage.InternalError("Configuration.get_configuration_sets")

    return []

  ##
  # @if jp
  # 
  # @brief [CORBA interface] ConfigurationSet �μ���
  #
  # ���Υ��ڥ졼�����ϰ����ǻ��ꤵ�줿 ConfigurationSet �� ID �˴�Ϣ
  # �դ���줿 ConfigurationSet ���֤���
  #
  # @param self
  # @param config_id ConfigurationSet �μ��̻ҡ�
  #
  # @return �����ˤ����ꤵ�줿 ConfigurationSet��
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter "config_id" �� null �������ꤵ�줿
  #            ConfigurationSet ��¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Getting a ConfigurationSet
  #
  # This operation returns the ConfigurationSet specified by the parameter
  # configurationSetID.
  #
  # @param config_id Identifier of ConfigurationSet requested.
  #
  # @return The configuration set specified by the parameter config_id.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception InvalidParameter If the parameter 'config_id' is null
  #            or if there are no ConfigurationSets stored with such id.
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_configuration_set(self, config_id):
    if config_id is None:
      raise SDOPackage.InvalidParameter("ID is empty")

    guard = ScopedLock(self._config_mutex)

    if not self._configsets.haveConfig(config_id):
      raise SDOPackage.InvalidParameter("No such ConfigurationSet")

    configset = self._configsets.getConfigurationSet(config_id)

    try:
      config = SDOPackage.ConfigurationSet("","",[])
      toConfigurationSet(config, configset)
      return config
    except:
      raise SDOPackage.InvalidError("Configuration::get_configuration_set()")

    return SDOPackage.ConfigurationSet("","",[])


  ##
  # @if jp
  # 
  # @brief [CORBA interface] ConfigurationSet �򥻥åȤ���
  #
  # ���Υ��ڥ졼�����ϻ��ꤵ�줿 id �� ConfigurationSet �򹹿����롣
  #
  # @param self
  # @param config_id �ѹ����� ConfigurationSet �� ID��
  # @param configuration_set �ѹ����� ConfigurationSet ���Τ�Ρ�
  #
  # @return ConfigurationSet ������˹����Ǥ������� true��
  #         �����Ǥʤ���� false ���֤���
  #
  # @exception InvalidParameter config_id �� null ����
  #            ���ꤵ�줿 id �ǳ�Ǽ���줿 ConfigurationSet��¸�ߤ��ʤ�����
  #            ���ꤵ�줿 configuration_set���°���Σ��Ĥ�������
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Set ConfigurationSet
  #
  # This operation modifies the specified ConfigurationSet of an SDO.
  #
  # �� �ѥ�᡼���ο��� spec �� IDL �ǰۤʤ롪����
  # @param configu_id The ID of ConfigurationSet to be modified.
  # @param configuration_set ConfigurationSet to be replaced.
  #
  # @return A flag indicating if the ConfigurationSet was modified 
  #         successfully. "true" - The ConfigurationSet was modified
  #         successfully. "false" - The ConfigurationSet could not be
  #         modified successfully.
  #
  # @exception InvalidParameter if the parameter 'configurationSetID' is
  #            null or if there is no ConfigurationSet stored with such id.
  #            This exception is also raised if one of the attributes
  #            defining ConfigurationSet is not valid.
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def set_configuration_set_values(self, config_id, configuration_set):
    if config_id is None:
      raise SDOPackage.InvalidParameter("ID is empty.")

    try:
      conf = OpenRTM.Properties(key=config_id)
      toProperties(conf, configuration_set)
      return self._configsets.setConfigurationSetValues(config_id, conf)
    except:
      raise SDOPackage.InvalidError("Configuration::set_configuration_set_values()")

    return True


  ##
  # @if jp
  # 
  # @brief [CORBA interface] �����ƥ��֤� ConfigurationSet ���������
  #
  # ���Υ��ڥ졼����������SDO�θ��ߥ����ƥ��֤� ConfigurationSet ���֤���
  # (�⤷SDO�θ��ߤ����꤬ͽ��������줿 ConfigurationSet �ˤ�����ꤵ���
  # ����ʤ�С�)
  # ConfigurationSet �ϰʲ��ξ��ˤϥ����ƥ��֤ǤϤʤ���ΤȤߤʤ���롣
  #
  # - ���ߤ����꤬ͽ��������줿 ConfigurationSet �ˤ�ꥻ�åȤ���Ƥ��ʤ���
  # - SDO �����꤬�����ƥ��֤ˤʤä�����ѹ����줿��
  # - SDO �����ꤹ�� ConfigurationSet ���ѹ����줿��
  # 
  # �����ξ��ˤϡ����� ConfigurationSet ���֤���롣
  #
  # @param self
  #
  # @return ���ߥ����ƥ��֤� ConfigurationSet��
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Get active ConfigurationSet
  #
  # This operation returns the current active ConfigurationSet of an
  # SDO (i.e., if the current configuration of the SDO was set using
  # predefined configuration set).
  # ConfigurationSet cannot be considered active if the:
  #
  # - current configuration of the SDO was not set using any predefined
  #   ConfigurationSet, or
  # - configuration of the SDO was changed after it has been active, or
  # - ConfigurationSet that was used to configure the SDO was modified.
  #
  # Empty ConfigurationSet is returned in these cases.
  #
  # @return The active ConfigurationSet.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_active_configuration_set(self):
    if not self._configsets.isActive():
      raise SDOPackage.NotAvailable()

    try:
      guard = ScopedLock(self._config_mutex)
      config = SDOPackage.ConfigurationSet("","",[])
      toConfigurationSet(config, self._configsets.getActiveConfigurationSet())
      return config
    except:
      raise SDOPackage.InternalError("Configuration.get_active_configuration_set()")

    return SDOPackage.ConfigurationSet("","",[])


  ##
  # @if jp
  # 
  # @brief [CORBA interface] ConfigurationSet ���ɲä���
  #
  # ConfigurationProfile �� ConfigurationSet ���ɲä��륪�ڥ졼�����
  #
  # @param self
  # @param configuration_set �ɲä��� ConfigurationSet��
  #
  # @return ���ڥ졼����������������ɤ�����
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter "configurationSet" �� null ����
  #            "configurationSet"��������줿°���Σ��Ĥ���������
  #            ���ꤵ�줿 configurationSet ��ID������¸�ߤ��롣
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Add ConfigurationSet
  #
  # This operation adds a ConfigurationSet to the ConfigurationProfile.
  #
  # @param configuration_set The ConfigurationSet that is added.
  #
  # @return If the operation was successfully completed.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception InvalidParameter If the argument "configurationSet" is null,
  #            or if one of the attributes defining "configurationSet" is
  #            invalid, or if the specified identifier of the configuration
  #            set already exists.
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def add_configuration_set(self, configuration_set):
    if configuration_set is None:
      raise SDOPackage.InvalidParameter("configuration_set is empty.")

    try:
      guard = ScopedLock(self._config_mutex)
      config_id = configuration_set.id
      config = OpenRTM.Properties(key=config_id)
      toProperties(config, configuration_set)
      return self._configsets.addConfigurationSet(config)
    except:
      raise SDOPackage.InternalError("Configuration::add_configuration_set()")

    return True


  ##
  # @if jp
  # 
  # @brief [CORBA interface] ConfigurationSet ��������
  #
  # ConfigurationProfile ���� ConfigurationSet �������롣
  #
  # @param self
  # @param config_id ������� ConfigurationSet �� id��
  #
  # @return ���ڥ졼����������������ɤ�����
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "configurationSetID" �� null �Ǥ��롢
  #            �⤷���ϡ������ǻ��ꤵ�줿 ConfigurationSet ��¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Remove ConfigurationSet
  #
  # This operation removes a ConfigurationSet from the ConfigurationProfile.
  #
  # @param config_id The id of ConfigurationSet which is removed.
  #
  # @return If the operation was successfully completed.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception InvalidParameter The arguments "configurationSetID" is null,
  #            or if the object specified by the argument
  #            "configurationSetID" does not exist.
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def remove_configuration_set(self, config_id):
    if config_id is None:
      raise SDOPackage.InvalidParameter("ID is empty.")
      
    try:
      guard = ScopedLock(self._config_mutex)
      return self._configsets.removeConfigurationSet(config_id)
    except:
      raise SDOPackage.InvalidError("Configuration.remove_configuration_set()")

    return False


  ##
  # @if jp
  # 
  # @brief [CORBA interface] ConfigurationSet �Υ����ƥ��ֲ�
  #
  # ConfigurationProfile �˳�Ǽ���줿 ConfigurationSet �Τ�����Ĥ�
  # �����ƥ��֤ˤ��롣
  # ���Υ��ڥ졼����������� ConfigurationSet �򥢥��ƥ��֤ˤ��롣
  # ���ʤ����SDO �Υ���ե�����졼����󡦥ץ��ѥƥ������γ�Ǽ����Ƥ���
  # ConfigurationSet �ˤ�����ꤵ���ץ��ѥƥ����ͤ��ѹ�����롣
  # ���ꤵ�줿 ConfigurationSet ���ͤ������ƥ��֡�����ե�����졼�����
  # �˥��ԡ������Ȥ������Ȥ��̣���롣
  #
  # @param self
  # @param config_id �����ƥ��ֲ����� ConfigurationSet �� id��
  #
  # @return ���ڥ졼����������������ɤ�����
  #
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "config_id" �� null �Ǥ��롢�⤷����
  #            �����ǻ��ꤵ�줿 ConfigurationSet ��¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  #
  # @brief [CORBA interface] Activate ConfigurationSet
  #
  # This operation activates one of the stored ConfigurationSets in the
  # ConfigurationProfile.
  # This operation activates the specified stored ConfigurationSets.
  # This means that the configuration properties of the SDO are changed as
  # the values of these properties specified in the stored ConfigurationSet.
  # In other words, values of the specified ConfigurationSet are now copied
  # to the active configuration.
  #
  # @param Identifier of ConfigurationSet to be activated.
  #
  # @return If the operation was successfully completed.
  #
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception InvalidParameter if the argument ("configID") is null or
  #            there is no configuration set with identifier specified by
  #            the argument.
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def activate_configuration_set(self, config_id):
    if config_id is None:
      raise SDOPackage.InvalidParameter("ID is empty.")
      
    try:
      return self._configsets.activateConfigurationSet(config_id)
    except:
      raise SDOPackage.InvalidError("Configuration.activate_configuration_set()")

    return False


  #============================================================
  # end of CORBA interface definition
  #============================================================

  ##
  # @if jp
  #
  # @brief ���֥������ȡ���ե���󥹤��������
  # 
  # �оݤΥ��֥������ȥ�ե���󥹤��������
  #
  # @param self
  # 
  # @return ���֥������ȥ�ե����
  # 
  # @else
  #
  # @endif
  def getObjRef(self):
    return self._objref


  ##
  # @if jp
  #
  # @brief SDO �� DeviceProfile ���������
  # 
  # SDO �� DeviceProfile ���������
  #
  # @param self
  # 
  # @return SDO �� DeviceProfile
  # 
  # @else
  #
  # @endif
  def getDeviceProfile(self):
    return self._deviceProfile


  ##
  # @if jp
  #
  # @brief SDO �� ServiceProfile �Υꥹ�Ȥ��������
  # 
  # SDO �� ServiceProfile �Υꥹ�Ȥ��������
  #
  # @param self
  # 
  # @return SDO ServiceProfile�ꥹ��
  # 
  # @else
  #
  # @endif
  def getServiceProfiles(self):
    return self._serviceProfiles


  ##
  # @if jp
  #
  # @brief SDO �� ServiceProfile ���������
  # 
  # ���Υ��ڥ졼�����ϰ��� "id" �ǻ��ꤵ�줿SDO �� ServiceProfile���֤���
  # "id" �ǻ��ꤵ�줿 ServiceProfile��¸�ߤ��ʤ���硢
  # ServiceProfile�Υ��󥹥��󥹤��������֤���
  # 
  # @param self
  # @param id ServiceProfile �μ��̻ҡ�
  # 
  # @return ���ꤵ�줿 SDO ServiceProfile
  # 
  # @else
  #
  # @endif
  def getServiceProfile(self, id):
    index = OpenRTM.CORBA_SeqUtil.find(self._serviceProfiles,
                       self.service_id(id))

    if index < 0:
      return SDOPackage.ServiceProfile("","",[],None)

    return self._serviceProfiles[index]


  ##
  # @if jp
  #
  # @brief SDO �� Organization �ꥹ�Ȥ��������
  # 
  # SDO �� Organization �ꥹ�Ȥ��������
  # 
  # @param self
  # 
  # @return SDO �� Organization �ꥹ��
  # 
  # @else
  #
  # @endif
  def getOrganizations(self):
    return self._organizations


  ##
  # @if jp
  #
  # @brief UUID����������
  # 
  # UUID����������
  # 
  # @param self
  # 
  # @return ��������UUID
  # 
  # @else
  #
  # @endif
  def getUUID(self):
    return OpenRTM.uuid1()


  # functor for ServiceProfile
  ##
  # @if jp
  # @class service_id
  # @brief  ServiceProfile��functor
  # @else
  # @brief  functor for ServiceProfile
  # @endif
  class service_id:
    def __init__(self, id_):
      self._id = str(id_)

    def __call__(self, s):
      id_ = str(s.id)
      return self._id == id_


  # functor for Organization
  ##
  # @if jp
  # @class org_id
  # @brief  Organization��functor
  # @else
  # @brief  functor for Organization
  # @endif
  class org_id:
    def __init__(self, id_):
      self._id = str(id_)

    def __call__(self, o):
      id_ = str(o.get_organization_id())
      return self._id == id_

    
  # functor for ConfigurationSet
  ##
  # @if jp
  # @class config_id
  # @brief  ConfigurationSet��functor
  # @else
  # @brief  functor for ConfigurationSet
  # @endif
  class config_id:
    def __init__(self, id_):
      self._id = str(id_)

    def __call__(self, c):
      id_ = str(c.id)
      return self._id == id_