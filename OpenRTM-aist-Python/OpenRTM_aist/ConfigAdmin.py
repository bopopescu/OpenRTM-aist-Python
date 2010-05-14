#!/usr/bin/env python
# -*- coding: euc-jp -*- 

##
# @file ConfigAdmin.py
# @brief Configuration Administration classes
# @date $Date: 2007/09/04$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2007-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



import copy
import OpenRTM_aist


class OnUpdateCallback:
  def __init__(self):
    pass


  def __call__(self, config_set):
    pass



class OnUpdateParamCallback:
  def __init__(self):
    pass


  def __call__(self, config_set, config_param):
    pass



class OnSetConfigurationSetCallback:
  def __init__(self):
    pass


  def __call__(self, config_set):
    pass



class OnAddConfigurationAddCallback:
  def __init__(self):
    pass


  def __call__(self, config_set):
    pass



class OnRemoveConfigurationSetCallback:
  def __init__(self):
    pass


  def __call__(self, config_set):
    pass



class OnActivateSetCallback:
  def __init__(self):
    pass


  def __call__(self, config_id):
    pass



##
# @if jp
# @class Config
# @brief Config ���饹
# 
# ����ե�����졼�����ѥ�᡼���ξ�����ݻ����륯�饹��
# ����ե�����졼�����Υǡ����������ꤵ�줿�ǡ�������ʸ������Ѵ�����
# �Ѵ��ؿ�����ꤹ�롣
# 
# @since 0.4.0
# 
# @else
# 
# @endif
class Config:
  """
  """

  ##
  # @if jp
  # 
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  # 
  # @param self 
  # @param name ����ե�����졼�����ѥ�᡼��̾
  # @param var ����ե�����졼�����ѥ�᡼����Ǽ���ѿ�
  # @param def_val ʸ��������Υǥե������
  # @param trans ʸ��������Ѵ��ؿ�(�ǥե������:None)
  # 
  # @else
  # 
  # @endif
  def __init__(self, name, var, def_val, trans=None):
    self.name = name
    self.default_value = def_val
    self._var = var
    if trans:
      self._trans = trans
    else:
      self._trans = OpenRTM_aist.stringTo


  ##
  # @if jp
  # 
  # @brief �Х���ɥѥ�᡼���ͤ򹹿�
  # 
  # ����ե�����졼����������ͤǥ���ե�����졼�����ѥ�᡼���򹹿�����
  # 
  # @param self 
  # @param val �ѥ�᡼���ͤ�ʸ����ɽ��
  # 
  # @return �����������(��������:true����������:false)
  # 
  # @else
  # 
  # @endif
  # virtual bool update(const char* val)
  def update(self, val):
    if self._trans(self._var, val):
      return True
    self._trans(self._var, self._default_value)
    return False



