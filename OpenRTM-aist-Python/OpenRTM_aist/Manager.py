#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file Manager.py
# @brief RTComponent manager class
# @date $Date: $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import threading
import string
import signal, os
import sys
import traceback
import time
from omniORB import CORBA, PortableServer
from types import IntType, ListType

import OpenRTM_aist
import RTC
import SDOPackage



#------------------------------------------------------------
# static var
#------------------------------------------------------------

##
# @if jp
# @brief ͣ��� Manager �ؤΥݥ���
# @else
# @brief The pointer to the Manager
# @endif
manager = None

##
# @if jp
# @brief ͣ��� Manager �ؤΥݥ��󥿤��Ф��� mutex
# @else
# @brief The mutex of the pointer to the Manager 
# @endif
mutex = threading.RLock()


##
# @if jp
# @brief ��λ����
#
# �ޥ͡������λ������
#
# @param signum �����ʥ��ֹ�
# @param frame ���ߤΥ����å��ե졼��
#
# @else
#
# @endif
def handler(signum, frame):
  mgr = OpenRTM_aist.Manager.instance()
  mgr.terminate()



##
# @if jp
# @class ScopedLock
# @brief ScopedLock ���饹
#
# ��¾�����ѥ�å����饹��
#
# @since 0.4.0
#
# @else
#
# @endif
class ScopedLock:



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param mutex ��å��ѥߥ塼�ƥå���
  #
  # @else
  #
  # @endif
  def __init__(self, mutex):
    self.mutex = mutex
    self.mutex.acquire()


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @param self
  #
  # @else
  #
  # @endif
  def __del__(self):
    self.mutex.release()



