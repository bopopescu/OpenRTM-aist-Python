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
import OpenRTM


##
# @if jp
# @class ConfigBase
# @brief ConfigBase ��ݥ��饹
# 
# �Ƽ拾��ե�����졼����������ݻ����뤿�����ݥ��饹��
# ��ݥ���ե�����졼����󥯥饹�ϡ��ʲ��δؿ��μ������󶡤��ʤ���
# �Фʤ�ʤ���
# 
# public���󥿡��ե������Ȥ��ưʲ��Τ�Τ��󶡤��롣
#  - update(): ����ե�����졼�����ѥ�᡼���ͤι���
# 
# @since 0.4.0
# 
# @else
# 
# @endif
class ConfigBase:



  ##
  # @if jp
  # 
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  # 
  # @param self 
  # @param name ����ե�����졼�����̾
  # @param def_val ʸ��������Υǥե������
  # 
  # @else
  # 
  # @endif
  def __init__(self, name, def_val):
    self.name = name
    self.default_value = def_val


  ##
  # @if jp
  # 
  # @brief ����ե�����졼�����ѥ�᡼���͹����Ѵؿ�(���֥��饹������)
  # 
  # ����ե�����졼����������ͤǥ���ե�����졼�����ѥ�᡼���򹹿�����
  # ����δؿ���<BR>
  # �����֥��饹�Ǥμ���������
  # 
  # @param self 
  # @param val �ѥ�᡼���ͤ�ʸ����ɽ��
  # 
  # @return ������
  # 
  # @else
  # 
  # @endif
  def update(self, val):
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
class Config(ConfigBase):



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
    ConfigBase.__init__(self, name, def_val)
    self._var = var
    if trans:
      self._trans = trans
    else:
      self._trans = OpenRTM.stringTo


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
  def __init__(self, configsets):
    self._configsets = configsets
    self._activeId   = "default"
    self._active     = True
    self._changed    = False
    self._params     = []
    self._emptyconf  = OpenRTM.Properties()
    self._newConfig  = []


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
  def bindParameter(self, param_name, var, def_val, trans=None):
    if trans is None:
      trans = OpenRTM.stringTo
    
    if self.isExist(param_name):
      return False

    if not OpenRTM.stringTo(var, def_val):
      return False
    
    self._params.append(Config(param_name, var, def_val, trans))
    return True


  ##
  # @if jp
  # 
  # @brief ����ե�����졼�����ѥ�᡼���ι���
  # 
  # ��������������ˤ�äưʲ��ν�����Ԥ���
  # - config_set�Τߤ����ꤵ��Ƥ�����
  #     ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ����ꤷ���ͤǡ�
  #     ����ե�����졼�����ѥ�᡼�����ͤ򹹿����롣
  #     ���ꤷ��ID�Υ���ե�����졼����󥻥åȤ�¸�ߤ��ʤ����ϡ�
  #     ���⤻���˽�λ���롣
  # - config_set��config_param�����ꤵ��Ƥ�����
  #     ���ꤷ���ѥ��Υ���ե�����졼���������ꤷ���ͤǡ�
  #     ����ե�����졼�����ѥ�᡼�����ͤ򹹿����롣
  # - config_set��config_param��ξ���Ȥ����ꤵ��Ƥ��ʤ����
  #     ����ե�����졼����󥻥åȤ���������Ƥ�����ˡ�
  #     ���ߥ����ƥ��֤ˤʤäƤ��륳��ե�����졼���������ꤷ���ͤǡ�
  #     ����ե�����졼�����ѥ�᡼�����ͤ򹹿����롣
  #     ���ν����Ǥι����ϡ������ƥ��֤ȤʤäƤ��륳��ե�����졼����󥻥å�
  #     ��¸�ߤ��Ƥ����硢����ι������饳��ե�����졼����󥻥åȤ����Ƥ�
  #     ��������Ƥ�����Τ߼¹Ԥ���롣
  # 
  # @param self 
  # @param config_set ����ե�����졼�����̾�Ρ���.�׶��ڤ�ǺǸ�����Ǥ�
  #                   ������̾��
  # @param config_param ����ե�����졼����󥻥åȤκǸ������̾
  # 
  # @else
  # 
  # @endif
  def update(self, config_set=None, config_param=None):
    # update(const char* config_set)
    if config_set and config_param is None:
      if self._configsets.hasKey(config_set) is None:
        return
      prop = self._configsets.getNode(config_set)
      for i in range(len(self._params)):
        if prop.hasKey(self._params[i].name):
          self._params[i].update(prop.getProperty(self._params[i].name))

    # update(const char* config_set, const char* config_param)
    if config_set and config_param:
      key = config_set
      key = key+"."+config_param
      for conf in self._params:
        if conf.name == config_param:
          conf.update(self._configsets.getProperty(key))
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
  def isExist(self, param_name):
    if self._params is None:
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
  # ���ꤷ���ץ�ѥƥ���ID�ǻ��ꤷ������ե�����졼����󥻥åȤ��ɲä��롣
  # ���ꤷ��ID�Ȱ��פ��륳��ե�����졼����󥻥åȤ�¸�ߤ��ʤ����ϡ�
  # false ���֤���
  # 
  # @param self 
  # @param config_id �ɲ��оݥ���ե�����졼����󥻥åȤ�ID
  # @param config_set �ɲä���ץ�ѥƥ�
  # 
  # @return �ɲý����¹Է��(�ɲ�����:true���ɲü���:false)
  # 
  # @else
  # 
  # @endif
  def setConfigurationSetValues(self, config_id, config_set):
    if config_set.getName() != config_id:
      return False
    if not self._configsets.hasKey(config_id):
      return False

    p = self._configsets.getNode(config_id)
    if p is None:
      return False
    p.mergeProperties(config_set)

    self._changed = True
    self._active  = False
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
  def addConfigurationSet(self, configset):
    if self._configsets.hasKey(configset.getName()):
      return False
    node = configset.getName()

    # Create node
    self._configsets.createNode(node)

    p = self._configsets.getNode(node)
    p.mergeProperties(configset)
    self._newConfig.append(node)

    self._changed = True
    self._active  = False

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
  def removeConfigurationSet(self, config_id):
    idx = 0
    for conf in self._newConfig:
      if conf == config_id:
        break
      idx += 1

    if idx == len(self._newConfig):
      return False

    p = self._configsets.getNode(config_id)
    if p:
      p.getRoot().removeNode(config_id)
      del p

    del self._newConfig[idx]

    self._changed = True
    self._active  = False

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
  def activateConfigurationSet(self, config_id):
    if config_id is None:
      return False
    if self._configsets.hasKey(config_id) is None:
      return False
    self._activeId = config_id
    self._active   = True
    self._changed  = True
    return True