##
# @if jp
# @class ConfigAdmin
# @brief ConfigAdmin ���饹
# 
# �Ƽ拾��ե�����졼���������������륯�饹��
# 
# @since 0.4.0
# 
# @else
# 
# @endif
class ConfigAdmin:
  """
  """



  ##
  # @if jp
  # 
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  # 
  # @param self 
  # @param configsets �����оݥץ�ѥƥ�̾
  # 
  # @else
  # 
  # @endif
  # ConfigAdmin(coil::Properties& prop);
  def __init__(self, configsets):
    self._configsets = configsets
    self._activeId   = "default"
    self._active     = True
    self._changed    = False
    self._params     = []
    self._emptyconf  = OpenRTM_aist.Properties()
    self._newConfig  = []

    self._updateCb          = None
    self._updateParamCb     = None
    self._setConfigSetCb    = None
    self._addConfigSetCb    = None
    self._removeConfigSetCb = None
    self._activateSetCb     = None


  ##
  # @if jp
  # 
  # @brief �ǥ��ȥ饯��
  # 
  # �ǥ��ȥ饯����
  # ���ꤵ��Ƥ���ѥ�᡼���������롣
  # 
  # @param self 
  # 
  # @else
  # 
  # @endif
  def __del__(self):
    del self._params


  ##
  # @if jp
  # 
  # @brief ����ե�����졼�����ѥ�᡼��������
  # 
  # ����ե�����졼�����ѥ�᡼�����ѿ���Х���ɤ���
  # ���ꤷ��̾�ΤΥ���ե�����졼�����ѥ�᡼��������¸�ߤ������
  # false���֤���
  # 
  # @param self 
  # @param param_name ����ե�����졼�����ѥ�᡼��̾
  # @param var ����ե�����졼�����ѥ�᡼����Ǽ���ѿ�
  # @param def_val ����ե�����졼�����ѥ�᡼���ǥե������
  # @param trans ����ե�����졼�����ѥ�᡼��ʸ�����Ѵ��Ѵؿ�
  #             (�ǥե������:None)
  # 
  # @return ������(��������:true�����꼺��:false)
  # 
  # @else
  # 
  # @endif
  #template <typename VarType>
  # bool bindParameter(const char* param_name, VarType& var,
  #                    const char* def_val,
  #                    bool (*trans)(VarType&, const char*) = coil::stringTo)
  def bindParameter(self, param_name, var, def_val, trans=None):
    if trans is None:
      trans = OpenRTM_aist.stringTo
    
    if self.isExist(param_name):
      return False

    if not trans(var, def_val):
      return False
    
    self._params.append(Config(param_name, var, def_val, trans))
    return True


  ##
  # void update(void);
  #
  # @if jp
  #
  # @brief ����ե�����졼�����ѥ�᡼���ι���
  #        (�����ƥ��֥���ե�����졼����󥻥å�)
  # 
  # ����ե�����졼����󥻥åȤ���������Ƥ�����ˡ����ߥ����ƥ�
  # �֤ˤʤäƤ��륳��ե�����졼���������ꤷ���ͤǡ�����ե�����
  # �졼�����ѥ�᡼�����ͤ򹹿����롣���ν����Ǥι����ϡ������ƥ�
  # �֤ȤʤäƤ��륳��ե�����졼����󥻥åȤ�¸�ߤ��Ƥ����硢��
  # ��ι������饳��ե�����졼����󥻥åȤ����Ƥ���������Ƥ����
  # ��Τ߼¹Ԥ���롣
  #
  # @else
  #
  # @brief Update the values of configuration parameters
  #        (Active configuration set)
  # 
  # When configuration set is updated, update the configuration
  # parameter value to the value that is set to the current active
  # configuration.  This update will be executed, only when an
  # active configuration set exists and the content of the
  # configuration set has been updated from the last update.
  #
  # @endif
  #
  # void update(const char* config_set);
  #
  # @if jp
  #
  # @brief ����ե�����졼�����ѥ�᡼���ι���(ID����)
  # 
  # ����ե�����졼������ѿ����ͤ򡢻��ꤷ��ID����ĥ���ե�����졼
  # ����󥻥åȤ��ͤǹ������롣����ˤ�ꡢ�����ƥ��֤ʥ���ե�����
  # �졼����󥻥åȤ��ѹ�����ʤ����������äơ������ƥ��֥���ե�����
  # �졼����󥻥åȤȥѥ�᡼���ѿ��δ֤�̷�⤬ȯ�������ǽ��������
  # �Τ���դ�ɬ�פǤ��롣
  #
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ�¸�ߤ��ʤ����ϡ�����
  # �����˽�λ���롣
  #
  # @param config_set �����оݤΥ���ե�����졼����󥻥å�ID
  # 
  # @else
  #
  # @brief Update configuration parameter (By ID)
  # 
  # This operation updates configuration variables by the
  # configuration-set with specified ID. This operation does not
  # change current active configuration-set. Since this operation
  # causes inconsistency between current active configuration set
  # and actual values of configuration variables, user should
  # carefully use it.
  #
  # This operation ends without doing anything, if the
  # configuration-set does not exist.
  #
  # @param config_set The target configuration set's ID to setup
  #
  # @endif
  #
  # void update(const char* config_set, const char* config_param);
  #
  # @if jp
  #
  # @brief ����ե�����졼�����ѥ�᡼���ι���(̾�λ���)
  # 
  # ����Υ���ե�����졼������ѿ����ͤ򡢻��ꤷ��ID����ĥ���ե�
  # ����졼����󥻥åȤ��ͤǹ������롣����ˤ�ꡢ�����ƥ��֤ʥ���
  # �ե�����졼����󥻥åȤ��ѹ�����ʤ����������äơ������ƥ��֥�
  # ��ե�����졼����󥻥åȤȥѥ�᡼���ѿ��δ֤�̷�⤬ȯ�������
  # ǽ��������Τ���դ�ɬ�פǤ��롣
  #
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ䡢���ꤷ��̾�ΤΥѥ�᡼
  # ����¸�ߤ��ʤ����ϡ����⤻���˽�λ���롣
  #
  # @param config_set ����ե�����졼�����ID
  # @param config_param ����ե�����졼�����ѥ�᡼��̾
  # 
  # @else
  #
  # @brief Update the values of configuration parameters (By name)
  # 
  # This operation updates a configuration variable by the
  # specified configuration parameter in the
  # configuration-set. This operation does not change current
  # active configuration-set. Since this operation causes
  # inconsistency between current active configuration set and
  # actual values of configuration variables, user should carefully
  # use it.
  #
  # This operation ends without doing anything, if the
  # configuration-set or the configuration parameter do not exist.
  #
  # @param config_set configuration-set ID.
  # @param config_param configuration parameter name.
  #
  # @endif
  #
  def update(self, config_set=None, config_param=None):
    # update(const char* config_set)
    if config_set and config_param is None:
      if self._configsets.hasKey(config_set) is None:
        return
      prop = self._configsets.getNode(config_set)
      for i in range(len(self._params)):
        if prop.hasKey(self._params[i].name):
          self._params[i].update(prop.getProperty(self._params[i].name))
          self.onUpdate(config_set)

    # update(const char* config_set, const char* config_param)
    if config_set and config_param:
      key = config_set
      key = key+"."+config_param
      for conf in self._params:
        if conf.name == config_param:
          conf.update(self._configsets.getProperty(key))
          self.onUpdateParam(config_set, config_param)
          return

    # update()
    if config_set is None and config_param is None:
      if self._changed and self._active:
        self.update(self._activeId)
        self._changed = False
      return


  ##
  # @if jp
  # 
  # @brief ����ե�����졼�����ѥ�᡼����¸�߳�ǧ
  # 
  # ���ꤷ��̾�Τ���ĥ���ե�����졼�����ѥ�᡼����¸�ߤ��뤫��ǧ���롣
  # 
  # @param self 
  # @param param_name ����ե�����졼�����ѥ�᡼��̾�Ρ�
  # 
  # @return ¸�߳�ǧ���(�ѥ�᡼������:true���ѥ�᡼���ʤ�:false)
  # 
  # @else
  # 
  # @endif
  # bool isExist(const char* name);
  def isExist(self, param_name):
    if not self._params:
      return False
    
    for conf in self._params:
      if conf.name == param_name:
        return True

    return False


  ##
  # @if jp
  # 
  # @brief ����ե�����졼�����ѥ�᡼�����ѹ���ǧ
  # 
  # ����ե�����졼�����ѥ�᡼�����ѹ����줿����ǧ���롣
  # 
  # @param self 
  # 
  # @return �ѹ���ǧ���(�ѹ�����:true���ѹ��ʤ�:false)
  # 
  # @else
  # 
  # @endif
  # bool isChanged(void) {return m_changed;}
  def isChanged(self):
    return self._changed


  ##
  # @if jp
  # 
  # @brief �����ƥ��֡�����ե�����졼����󥻥å�ID�μ���
  # 
  # ���ߥ����ƥ��֤ʥ���ե�����졼����󥻥åȤ�ID��������롣
  # 
  # @param self 
  # 
  # @return �����ƥ��֡�����ե�����졼����󥻥å�ID
  # 
  # @else
  # 
  # @endif
  # const char* getActiveId(void);
  def getActiveId(self):
    return self._activeId


  ##
  # @if jp
  # 
  # @brief ����ե�����졼����󥻥åȤ�¸�߳�ǧ
  # 
  # ���ꤷ������ե�����졼����󥻥åȤ�¸�ߤ��뤫��ǧ���롣
  # 
  # @param self 
  # @param config_id ��ǧ�оݥ���ե�����졼����󥻥å�ID
  # 
  # @return ¸�߳�ǧ���(���ꤷ��ConfigSet����:true���ʤ�:false)
  # 
  # @else
  # 
  # @endif
  # bool haveConfig(const char* config_id);
  def haveConfig(self, config_id):
    if self._configsets.hasKey(config_id) is None:
      return False
    else:
      return True


  ##
  # @if jp
  # 
  # @brief ����ե�����졼����󥻥åȤΥ����ƥ��ֲ���ǧ
  # 
  # ����ե�����졼����󥻥åȤ������ƥ��ֲ�����Ƥ��뤫��ǧ���롣
  # 
  # @param self 
  # 
  # @return ���ֳ�ǧ���(�����ƥ��־���:true���󥢥��ƥ��־���:false)
  # 
  # @else
  # 
  # @endif
  # bool isActive(void);
  def isActive(self):
    return self._active


  ##
  # @if jp
  # 
  # @brief ������ե�����졼����󥻥åȤμ���
  # 
  # ���ꤵ��Ƥ���������ե�����졼����󥻥åȤ�������롣
  # 
  # @param self 
  # 
  # @return ������ե�����졼����󥻥å�
  # 
  # @else
  # 
  # @endif
  # const std::vector<coil::Properties*>& getConfigurationSets(void);
  def getConfigurationSets(self):
    return self._configsets.getLeaf()


  ##
  # @if jp
  # 
  # @brief ���ꤷ��ID�Υ���ե�����졼����󥻥åȤμ���
  # 
  # ID�ǻ��ꤷ������ե�����졼����󥻥åȤ�������롣
  # ���ꤷ������ե�����졼����󥻥åȤ�¸�ߤ��ʤ����ϡ�
  # ���Υ���ե�����졼����󥻥åȤ��֤���
  # 
  # @param self 
  # @param config_id �����оݥ���ե�����졼����󥻥åȤ�ID
  # 
  # @return ����ե�����졼����󥻥å�
  # 
  # @else
  # 
  # @endif
  # const coil::Properties& getConfigurationSet(const char* config_id);
  def getConfigurationSet(self, config_id):
    prop = self._configsets.getNode(config_id)
    if prop is None:
      return self._emptyconf
    return prop


  ##
  # @if jp
  # 
  # @brief ���ꤷ���ץ�ѥƥ��Υ���ե�����졼����󥻥åȤؤ��ɲ�
  # 
  # ���ꤷ���ץ�ѥƥ��򥳥�ե�����졼����󥻥åȤ��ɲä��롣
  # 
  # @param self 
  # @param config_set �ɲä���ץ�ѥƥ�
  # 
  # @return �ɲý����¹Է��(�ɲ�����:true���ɲü���:false)
  # 
  # @else
  # 
  # @endif
  # bool setConfigurationSetValues(const coil::Properties& config_set)
  def setConfigurationSetValues(self, config_set):
    if config_set.getName() == "" or config_set.getName() is None:
      return False

    if not self._configsets.hasKey(config_set.getName()):
      return False

    p = self._configsets.getNode(config_set.getName())
    if p is None:
      return False

    p.mergeProperties(config_set)
    self._changed = True
    self._active  = False
    self.onSetConfigurationSet(config_set)
    return True


  ##
  # @if jp
  # 
  # @brief �����ƥ��֡�����ե�����졼����󥻥åȤ����
  # 
  # ���ߥ����ƥ��֤ȤʤäƤ��륳��ե�����졼����󥻥åȤ�������롣
  # �����ƥ��֤ȤʤäƤ��륳��ե�����졼����󥻥åȤ�¸�ߤ��ʤ����ϡ�
  # ���Υ���ե�����졼����󥻥å� ���֤���
  # 
  # @param self 
  # 
  # @return �����ƥ��֡�����ե�����졼����󥻥å�
  # 
  # @else
  # 
  # @endif
  # const coil::Properties& getActiveConfigurationSet(void);
  def getActiveConfigurationSet(self):
    p = self._configsets.getNode(self._activeId)
    if p is None:
      return self._emptyconf

    return p


  ##
  # @if jp
  # 
  # @brief ����ե�����졼����󥻥åȤ������ͤ��ɲ�
  # 
  # ����ե�����졼����󥻥åȤ������ͤ��ɲä��롣
  # 
  # @param self 
  # @param configset �ɲä���ץ�ѥƥ�
  # 
  # @return �ɲý������(�ɲ�����:true���ɲü���:false)
  # 
  # @else
  # 
  # @endif
  # bool addConfigurationSet(const coil::Properties& configuration_set);
  def addConfigurationSet(self, configset):
    if self._configsets.hasKey(configset.getName()):
      return False
    node = configset.getName()

    # Create node
    self._configsets.createNode(node)

    p = self._configsets.getNode(node)
    if p is None:
      return False

    p.mergeProperties(configset)
    self._newConfig.append(node)

    self._changed = True
    self._active  = False
    self.onAddConfigurationSet(configset)
    return True


  ##
  # @if jp
  # 
  # @brief ����ե�����졼����󥻥åȤκ��
  # 
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ������롣
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ�¸�ߤ��ʤ����ϡ�
  # false���֤���
  # 
  # @param self 
  # @param config_id ����оݥ���ե�����졼����󥻥åȤ�ID
  # 
  # @return ����������(�������:true���������:false)
  # 
  # @else
  # 
  # @endif
  # bool removeConfigurationSet(const char* config_id);
  def removeConfigurationSet(self, config_id):
    if config_id == "default":
      return False
    if self._activeId == config_id:
      return False

    find_flg = False
    # removeable config-set is only config-sets newly added
    for (idx,conf) in enumerate(self._newConfig):
      if conf == config_id:
        find_flg = True
        break


    if not find_flg:
      return False

    p = self._configsets.getNode(config_id)
    if p:
      p.getRoot().removeNode(config_id)
      del p

    del self._newConfig[idx]

    self._changed = True
    self._active  = False
    self.onRemoveConfigurationSet(config_id)
    return True


  ##
  # @if jp
  # 
  # @brief ����ե�����졼����󥻥åȤΥ����ƥ��ֲ�
  # 
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ򥢥��ƥ��ֲ����롣
  # ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ�¸�ߤ��ʤ����ϡ�
  # false���֤���
  # 
  # @param self 
  # @param config_id ����оݥ���ե�����졼����󥻥åȤ�ID
  # 
  # @return �����ƥ��ֽ������(����:true������:false)
  # 
  # @else
  # 
  # @endif
  # bool activateConfigurationSet(const char* config_id);
  def activateConfigurationSet(self, config_id):
    if config_id is None:
      return False

    # '_<conf_name>' is special configuration set name
    if config_id[0] == '_':
      return False

    if not self._configsets.hasKey(config_id):
      return False
    self._activeId = config_id
    self._active   = True
    self._changed  = True
    self.onActivateSet(config_id)
    return True


  # void setOnUpdate(OnUpdateCallback* cb);
  def setOnUpdate(self, cb):
    self._updateCb = cb


  # void setOnUpdateParam(OnUpdateParamCallback* cb);
  def setOnUpdateParam(self, cb):
    self._updateParamCb = cb


  # void setOnSetConfigurationSet(OnSetConfigurationSetCallback* cb);
  def setOnSetConfigurationSet(self, cb):
    self._setConfigSetCb = cb


  # void setOnAddConfigurationSet(OnAddConfigurationAddCallback* cb);
  def setOnAddConfigurationSet(self, cb):
    self._addConfigSetCb = cb


  # void setOnRemoveConfigurationSet(OnRemoveConfigurationSetCallback* cb);
  def setOnRemoveConfigurationSet(self, cb):
    self._removeConfigSetCb = cb


  # void setOnActivateSet(OnActivateSetCallback* cb);
  def setOnActivateSet(self, cb):
    self._activateSetCb = cb


  # void onUpdate(const char* config_set);
  def onUpdate(self, config_set):
    if self._updateCb is not None:
      self._updateCb(config_set)


  # void onUpdateParam(const char* config_set, const char* config_param);
  def onUpdateParam(self, config_set, config_param):
    if self._updateParamCb is not None:
      self._updateParamCb(config_set, config_param)


  # void onSetConfigurationSet(const coil::Properties& config_set);
  def onSetConfigurationSet(self, config_set):
    if self._setConfigSetCb is not None:
      self._setConfigSetCb(config_set)


  # void onAddConfigurationSet(const coil::Properties& config_set);
  def onAddConfigurationSet(self, config_set):
    if self._addConfigSetCb is not None:
      self._addConfigSetCb(config_set)


  # void onRemoveConfigurationSet(const char* config_id);
  def onRemoveConfigurationSet(self, config_id):
    if self._removeConfigSetCb is not None:
      self._removeConfigSetCb(config_id)


  # void onActivateSet(const char* config_id);
  def onActivateSet(self, config_id):
    if self._activateSetCb is not None:
      self._activateSetCb(config_id)



  class find_conf:
    def __init__(self, name):
      self._name = name

    def __call__(self, conf):
      if conf is None or conf is 0:
        return False

      return self._name == conf.name