##
# @if jp
# @class Manager
# @brief Manager ���饹
#
# ����ݡ��ͥ�ȤʤɳƼ�ξ��������Ԥ��ޥ͡����㥯�饹��
#
# @since 0.2.0
#
# @else
# @class Manager
# @brief Manager class
# @endif
class Manager:
  """
  """



  ##
  # @if jp
  # @brief ���ԡ����󥹥ȥ饯��
  #
  # ���ԡ����󥹥ȥ饯��
  #
  # @param self
  # @param _manager ���ԡ����ޥ͡����㥪�֥�������(�ǥե������:None)
  #
  # @else
  # @brief Protected Copy Constructor
  #
  # @endif
  def __init__(self, _manager=None):
    self._initProc   = None
    self._runner     = None
    self._terminator = None
    self._compManager = OpenRTM_aist.ObjectManager(self.InstanceName)
    self._factory = OpenRTM_aist.ObjectManager(self.FactoryPredicate)
    self._ecfactory = OpenRTM_aist.ObjectManager(self.ECFactoryPredicate)
    self._terminate = self.Term()
    self._ecs = []
    self._timer = None
    signal.signal(signal.SIGINT, handler)
    
    return


  ##
  # @if jp
  # @brief �ޥ͡�����ν����
  #
  # �ޥ͡�������������� static �ؿ���
  # �ޥ͡�����򥳥ޥ�ɥ饤�������Ϳ���ƽ�������롣
  # �ޥ͡��������Ѥ�����ϡ�ɬ�����ν�������дؿ� init() ��
  # �ƤФʤ���Фʤ�ʤ���
  # �ޥ͡�����Υ��󥹥��󥹤����������ˡ�Ȥ��ơ�init(), instance() ��
  # 2�Ĥ� static �ؿ����Ѱդ���Ƥ��뤬���������init()�Ǥ����Ԥ��ʤ����ᡢ
  # Manager ����¸���֤ΰ��ֺǽ�ˤ�init()��Ƥ�ɬ�פ����롣
  #
  # ���ޥ͡�����ν��������
  # - initManager: ����������config�ե�������ɤ߹��ߡ����֥����ƥ�����
  # - initLogger: Logger�����
  # - initORB: ORB �����
  # - initNaming: NamingService �����
  # - initExecutionContext: ExecutionContext factory �����
  # - initTimer: Timer �����
  #
  # @param argv ���ޥ�ɥ饤�����
  # 
  # @return Manager ��ͣ��Υ��󥹥��󥹤λ���
  #
  # @else
  # @brief Initializa manager
  #
  # This is the static function to tintialize the Manager.
  # The Manager is initialized by given arguments.
  # At the starting the manager, this static function "must" be called from
  # application program. The manager has two static functions to get 
  # the instance, "init()" and "instance()". Since initializing
  # process is only performed by the "init()" function, the "init()" has
  # to be called at the beginning of the lifecycle of the Manager.
  # function.
  #
  # @param argv The array of the command line arguments.
  #
  # @endif
  def init(*arg):
    global manager
    global mutex
    
    if len(arg) == 1:
      argv = arg[0]
    elif len(arg) == 2 and \
             isinstance(arg[0], IntType) and \
             isinstance(arg[1], ListType):
      argv = arg[1]
    else:
      print "Invalid arguments for init()"
      print "init(argc,argv) or init(argv)"
        
    if manager is None:
      guard = ScopedLock(mutex)
      if manager is None:
        manager = Manager()
        manager.initManager(argv)
        manager.initLogger()
        manager.initORB()
        manager.initNaming()
        manager.initExecContext()
        manager.initComposite()
        manager.initTimer()
        manager.initManagerServant()

    return manager
  
  init = staticmethod(init)


  ##
  # @if jp
  # @brief �ޥ͡�����Υ��󥹥��󥹤μ���
  #
  # �ޥ͡�����Υ��󥹥��󥹤�������� static �ؿ���
  # ���δؿ���Ƥ����ˡ�ɬ�����ν�����ؿ� init() ���ƤФ�Ƥ���ɬ�פ����롣
  #
  # @return Manager ��ͣ��Υ��󥹥��󥹤λ���
  # 
  # @else
  #
  # @brief Get instance of the manager
  #
  # This is the static function to get the instance of the Manager.
  # Before calling this function, ensure that the initialization function
  # "init()" is called.
  #
  # @return The only instance reference of the manager
  #
  # @endif
  def instance():
    global manager
    global mutex
    
    if manager is None:
      guard = ScopedLock(mutex)
      if manager is None:
        manager = Manager()
        manager.initManager(None)
        manager.initLogger()
        manager.initORB()
        manager.initNaming()
        manager.initExecContext()
        manager.initComposite()
        manager.initTimer()
        manager.initManagerServant()

    return manager

  instance = staticmethod(instance)


  ##
  # @if jp
  # @brief �ޥ͡����㽪λ����
  #
  # �ޥ͡�����ν�λ������¹Ԥ��롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def terminate(self):
    if self._terminator:
      self._terminator.terminate()


  ##
  # @if jp
  # @brief �ޥ͡����㡦����åȥ�����
  #
  # �ޥ͡�����ν�λ������¹Ԥ��롣
  # ORB��λ�塢Ʊ�����äƽ�λ���롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def shutdown(self):
    self._rtcout.RTC_DEBUG("Manager::shutdown()")
    self.shutdownComponents()
    self.shutdownNaming()
    self.shutdownORB()
    self.shutdownManager()

    if self._runner:
      self._runner.wait()
    else:
      self.join()

    self.shutdownLogger()


  ##
  # @if jp
  # @brief �ޥ͡����㽪λ�������Ԥ���碌
  #
  # Ʊ�����뤿�ᡢ�ޥ͡����㽪λ�������Ԥ���碌��Ԥ���
  #
  # @param self
  #
  # @else
  #
  # @endif
  def join(self):
    self._rtcout.RTC_DEBUG("Manager::wait()")
    guard = ScopedLock(self._terminate.mutex)
    self._terminate.waiting += 1
    del guard
    while 1:
      guard = ScopedLock(self._terminate.mutex)
      #if self._terminate.waiting > 1:
      if self._terminate.waiting > 0:
        break
      del guard
      time.sleep(0.001)


  ##
  # @if jp
  #
  # @brief ������ץ�������Υ��å�
  #
  # ���Υ��ڥ졼�����ϥ桼�����Ԥ��⥸�塼�����ν�����ץ�������
  # �����ꤹ�롣���������ꤵ�줿�ץ�������ϡ��ޥ͡����㤬��������졢
  # �����ƥ��ֲ����줿�塢Ŭ�ڤʥ����ߥ󥰤Ǽ¹Ԥ���롣
  #
  # @param self
  # @param proc ������ץ�������δؿ��ݥ���
  #
  # @else
  #
  # @brief Run the Manager
  #
  # This operation sets the initial procedure call to process module
  # initialization, other user defined initialization and so on.
  # The given procedure will be called at the proper timing after the 
  # manager initialization, activation and run.
  #
  # @param proc A function pointer to the initial procedure call
  #
  # @endif
  def setModuleInitProc(self, proc):
    self._initProc = proc
    return


  ##
  # @if jp
  #
  # @brief Manager�Υ����ƥ��ֲ�
  #
  # ���Υ��ڥ졼�����ϰʲ��ν�����Ԥ�
  # - CORBA POAManager �Υ����ƥ��ֲ�
  # - �ޥ͡�����CORBA���֥������ȤΥ����ƥ��ֲ�
  # - Manager ���֥������Ȥؤν�����ץ�������μ¹�
  #
  # ���Υ��ڥ졼�����ϡ��ޥ͡�����ν�����塢runManager()
  # �����˸Ƥ�ɬ�פ����롣
  #
  # @param self
  #
  # @return �������(�����ƥ��ֲ�����:true������:false)
  #
  # @else
  #
  # @brief Activate Manager
  #
  # This operation do the following,
  # - Activate CORBA POAManager
  # - Activate Manager CORBA object
  # - Execute the initial procedure call of the Manager
  #
  # This operationo should be invoked after Manager:init(),
  # and before tunManager().
  #
  # @endif
  def activateManager(self):
    self._rtcout.RTC_DEBUG("Manager::activateManager()")

    try:
      self.getPOAManager().activate()
      if self._initProc:
        self._initProc(self)
    except:
      print "Exception: Manager.activateManager()"
      return False

    return True


  ##
  # @if jp
  #
  # @brief Manager�μ¹�
  #
  # ���Υ��ڥ졼�����ϥޥ͡�����Υᥤ��롼�פ�¹Ԥ��롣
  # ���Υᥤ��롼����Ǥϡ�CORBA ORB�Υ��٥�ȥ롼������
  # ��������롣�ǥե���ȤǤϡ����Υ��ڥ졼�����ϥ֥�å�����
  # Manager::destroy() ���ƤФ��ޤǽ������ᤵ�ʤ���
  # ���� no_block �� true �����ꤵ��Ƥ�����ϡ������ǥ��٥�ȥ롼��
  # ��������륹��åɤ�ư�����֥�å������˽������᤹��
  #
  # @param self
  # @param no_block false: �֥�å��󥰥⡼��, true: �Υ�֥�å��󥰥⡼��
  #
  # @else
  #
  # @brief Run the Manager
  #
  # This operation processes the main event loop of the Manager.
  # In this main loop, CORBA's ORB event loop or other processes
  # are performed. As the default behavior, this operation is going to
  # blocking mode and never returns until manager::destroy() is called.
  # When the given argument "no_block" is set to "true", this operation
  # creates a thread to process the event loop internally, and it doesn't
  # block and returns.
  #
  # @param no_block false: Blocking mode, true: non-blocking mode.
  #
  # @endif
  def runManager(self, no_block=None):
    if no_block is None:
      no_block = False

    if no_block:
      self._rtcout.RTC_DEBUG("Manager::runManager(): non-blocking mode")
      self._runner = self.OrbRunner(self._orb)
      # self._runnner.open()
    else:
      self._rtcout.RTC_DEBUG("Manager::runManager(): blocking mode")
      self._orb.run()
      self._rtcout.RTC_DEBUG("Manager::runManager(): ORB was terminated")
      self.join()
    return


  ##
  # @if jp
  # @brief [CORBA interface] �⥸�塼��Υ���
  #
  # ���ꤷ������ݡ��ͥ�ȤΥ⥸�塼�����ɤ���ȤȤ�ˡ�
  # ���ꤷ��������ؿ���¹Ԥ��롣
  #
  # @param self
  # @param fname   �⥸�塼��ե�����̾
  # @param initfunc ������ؿ�̾
  # 
  # @else
  #
  # @brief [CORBA interface] Load module
  #
  # Load module (shared library, DLL etc..) by file name,
  # and invoke initialize function.
  #
  # @param fname    The module file name
  # @param initfunc The initialize function name
  #
  # @endif
  def load(self, fname, initfunc):
    self._rtcout.RTC_DEBUG("Manager::load()")
    self._module.load(fname, initfunc)
    return


  ##
  # @if jp
  #
  # @brief �⥸�塼��Υ������
  #
  # �⥸�塼��򥢥���ɤ���
  #
  # @param self
  # @param fname �⥸�塼��Υե�����̾
  # 
  # @else
  #
  # @brief Unload module
  #
  # Unload shared library.
  #
  # @param pathname Module file name
  #
  # @endif
  def unload(self, fname):
    self._rtcout.RTC_DEBUG("Manager::unload()")
    self._module.unload(fname)
    return


  ##
  # @if jp
  #
  # @brief ���⥸�塼��Υ������
  #
  # �⥸�塼��򤹤٤ƥ�����ɤ���
  #
  # @param self
  #
  # @else
  #
  # @brief Unload module
  #
  # Unload all loaded shared library.
  #
  # @endif
  def unloadAll(self):
    self._rtcout.RTC_DEBUG("Manager::unloadAll()")
    self._module.unloadAll()
    return


  ##
  # @if jp
  # @brief ���ɺѤߤΥ⥸�塼��ꥹ�Ȥ��������
  #
  # ���ߥޥ͡�����˥��ɤ���Ƥ���⥸�塼��Υꥹ�Ȥ�������롣
  #
  # @param self
  #
  # @return ���ɺѤߥ⥸�塼��ꥹ��
  #
  # @else
  # @brief Get loaded module names
  # @endif
  def getLoadedModules(self):
    self._rtcout.RTC_DEBUG("Manager::getLoadedModules()")
    return self._module.getLoadedModules()


  ##
  # @if jp
  # @brief ���ɲ�ǽ�ʥ⥸�塼��ꥹ�Ȥ��������
  #
  # ���ɲ�ǽ�⥸�塼��Υꥹ�Ȥ�������롣
  # (���ߤ�ModuleManager¦��̤����)
  #
  # @param self
  #
  # @return ���ɲ�ǽ�⥸�塼�롡�ꥹ��
  #
  # @else
  # @brief Get loadable module names
  # @endif
  def getLoadableModules(self):
    self._rtcout.RTC_DEBUG("Manager::getLoadableModules()")
    return self._module.getLoadableModules()


  #============================================================
  # Component Factory Management
  #============================================================

  ##
  # @if jp
  # @brief RT����ݡ��ͥ���ѥե����ȥ����Ͽ����
  #
  # RT����ݡ��ͥ�ȤΥ��󥹥��󥹤��������뤿���
  # Factory����Ͽ���롣
  #
  # @param self
  # @param profile RT����ݡ��ͥ�� �ץ�ե�����
  # @param new_func RT����ݡ��ͥ�������Ѵؿ�
  # @param delete_func RT����ݡ��ͥ���˴��Ѵؿ�
  #
  # @return ��Ͽ�������(��Ͽ����:true������:false)
  #
  # @else
  # @brief Register RT-Component Factory
  # @endif
  def registerFactory(self, profile, new_func, delete_func):
    self._rtcout.RTC_DEBUG("Manager::registerFactory(%s)", profile.getProperty("type_name"))
    try:
      factory = OpenRTM_aist.FactoryPython(profile, new_func, delete_func)
      self._factory.registerObject(factory)
      return True
    except:
      return False


  def getFactoryProfiles(self):
    factories = self._factory.getObjects()

    if factories is None or factories is []:
      return []
      
    props = []
    for factory in factories:
      props.append(factory.profile())

    return props


  ##
  # @if jp
  # @brief ExecutionContext�ѥե����ȥ����Ͽ����
  #
  # ExecutionContext�Υ��󥹥��󥹤��������뤿���Factory����Ͽ���롣
  #
  # @param self
  # @param name �����о�ExecutionContext̾��
  # @param new_func ExecutionContext�����Ѵؿ�
  # @param delete_func ExecutionContext�˴��Ѵؿ�
  #
  # @return ��Ͽ�������(��Ͽ����:true������:false)
  #
  # @else
  # @brief Register ExecutionContext Factory
  # @endif
  def registerECFactory(self, name, new_func, delete_func):
    self._rtcout.RTC_DEBUG("Manager::registerECFactory(%s)", name)
    try:
      self._ecfactory.registerObject(OpenRTM_aist.ECFactoryPython(name, new_func, delete_func))
      return True
    except:
      return False

    return False


  ##
  # @if jp
  # @brief �ե����ȥ����ꥹ�Ȥ��������
  #
  # ��Ͽ����Ƥ���ե����ȥ�����ꥹ�Ȥ�������롣
  #
  # @param self
  #
  # @return ��Ͽ�ե����ȥ� �ꥹ��
  #
  # @else
  # @brief Get the list of all RT-Component Factory
  # @endif
  def getModulesFactories(self):
    self._rtcout.RTC_DEBUG("Manager::getModulesFactories()")

    self._modlist = []
    for _obj in self._factory._objects._obj:
      self._modlist.append(_obj.profile().getProperty("implementation_id"))
    return self._modlist


  #============================================================
  # Component management
  #============================================================

  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ���������
  #
  # ���ꤷ��RT����ݡ��ͥ�ȤΥ��󥹥��󥹤���Ͽ���줿Factory��ͳ���������롣
  # ���󥹥�������������������硢ʻ���ưʲ��ν�����¹Ԥ��롣
  #  - �����ե���������ꤷ������ե�����졼����������ɤ߹��ߡ�����
  #  - ExecutionContext�ΥХ���ɡ�ư���
  #  - �͡��ߥ󥰥����ӥ��ؤ���Ͽ
  #
  # @param self
  # @param module_name �����о�RT����ݡ��ͥ��̾��
  #
  # @return ��������RT����ݡ��ͥ�ȤΥ��󥹥���
  #
  # @else
  # @brief Create RT-Component
  # @endif
  def createComponent(self, module_name):
    prop = OpenRTM_aist.Properties()
    arg = str(module_name)
    comp_and_conf = arg.split("?")
    if len(comp_and_conf) == 0:
      return None

    module_name = comp_and_conf[0]

    if len(comp_and_conf) > 1:
      conf = comp_and_conf[1].split("&")
      for i in range(len(conf)):
        keyval = conf[i].split("=")
        prop.setProperty(keyval[0],keyval[1])

    self._rtcout.RTC_DEBUG("Manager::createComponent(%s)", module_name)

    obj = self._factory.find(module_name)
    if obj is None:
      print "Manager.createComponent: Not found module_name: ", module_name
      return None

    comp = obj.create(self)
    if comp is None:
      return None
    self._rtcout.RTC_DEBUG("RTC Created: %s", module_name)

    self.configureComponent(comp,prop)

    if self.bindExecutionContext(comp) is not True:
      comp.exit()
      return None

    if comp.initialize() is not RTC.RTC_OK:
      self._rtcout.RTC_DEBUG("RTC initialization failed: %s", module_name)
      comp.exit()
      self._rtcout.RTC_DEBUG("%s was finalized", module_name)
      return None

    self._rtcout.RTC_DEBUG("RTC initialization succeeded: %s", module_name)
    self.registerComponent(comp)
    return comp


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ�ľ�� Manager ����Ͽ����
  #
  # ���ꤷ��RT����ݡ��ͥ�ȤΥ��󥹥��󥹤�ե����ȥ��ͳ�ǤϤʤ�
  # ľ�ܥޥ͡��������Ͽ���롣
  #
  # @param self
  # @param comp ��Ͽ�о�RT����ݡ��ͥ�ȤΥ��󥹥���
  #
  # @return ��Ͽ�������(��Ͽ����:true������:false)
  #
  # @else
  # @brief Register RT-Component directly without Factory
  # @endif
  def registerComponent(self, comp):
    self._rtcout.RTC_DEBUG("Manager::registerComponent(%s)", comp.getInstanceName())

    self._compManager.registerObject(comp)
    names = comp.getNamingNames()

    for name in names:
      self._rtcout.RTC_DEBUG("Bind name: %s", name)
      self._namingManager.bindObject(name, comp)

    return True

  
  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ���Ͽ��������
  #
  # ���ꤷ��RT����ݡ��ͥ�Ȥ���Ͽ�������롣
  #
  # @param self
  # @param comp ��Ͽ����о�RT����ݡ��ͥ�ȤΥ��󥹥���
  #
  # @return ��Ͽ����������(�������:true���������:false)
  #
  # @else
  # @brief Register RT-Component directly without Factory
  # @endif
  def unregisterComponent(self, comp):
    self._rtcout.RTC_DEBUG("Manager::unregisterComponent(%s)", comp.getInstanceName())
    self._compManager.unregisterObject(comp.getInstanceName())
    names = comp.getNamingNames()
    
    for name in names:
      self._rtcout.RTC_DEBUG("Unbind name: %s", name)
      self._namingManager.unbindObject(name)

    return True


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ�ExecutionContext��Х���ɤ���
  #
  # ���ꤷ��RT����ݡ��ͥ�Ȥ�ExecutionContext��Х���ɤ��롣
  # �Х���ɤ���ExecutionContext�η��ϥץ�ѥƥ����ե������
  # "exec_cxt.periodic.type"°���ˤ�äƻ��ꤹ�롣
  #
  # @param self
  # @param comp �Х�����о�RT����ݡ��ͥ�ȤΥ��󥹥���
  #
  # @return �Х���ɽ������(�Х��������:true������:false)
  #
  # @else
  # @brief Register RT-Component directly without Factory
  # @endif
  def bindExecutionContext(self, comp):
    self._rtcout.RTC_DEBUG("Manager::bindExecutionContext()")
    self._rtcout.RTC_DEBUG("ExecutionContext type: %s",
                 self._config.getProperty("exec_cxt.periodic.type"))

    rtobj = comp.getObjRef()

    exec_cxt = None

    if OpenRTM_aist.isDataFlowComponent(rtobj):
      ectype = self._config.getProperty("exec_cxt.periodic.type")
      exec_cxt = self._ecfactory.find(ectype).create()
      rate = self._config.getProperty("exec_cxt.periodic.rate")
      exec_cxt.set_rate(float(rate))
    else:
      ectype = self._config.getProperty("exec_cxt.evdriven.type")
      exec_cxt = self._ecfactory.find(ectype).create()
    exec_cxt.bindComponent(comp)
    exec_cxt.start()
    self._ecs.append(exec_cxt)
    return True


  ##
  # @if jp
  # @brief Manager ����Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ�������(̤����)
  #
  # �ޥ͡��������Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ������롣
  #
  # @param self
  # @param instance_name ����о�RT����ݡ��ͥ�ȤΥ��󥹥���̾
  #
  # @else
  # @brief Unregister RT-Component that is registered in the Manager
  # @endif
  def deleteComponent(self, instance_name):
    self._rtcout.RTC_DEBUG("Manager::deleteComponent(%s)", instance_name)
    comp = self._compManager.find(instance_name)
    if comp is None:
      return

    comp.exit()
    self._compManager.unregisterObject(instance_name)


  ##
  # @if jp
  # @brief Manager ����Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ򸡺�����
  #
  # Manager ����Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ���ꤷ��̾�ΤǸ�������
  # ���פ��륳��ݡ��ͥ�Ȥ�������롣
  #
  # @param self
  # @param instance_name �����о�RT����ݡ��ͥ�Ȥ�̾��
  #
  # @return ̾�Τ����פ���RT����ݡ��ͥ�ȤΥ��󥹥���
  #
  # @else
  # @brief Get RT-Component's pointer
  # @endif
  def getComponent(self, instance_name):
    self._rtcout.RTC_DEBUG("Manager::getComponent(%s)", instance_name)
    return self._compManager.find(instance_name)


  ##
  # @if jp
  # @brief Manager ����Ͽ����Ƥ�����RT����ݡ��ͥ�Ȥ��������
  #
  # Manager ����Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ������󥹥��󥹤�������롣
  #
  # @param self
  #
  # @return ��RT����ݡ��ͥ�ȤΥ��󥹥��󥹥ꥹ��
  #
  # @else
  # @brief Get all RT-Component's pointer
  # @endif
  def getComponents(self):
    self._rtcout.RTC_DEBUG("Manager::getComponents()")
    return self._compManager.getObjects()


  #============================================================
  # CORBA ��Ϣ
  #============================================================

  ##
  # @if jp
  # @brief ORB �Υݥ��󥿤��������
  #
  # Manager �����ꤵ�줿 ORB �Υݥ��󥿤�������롣
  #
  # @param self
  #
  # @return ORB ���֥�������
  #
  # @else
  # @brief Get the pointer to the ORB
  # @endif
  def getORB(self):
    self._rtcout.RTC_DEBUG("Manager::getORB()")
    return self._orb


  ##
  # @if jp
  # @brief Manager ������ RootPOA �Υݥ��󥿤��������
  #
  # Manager �����ꤵ�줿 RootPOA �ؤΥݥ��󥿤�������롣
  #
  # @param self
  #
  # @return RootPOA���֥�������
  #
  # @else
  # @brief Get the pointer to the RootPOA 
  # @endif
  def getPOA(self):
    self._rtcout.RTC_DEBUG("Manager::getPOA()")
    return self._poa


  ##
  # @if jp
  # @brief Manager ������ POAManager ���������
  #
  # Manager �����ꤵ�줿 POAMAnager ��������롣
  #
  # @param self
  #
  # @return POA�ޥ͡�����
  #
  # @else
  #
  # @endif
  def getPOAManager(self):
    self._rtcout.RTC_DEBUG("Manager::getPOAManager()")
    return self._poaManager



  #============================================================
  # Manager initialize and finalization
  #============================================================

  ##
  # @if jp
  # @brief Manager ���������������
  # 
  # Manager �����������������¹Ԥ��롣
  #  - Manager ����ե�����졼����������
  #  - �����ϥե����������
  #  - ��λ�����ѥ���åɤ�����
  #  - �������ѥ���åɤ�����(�����޻��ѻ�)
  #
  # @param self
  # @param argv ���ޥ�ɥ饤�����
  # 
  # @else
  # @brief Manager internal initialization
  # @endif
  def initManager(self, argv):
    config = OpenRTM_aist.ManagerConfig(argv)
    self._config = config.configure(OpenRTM_aist.Properties())
    self._config.setProperty("logger.file_name",self.formatString(self._config.getProperty("logger.file_name"), self._config))

    self._module = OpenRTM_aist.ModuleManager(self._config)
    self._terminator = self.Terminator(self)
    guard = ScopedLock(self._terminate.mutex)
    self._terminate.waiting = 0
    del guard

    if OpenRTM_aist.toBool(self._config.getProperty("timer.enable"), "YES", "NO", True):
      tm = OpenRTM_aist.TimeValue(0, 100000)
      tick = self._config.getProperty("timer.tick")
      if tick != "":
        tm = tm.set_time(float(tick))
        self._timer = OpenRTM_aist.Timer(tm)
        self._timer.start()


  ##
  # @if jp
  # @brief Manager �ν�λ����(̤����)
  #
  # Manager ��λ����
  # (�����������ߤ�̤����)
  #
  # @param self
  #
  # @else
  #
  # @endif
  def shutdownManager(self):
    self._rtcout.RTC_DEBUG("Manager::shutdownManager()")
    if self._timer:
      self._timer.stop()


  #============================================================
  # Logger initialize and terminator
  #============================================================

  ##
  # @if jp
  # @brief System logger �ν����
  #
  # System logger �ν������¹Ԥ��롣
  # ����ե�����졼�����ե���������ꤵ�줿����˴�Ť���
  # �����ν�����������¹Ԥ��롣
  #
  # @param self
  #
  # @return ������¹Է��(���������:true�����������:false)
  #
  # @else
  # @brief System logger initialization
  # @endif
  def initLogger(self):
    logfile = self._config.getProperty("logger.file_name")
    if logfile == "":
      logfile = "./rtc.log"

    if OpenRTM_aist.toBool(self._config.getProperty("logger.enable"), "YES", "NO", True):
      self._Logbuf = OpenRTM_aist.Logbuf(fileName = logfile)
      self._rtcout = OpenRTM_aist.LogStream(self._Logbuf)
      self._rtcout.setLogLevel(self._config.getProperty("logger.log_level"))
      self._rtcout.setLogLock(OpenRTM_aist.toBool(self._config.getProperty("logger.stream_lock"),
                          "enable", "disable", False))

      self._rtcout.RTC_INFO("%s", self._config.getProperty("openrtm.version"))
      self._rtcout.RTC_INFO("Copyright (C) 2003-2007")
      self._rtcout.RTC_INFO("  Noriaki Ando")
      self._rtcout.RTC_INFO("  Task-intelligence Research Group,")
      self._rtcout.RTC_INFO("  Intelligent Systems Research Institute, AIST")
      self._rtcout.RTC_INFO("Manager starting.")
      self._rtcout.RTC_INFO("Starting local logging.")
    else:
      self._rtcout = OpenRTM_aist.LogStream()

    return True


  ##
  # @if jp
  # @brief System Logger �ν�λ����(̤����)
  #
  # System Logger�ν�λ������¹Ԥ��롣
  # (���ߤ�̤����)
  #
  # @param self
  #
  # @else
  # @brief System Logger finalization
  # @endif
  def shutdownLogger(self):
    self._rtcout.RTC_DEBUG("Manager::shutdownLogger()")


  #============================================================
  # ORB initialization and finalization
  #============================================================

  ##
  # @if jp
  # @brief CORBA ORB �ν��������
  #
  # �������򸵤�ORB���������롣
  #
  # @param self
  #
  # @return ORB ������������(���������:true�����������:false)
  #
  # @else
  # @brief CORBA ORB initialization
  # @endif
  def initORB(self):
    self._rtcout.RTC_DEBUG("Manager::initORB()")

    try:
      args = OpenRTM_aist.split(self.createORBOptions(), " ")
      argv = OpenRTM_aist.toArgv(args)
      self._orb = CORBA.ORB_init(argv)

      self._poa = self._orb.resolve_initial_references("RootPOA")

      if CORBA.is_nil(self._poa):
        self._rtcout.RTC_ERROR("Could not resolve RootPOA")
        return False

      self._poaManager = self._poa._get_the_POAManager()
    except:
      self._rtcout.RTC_ERROR("Exception: Caught unknown exception in initORB().")
      return False

    return True


  ##
  # @if jp
  # @brief ORB �Υ��ޥ�ɥ饤�󥪥ץ�������
  #
  # ����ե�����졼������������ꤵ�줿���Ƥ���
  # ORB �ε�ư�����ץ�����������롣
  #
  # @param self
  #
  # @return ORB ��ư�����ץ����
  #
  # @else
  # @brief ORB command option creation
  # @endif
  def createORBOptions(self):
    opt      = self._config.getProperty("corba.args")
    corba    = self._config.getProperty("corba.id")
    endpoint = self._config.getProperty("corba.endpoint")

    if endpoint != "":
      if opt != "":
        opt += " "
      if corba == "omniORB":
        opt = "-ORBendPoint giop:tcp:" + endpoint
      elif corba == "TAO":
        opt = "-ORBEndPoint iiop://" + endpoint
      elif corba == "MICO":
        opt = "-ORBIIOPAddr inet:" + endpoint
    return opt


  ##
  # @if jp
  # @brief ORB �ν�λ����
  #
  # ORB �ν�λ������¹Ԥ��롣
  # �¹��Ԥ��ν�����¸�ߤ�����ˤϡ����ν�������λ����ޤ��Ԥġ�
  # �ºݤν�λ�����Ǥϡ�POA Manager������������� ORB �Υ���åȥ������¹�
  # ���롣
  #
  # @param self
  #
  # @else
  # @brief ORB finalization
  # @endif
  def shutdownORB(self):
    self._rtcout.RTC_DEBUG("Manager::shutdownORB()")
    try:
      while self._orb.work_pending():
        self._rtcout.RTC_PARANOID("Pending work still exists.")
        if self._orb.work_pending():
          self._orb.perform_work()
    except:
      traceback.print_exception(*sys.exc_info())
      pass

    self._rtcout.RTC_DEBUG("No pending works of ORB. Shutting down POA and ORB.")

    if not CORBA.is_nil(self._poa):
      try:
        if not CORBA.is_nil(self._poaManager):
          self._poaManager.deactivate(False, True)
        self._rtcout.RTC_DEBUG("POA Manager was deactivated.")
        self._poa.destroy(False, True)
        self._poa = PortableServer.POA._nil
        self._rtcout.RTC_DEBUG("POA was destroid.")
      except CORBA.SystemException, ex:
        self._rtcout.RTC_ERROR("Caught SystemException during root POA destruction")
      except:
        self._rtcout.RTC_ERROR("Caught unknown exception during destruction")

    if self._orb:
      try:
        self._orb.shutdown(True)
        self._rtcout.RTC_DEBUG("ORB was shutdown.")
        self._orb = CORBA.Object._nil
      except CORBA.SystemException, ex:
        self._rtcout.RTC_ERROR("Caught CORBA::SystemException during ORB shutdown.")
      except:
        self._rtcout.RTC_ERROR("Caught unknown exception during ORB shutdown.")


  #============================================================
  # NamingService initialization and finalization
  #============================================================

  ##
  # @if jp
  # @brief NamingManager �ν����
  #
  # NamingManager �ν����������¹Ԥ��롣
  # �������� NamingManager ����Ѥ��ʤ��褦�˥ץ�ѥƥ���������ꤵ��Ƥ���
  # ���ˤϲ��⤷�ʤ���
  # NamingManager ����Ѥ����硢�ץ�ѥƥ���������ꤵ��Ƥ���
  # �ǥե���� NamingServer ����Ͽ���롣
  # �ޤ������Ū�˾���򹹿�����褦�����ꤵ��Ƥ�����ˤϡ����ꤵ�줿����
  # �Ǽ�ư������Ԥ�����Υ����ޤ�ư����ȤȤ�ˡ������ѥ᥽�åɤ򥿥��ޤ�
  # ��Ͽ���롣
  #
  # @param self
  #
  # @return ������������(���������:true�����������:false)
  #
  # @else
  #
  # @endif
  def initNaming(self):
    self._rtcout.RTC_DEBUG("Manager::initNaming()")
    self._namingManager = OpenRTM_aist.NamingManager(self)

    if not OpenRTM_aist.toBool(self._config.getProperty("naming.enable"), "YES", "NO", True):
      return True

    meths = OpenRTM_aist.split(self._config.getProperty("naming.type"),",")
    
    for meth in meths:
      names = OpenRTM_aist.split(self._config.getProperty(meth+".nameservers"), ",")
      for name in names:
        self._rtcout.RTC_DEBUG("Register Naming Server: %s/%s", (meth, name))
        self._namingManager.registerNameServer(meth,name)

    if OpenRTM_aist.toBool(self._config.getProperty("naming.update.enable"), "YES", "NO", True):
      tm = OpenRTM_aist.TimeValue(10,0)
      intr = self._config.getProperty("naming.update.interval")
      if intr != "":
        tm = OpenRTM_aist.TimeValue(intr)

      if self._timer:
        self._timer.registerListenerObj(self._namingManager,OpenRTM_aist.NamingManager.update,tm)
  
    return True


  ##
  # @if jp
  # @brief NamingManager �ν�λ����
  #
  # NamingManager ��λ���롣
  # ��Ͽ����Ƥ��������Ǥ򥢥�Х���ɤ�����λ���롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def shutdownNaming(self):
    self._rtcout.RTC_DEBUG("Manager::shutdownNaming()")
    self._namingManager.unbindAll()


  ##
  # @if jp
  # @brief ExecutionContextManager �ν����
  #
  # ���Ѥ���� ExecutionContext �ν����������¹Ԥ����� ExecutionContext 
  # ������ Factory �� ExecutionContextManager ����Ͽ���롣
  #
  # @param self
  #
  # @return ExecutionContextManager ����������¹Է��
  #         (���������:true�����������:false)
  #
  # @else
  #
  # @endif
  def initExecContext(self):
    self._rtcout.RTC_DEBUG("Manager::initExecContext()")
    OpenRTM_aist.PeriodicExecutionContextInit(self)
    OpenRTM_aist.ExtTrigExecutionContextInit(self)
    OpenRTM_aist.OpenHRPExecutionContextInit(self)
    return True


  def initComposite(self):
    self._rtcout.RTC_DEBUG("Manager::initComposite()")
    OpenRTM_aist.PeriodicECSharedCompositeInit(self)
    return True

  
  ##
  # @if jp
  # @brief Timer �ν����
  #
  # ���Ѥ���� Timer �ν����������¹Ԥ��롣
  # (�����μ����Ǥϲ��⤷�ʤ�)
  #
  # @param self
  #
  # @return Timer ����������¹Է��(���������:true�����������:false)
  #
  # @else
  #
  # @endif
  def initTimer(self):
    return True


  def initManagerServant(self):
    self._mgrservant = OpenRTM_aist.ManagerServant()
    prop = self._config.getNode("manager")
    names = OpenRTM_aist.split(prop.getProperty("naming_formats"),",")

    for name in names:
      mgr_name = self.formatString(name, prop)
      self._namingManager.bindManagerObject(mgr_name, self._mgrservant)

    otherref = None

    try:
      otherref = file(self._config.getProperty("manager.refstring_path"),'r')
    except:
      print "Not found. : %s" % self._config.getProperty("manager.refstring_path")
    else:
      otherref.close()
      try:
        reffile = file(self._config.getProperty("manager.refstring_path"),'w')
      except:
        return False
      else:
        reffile.write(self._pORB.object_to_string(self._mgrservant.getObjRef()))
        reffile.close()
    return True

  
  ##
  # @if jp
  # @brief NamingManager ����Ͽ����Ƥ���������ݡ��ͥ�Ȥν�λ����
  #
  # NamingManager ����Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ���� ExecutionContext ��
  # �ꥹ�Ȥ��������������ݡ��ͥ�Ȥ�λ���롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def shutdownComponents(self):
    self._rtcout.RTC_DEBUG("Manager::shutdownComponents()")
    comps = self._namingManager.getObjects()
    for comp in comps:
      try:
        comp.exit()
        p = OpenRTM_aist.Properties(key=comp.getInstanceName())
        p.mergeProperties(comp.getProperties())
      except:
        traceback.print_exception(*sys.exc_info())
        pass

    for ec in self._ecs:
      try:
        self._poa.deactivate_object(self._poa.servant_to_id(ec))
      except:
        traceback.print_exception(*sys.exc_info())
        pass


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ���Ͽ���
  #
  # ���ꤷ��RT����ݡ��ͥ�ȤΥ��󥹥��󥹤�͡��ߥ󥰥����ӥ�����
  # ��Ͽ������롣
  #
  # @param self
  # @param comp ��Ͽ����о�RT����ݡ��ͥ��
  #
  # @else
  #
  # @endif
  def cleanupComponent(self, comp):
    self._rtcout.RTC_DEBUG("Manager::cleanupComponents")
    self.unregisterComponent(comp)


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�ȤΥ���ե�����졼��������
  #
  # RT����ݡ��ͥ�Ȥη�����ӥ��󥹥�����˵��ܤ��줿�ץ�ѥƥ��ե������
  # ������ɤ߹��ߡ�����ݡ��ͥ�Ȥ����ꤹ�롣
  # �ޤ����ƥ���ݡ��ͥ�Ȥ� NamingService ��Ͽ����̾�Τ�����������ꤹ�롣
  #
  # @param self
  # @param comp ����ե�����졼������о�RT����ݡ��ͥ��
  #
  # @else
  #
  # @endif
  def configureComponent(self, comp, prop):
    category  = comp.getCategory()
    type_name = comp.getTypeName()
    inst_name = comp.getInstanceName()

    type_conf = category + "." + type_name + ".config_file"
    name_conf = category + "." + inst_name + ".config_file"

    type_prop = OpenRTM_aist.Properties()

    name_prop = OpenRTM_aist.Properties()

    if self._config.getProperty(name_conf) != "":
      try:
        conff = open(self._config.getProperty(name_conf))
      except:
        print "Not found. : %s" % self._config.getProperty(name_conf)
      else:
        name_prop.load(conff)

    if self._config.getProperty(type_conf) != "":
      try:
        conff = open(self._config.getProperty(type_conf))
      except:
        print "Not found. : %s" % self._config.getProperty(type_conf)
      else:
        type_prop.load(conff)

    type_prop = type_prop.mergeProperties(name_prop)
    comp.getProperties().mergeProperties(type_prop)
    comp.getProperties().mergeProperties(prop)

    naming_formats = ""
    comp_prop = OpenRTM_aist.Properties(prop=comp.getProperties())

    naming_formats += self._config.getProperty("naming.formats")
    naming_formats += ", " + comp_prop.getProperty("naming.formats")

    naming_formats = OpenRTM_aist.flatten(OpenRTM_aist.unique_sv(OpenRTM_aist.split(naming_formats, ",")))

    naming_names = self.formatString(naming_formats, comp.getProperties())
    comp.getProperties().setProperty("naming.formats",naming_formats)
    comp.getProperties().setProperty("naming.names",naming_names)


  ##
  # @if jp
  # @brief �ץ�ѥƥ�����Υޡ���
  #
  # ���ꤵ�줿�ե�����������ꤵ��Ƥ���ץ�ѥƥ��������ɤ���
  # ��¸������Ѥߥץ�ѥƥ��ȥޡ������롣
  #
  # @param self
  # @param prop �ޡ����оݥץ�ѥƥ�
  # @param file_name �ץ�ѥƥ����󤬵��Ҥ���Ƥ���ե�����̾
  #
  # @return �ޡ��������¹Է��(�ޡ�������:true���ޡ�������:false)
  #
  # @else
  #
  # @endif
  def mergeProperty(self, prop, file_name):
    if file_name == "":
      self._rtcout.RTC_ERROR("Invalid configuration file name.")
      return False

    if file_name[0] != '\0':
      
      try:
        conff = open(file_name)
      except:
        print "Not found. : %s" % file_name
      else:
        prop.load(conff)
        conff.close()
        return True

    return False

  ##
  # @if jp
  # @brief NamingServer ����Ͽ����ݤ���Ͽ������Ȥ�Ω�Ƥ�
  #
  # ���ꤵ�줿�񼰤ȥץ�ѥƥ�������� NameServer ����Ͽ����ݤξ����
  # �Ȥ�Ω�Ƥ롣
  # �ƽ񼰻�����ʸ���ΰ�̣�ϰʲ��ΤȤ���
  # - % : ����ƥ����Ȥζ��ڤ�
  # - n : ���󥹥���̾��
  # - t : ��̾
  # - m : ��̾
  # - v : �С������
  # - V : �٥����
  # - c : ���ƥ���
  # - h : �ۥ���̾
  # - M : �ޥ͡�����̾
  # - p : �ץ���ID
  #
  # @param self
  # @param naming_format NamingService ��Ͽ����񼰻���
  # @param prop ���Ѥ���ץ�ѥƥ�����
  #
  # @return ������Ѵ����
  #
  # @else
  #
  # @endif
  def formatString(self, naming_format, prop):
    name_ = naming_format
    str_  = ""
    count = 0

    for n in name_:
      if n == '%':
        count+=1
        if not (count % 2):
          str_ += n
      else:
        if  count > 0 and (count % 2):
          count = 0
          if   n == "n": str_ += prop.getProperty("instance_name")
          elif n == "t": str_ += prop.getProperty("type_name")
          elif n == "m": str_ += prop.getProperty("type_name")
          elif n == "v": str_ += prop.getProperty("version")
          elif n == "V": str_ += prop.getProperty("vendor")
          elif n == "c": str_ += prop.getProperty("category")
          elif n == "h": str_ += self._config.getProperty("manager.os.hostname")
          elif n == "M": str_ += self._config.getProperty("manager.name")
          elif n == "p": str_ += str(self._config.getProperty("manager.pid"))
          else: str_ += n
        else:
          count = 0
          str_ += n

    return str_


  ##
  # @if jp
  # @brief ���Хåե��μ���
  #
  # �ޥ͡���������ꤷ�����Хåե���������롣
  #
  # @param self
  #
  # @return �ޥ͡���������ꤷ�����Хåե�
  #
  # @else
  #
  # @endif
  def getLogbuf(self):
    return self._rtcout


  ##
  # @if jp
  # @brief �ޥ͡����㥳��ե�����졼�����μ���
  #
  # �ޥ͡���������ꤷ������ե�����졼������������롣
  #
  # @param self
  #
  # @return �ޥ͡�����Υ���ե�����졼�����
  #
  # @else
  #
  # @endif
  def getConfig(self):
    return self._config


  #============================================================
  # ����ݡ��ͥ�ȥޥ͡�����
  #============================================================
  ##
  # @if jp
  # @class InstanceName
  # @brief ObjectManager �����ѥե��󥯥�
  #
  # @else
  #
  # @endif
  class InstanceName:



    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    #
    # @param self
    # @param name �����оݥ���ݡ��ͥ��̾��(�ǥե������:None)
    # @param factory �����оݥե����ȥ�̾��(�ǥե������:None)
    #
    # @else
    #
    # @endif
    def __init__(self, name=None, factory=None):
      if factory:
        self._name = factory.getInstanceName()
      elif name:
        self._name = name

    def __call__(self, factory):
      return self._name == factory.getInstanceName()



  #============================================================
  # ����ݡ��ͥ�ȥե����ȥ�
  #============================================================
  ##
  # @if jp
  # @class FactoryPredicate
  # @brief ����ݡ��ͥ�ȥե����ȥ긡���ѥե��󥯥�
  #
  # @else
  #
  # @endif
  class FactoryPredicate:



    def __init__(self, name=None, factory=None):
      if name:
        self._name = name
      elif factory:
        self._name = factory.profile().getProperty("implementation_id")

    def __call__(self, factory):
      return self._name == factory.profile().getProperty("implementation_id")



  #============================================================
  # ExecutionContext�ե����ȥ�
  #============================================================
  ##
  # @if jp
  # @class FactoryPredicate
  # @brief ExecutionContext�ե����ȥ긡���ѥե��󥯥�
  #
  # @else
  #
  # @endif
  class ECFactoryPredicate:



    def __init__(self, name=None, factory=None):
      if name:
        self._name = name
      elif factory:
        self._name = factory.name()

    def __call__(self, factory):
      return self._name == factory.name()


  #------------------------------------------------------------
  # ORB runner
  #------------------------------------------------------------
  ##
  # @if jp
  # @class OrbRunner
  # @brief OrbRunner ���饹
  #
  # ORB �¹��ѥإ�ѡ����饹��
  #
  # @since 0.4.0
  #
  # @else
  # @class OrbRunner
  # @brief OrbRunner class
  # @endif
  class OrbRunner:



    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    #
    # @param self
    # @param orb ORB
    #
    # @else
    # @brief Constructor
    #
    # @endif
    def __init__(self, orb):
      self._orb = orb
      self._th = threading.Thread(target=self.run)
      self._th.start()
      self._evt = threading.Event()


    def __del__(self):
      self._th.join()


    ##
    # @if jp
    # @brief ORB �¹Խ���
    #
    # ORB �¹�
    #
    # @param self
    #
    # @else
    #
    # @endif
    def run(self):
      try:
        self._orb.run()
        #Manager.instance().shutdown()
        self._evt.set()
      except:
        traceback.print_exception(*sys.exc_info())
        pass
      self._evt.set()
      return


    ##
    # @if jp
    # @brief ORB wait����
    #
    # ORB wait
    #
    # @param self
    #
    # @else
    #
    # @endif
    def wait(self):
      self._evt.wait()

    ##
    # @if jp
    # @brief ORB ��λ����(̤����)
    #
    # ORB ��λ����
    #
    # @param self
    # @param flags ��λ�����ե饰
    #
    # @return ��λ�������
    #
    # @else
    #
    # @endif
    def close(self, flags):
      return 0


  #------------------------------------------------------------
  # Manager Terminator
  #------------------------------------------------------------
  ##
  # @if jp
  # @class Terminator
  # @brief Terminator ���饹
  #
  # ORB ��λ�ѥإ�ѡ����饹��
  #
  # @since 0.4.0
  #
  # @else
  #
  # @endif
  class Terminator:



    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    #
    # @param self
    # @param manager �ޥ͡����㡦���֥�������
    #
    # @else
    # @brief Constructor
    #
    # @endif
    def __init__(self, manager):
      self._manager = manager


    ##
    # @if jp
    # @brief ��λ����
    #
    # ORB���ޥ͡����㽪λ�����򳫻Ϥ��롣
    #
    # @param self
    #
    # @else
    #
    # @endif
    def terminate(self):
      self._manager.shutdown()



  ##
  # @if jp
  # @class Term
  # @brief Term ���饹
  #
  # ��λ�ѥإ�ѡ����饹��
  #
  # @since 0.4.0
  #
  # @else
  #
  # @endif
  class Term:



    def __init__(self):
      self.waiting = 0
      self.mutex   = threading.RLock()
