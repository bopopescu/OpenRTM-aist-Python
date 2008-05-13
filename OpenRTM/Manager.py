#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file Manager.py
 \brief RTComponent manager class
 \date $Date: $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""

import threading
import string
import signal, os
import sys
import traceback
import time
from omniORB import CORBA

import OpenRTM
import RTC
import SDOPackage



#------------------------------------------------------------
# static var
#------------------------------------------------------------
"""
 \var manager  The pointer to the Manager
"""
manager = None

"""
 \var mutex The mutex of the pointer to the Manager 
"""
mutex = threading.RLock()


def handler(signum, frame):
	mgr = OpenRTM.Manager.instance()
	mgr.terminate()


class ScopedLock:

	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()


class Manager:

	def __init__(self, _manager=None):
		"""
		\if jp
		\brief Protected ���ԡ����󥹥ȥ饯��
		\param _manager(OpenRTM.Manager)
		\else
		\brief Protected Copy Constructor
		\param _manager(OpenRTM.Manager)
		\endif
		"""
		self._initProc   = None
		self._runner     = None
		self._terminator = None
		self._compManager = OpenRTM.ObjectManager(self.InstanceName)
		self._factory = OpenRTM.ObjectManager(self.FactoryPredicate)
		self._ecfactory = OpenRTM.ObjectManager(self.ECFactoryPredicate)
		self._terminate = self.Term()
		self._ecs = []
		self._timer = None
		signal.signal(signal.SIGINT, handler)
			
		return


	def init(argc, argv):
		"""
		\if jp
		\brief �ޥ͡�����ν����

		�ޥ͡�������������� static ���дؿ���
		�ޥ͡�����򥳥ޥ�ɥ饤�������Ϳ���ƽ�������롣
		�ޥ͡��������Ѥ�����ϡ�ɬ�����ν�������дؿ� init() ��
		�ƤФʤ���Фʤ�ʤ���
		�ޥ͡�����Υ��󥹥��󥹤����������ˡ�Ȥ��ơ�init(), instance() ��
		2�Ĥ� static ���дؿ����Ѱդ���Ƥ��뤬���������init()�Ǥ���
		�Ԥ��ʤ����ᡢManager ����¸���֤ΰ��ֺǽ�ˤ�init()��Ƥ�ɬ�פ����롣

		���ޥ͡�����ν��������
		- initManager: ����������config�ե�������ɤ߹��ߡ����֥����ƥ�����
		- initLogger: Logger�����
		- initORB: ORB �����
		- initNaming: NamingService �����
		- initExecutionContext: ExecutionContext factory �����
		- initTimer: Timer �����

		\param argc ���ޥ�ɥ饤������ο�
		\param argv ���ޥ�ɥ饤�����

		\else
		\brief Initializa manager

		This is the static member function to tintialize the Manager.
		The Manager is initialized by given arguments.
		At the starting the manager, this static member function "must" be
		called from application program. The manager has two static functions
		to get the instance, "init()" and "instance()". Since initializing
		process is only performed by the "init()" function, the "init()" has
		to be called at the beginning of the lifecycle of the Manager.
		function.

		\param argc The number of command line argument. 
		\param argv The array of the command line arguments.

		\endif
		"""
		global manager
		global mutex
		
		if not manager:
			guard = ScopedLock(mutex)
			if not manager:
				manager = Manager()
				manager.initManager(argc, argv)
				manager.initLogger()
				manager.initORB()
				manager.initNaming()
				manager.initExecContext()
				manager.initTimer()

		return manager
	
	init = staticmethod(init)


	def instance():
		"""
		\if jp
		\brief �ޥ͡�����Υ��󥹥��󥹤μ���
    
		�ޥ͡�����Υ��󥹥��󥹤�������� static ���дؿ���
		���δؿ���Ƥ����ˡ�ɬ�����ν�������дؿ� init() ���ƤФ�Ƥ���
		ɬ�פ����롣
		
		\return Manager ��ͣ��Υ��󥹥��󥹤λ���
		
		\else
	
		\brief Get instance of the manager
		
		This is the static member function to get the instance of the Manager.
		Before calling this function, ensure that the initialization function
		"init()" is called.
		
		\return The only instance reference of the manager
		
		\endif
		"""
		global manager
		global mutex
		
		if not manager:
			guard = ScopedLock(mutex)
			if not manager:
				manager = Manager()
				manager.initManager(0, None)
				manager.initLogger()
				manager.initORB()
				manager.initNaming()
				manager.initExecContext()
				manager.initTimer()

		return manager

	instance = staticmethod(instance)


	def terminate(self):
		if self._terminator != None:
			self._terminator.terminate()

	
	def shutdown(self):
		self._rtcout.RTC_DEBUG("Manager::shutdown()")
		self.shutdownComponents()
		self.shutdownNaming()
		self.shutdownORB()
		self.shutdownManager()

		if self._runner != None:
			self._runner.wait()
		else:
			self.join()

		self.shutdownLogger()
	
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


	def setModuleInitProc(self, proc):
		"""
		\if jp
		\brief ������ץ�������Υ��å�
		
		���Υ��ڥ졼�����ϥ桼�����Ԥ��⥸�塼�����ν�����ץ�������
		�����ꤹ�롣���������ꤵ�줿�ץ�������ϡ��ޥ͡����㤬��������졢
		�����ƥ��ֲ����줿�塢Ŭ�ڤʥ����ߥ󥰤Ǽ¹Ԥ���롣
		\param proc ������ץ�������δؿ��ݥ���
		\else
		\brief Run the Manager
		
		This operation sets the initial procedure call to process module
		initialization, other user defined initialization and so on.
		The given procedure will be called at the proper timing after the 
		manager initialization, activation and run.
		\param proc A function pointer to the initial procedure call
		\endif
		"""
		self._initProc = proc
		return


	def activateManager(self):
		"""
		\if jp
		\brief Manager�Υ����ƥ��ֲ�
		
		���Υ��ڥ졼�����ϰʲ��ν�����Ԥ�
		- CORBA POAManager �Υ����ƥ��ֲ�
		- �ޥ͡�����CORBA���֥������ȤΥ����ƥ��ֲ�
		- Manager ���֥������ȤؤΥ��֥������Ȼ��Ȥ���Ͽ
		
		���Υ��ڥ졼�����ϡ��ޥ͡�����ν�����塢runManager()
		�����˸Ƥ�ɬ�פ����롣
		\else
		\brief Activate Manager
		
		This operation do the following,
		- Activate CORBA POAManager
		- Activate Manager CORBA object
		- Bind object reference of the Manager to the nameserver
		
		This operationo should be invoked after Manager:init(),
		and before tunManager().
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::activateManager()")

		try:
			self.getPOAManager().activate()
			if self._initProc != None:
				self._initProc(self)
		except:
			print "Exception: Manager.activateManager()"
			return False

		return True


	def runManager(self, no_block=None):
		"""
		\if jp
		\brief Manager�μ¹�

		���Υ��ڥ졼�����ϥޥ͡�����Υᥤ��롼�פ�¹Ԥ��롣
		���Υᥤ��롼����Ǥϡ�CORBA ORB�Υ��٥�ȥ롼������
		��������롣�ǥե���ȤǤϡ����Υ��ڥ졼�����ϥ֥�å�����
		Manager::destroy() ���ƤФ��ޤǽ������ᤵ�ʤ���
		���� no_block �� true �����ꤵ��Ƥ�����ϡ������ǥ��٥�ȥ롼��
		��������륹��åɤ�ư�����֥�å������˽������᤹��
		\param no_block(bool) false: �֥�å��󥰥⡼��, true: �Υ�֥�å��󥰥⡼��
		\else
		\brief Run the Manager

		This operation processes the main event loop of the Manager.
		In this main loop, CORBA's ORB event loop or other processes
		are performed. As the default behavior, this operation is going to
		blocking mode and never returns until manager::destroy() is called.
		When the given argument "no_block" is set to "true", this operation
		creates a thread to process the event loop internally, and it doesn't
		block and returns.
		\param no_block(bool) false: Blocking mode, true: non-blocking mode.
		\endif
		"""
		if no_block == None:
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


	def load(self, fname, initfunc):
		"""
		\if jp
		\brief [CORBA interface] �⥸�塼��Υ���
		
		����ݡ��ͥ�ȤΥ⥸�塼�����ɤ��ƽ�����ؿ���¹Ԥ��롣
		
		\param fname(string)   �⥸�塼��ե�����̾
		\param initfunc(string) ������ؿ�̾
		
		\else
		
		\brief [CORBA interface] Load module
		
		Load module (shared library, DLL etc..) by file name,
		and invoke initialize function.
		
		\param fname(string)    The module file name
		\param initfunc(string) The initialize function name
		
		\endif
		"""  
		self._rtcout.RTC_DEBUG("Manager::load()")
		self._module.load(fname, initfunc)
		return


	def unload(self, fname):
		"""
		\if jp
		\brief �⥸�塼��Υ������
		
		�⥸�塼��򥢥���ɤ���
		\param fname(string) �⥸�塼��Υե�����̾
		\else
		\brief Unload module
		
		Unload shared library.
		\param fname(string) Module file name
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::unload()")
		self._module.unload(fname)
		return


	def unloadAll(self):
		"""
		\if jp
		\brief ���⥸�塼��Υ������
		
		�⥸�塼��򤹤٤ƥ�����ɤ���
		\else
		\brief Unload module
		
		Unload all loaded shared library.
		\endif
		""" 
		self._rtcout.RTC_DEBUG("Manager::unloadAll()")
		self._module.unloadAll()
		return


	def getLoadedModules(self):
		"""
		\if jp
		\brief ���ɺѤߤΥ⥸�塼��ꥹ�Ȥ��������
		\else
		\brief Get loaded module names
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::getLoadedModules()")
		return self._module.getLoadedModules()


	def getLoadableModules(self):
		"""
		\if jp
		\brief ���ɲ�ǽ�ʥ⥸�塼��ꥹ�Ȥ��������
		\else
		\brief Get loadable module names
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::getLoadableModules()")
		return self._module.getLoadableModules()


    #============================================================
    # Component Factory Management
    #============================================================

	def registerFactory(self, profile, new_func, delete_func):
		"""
		\if jp
		\brief RT����ݡ��ͥ�ȥե����ȥ����Ͽ����
		\param profile(OpenRTM.Properties)
		\param new_func(create function object)
		\param delete_func(delete function object)
		\else
		\brief Register RT-Component Factory
		\param profile(OpenRTM.Properties)
		\param new_func(create function object)
		\param delete_func(delete function object)
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::registerFactory(%s)", profile.getProperty("type_name"))
		try:
			factory = OpenRTM.FactoryPython(profile, new_func, delete_func)
			self._factory.registerObject(factory)
			return True
		except:
			return False

	
	def registerECFactory(self, name, new_func, delete_func):
		"""
		\if jp
		\brief ExecutionContext�ե����ȥ����Ͽ����
		\param name(string)
		\param new_func(create function object)
		\param delete_func(delete function object)
		\else
		\brief Register ExecutionContext Factory
		\param name(string)
		\param new_func(create function object)
		\param delete_func(delete function object)
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::registerECFactory(%s)", name)
		try:
			self._ecfactory.registerObject(OpenRTM.ECFactoryPython(name, new_func, delete_func))
			return True
		except:
			return False

		return False


	def getModulesFactories(self):
		"""
		\if jp
		\brief �ե����ȥ����ꥹ�Ȥ��������
		\else
		\brief Get the list of all RT-Component Factory
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::getModulesFactories()")

		return self._factory.for_each(self.ModuleFactories)._modlist

    
    #============================================================
    # Component management
    #============================================================

	def createComponent(self, module_name):
		"""
		\if jp
		\brief RT����ݡ��ͥ�Ȥ���������
		\param module_name(string)
		\else
		\brief Create RT-Component
		\param module_name(string)
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::createComponent(%s)", module_name)

		obj = self._factory.find(module_name)
		comp = obj.create(self)
		if comp == None:
			return None
		self._rtcout.RTC_DEBUG("RTC Created: %s", module_name)

		self.configureComponent(comp)

		if comp.initialize() != RTC.RTC_OK:
			self._rtcout.RTC_DEBUG("RTC initialization failed: %s", module_name)
			comp.exit()
			self._rtcout.RTC_DEBUG("%s was finalized", module_name)
			return None

		self._rtcout.RTC_DEBUG("RTC initialization succeeded: %s", module_name)
		self.bindExecutionContext(comp)
		self.registerComponent(comp)
		return comp


	def registerComponent(self, comp):
		"""
		\if jp
		\brief RT����ݡ��ͥ�Ȥ�ľ�� Manager ����Ͽ����
		\param comp(OpenRTM.RTObject_impl)
		\else
		\brief Register RT-Component directly without Factory
		\param comp(OpenRTM.RTObject_impl)
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::registerComponent(%s)", comp.getInstanceName())

		self._compManager.registerObject(comp)
		names = comp.getNamingNames()

		for name in names:
			self._rtcout.RTC_DEBUG("Bind name: %s", name)
			self._namingManager.bindObject(name, comp)

		return True

	
	def unregisterComponent(self, comp):
		"""
		\if jp
		\brief RT����ݡ��ͥ�Ȥ�ľ�� Manager ����������
		\param comp(OpenRTM.RTObject_impl)
		\else
		\brief Unregister RT-Component directly without Factory
		\param comp(OpenRTM.RTObject_impl)
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::unregisterComponent(%s)", comp.getInstanceName())
		self._compManager.unregisterObject(comp.getInstanceName())
		names = comp.getNamingNames()
		
		for name in names:
			self._rtcout.RTC_DEBUG("Unbind name: %s", name)
			self._namingManager.unbindObject(name)

		return True


	def bindExecutionContext(self, comp):
		"""
		\if jp
		\brief ExecutionContext��RT���֥������Ȥ�Х���ɤ��롣
		\param comp(OpenRTM.RTObject_impl)
		\else
		\brief Bind RTObject to ExcecutionContext
		\param comp(OpenRTM.RTObject_impl)
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::bindExecutionContext()")
		self._rtcout.RTC_DEBUG("ExecutionContext type: %s",
							   self._config.getProperty("exec_cxt.periodic.type"))

		rtobj = comp.getObjRef()

		exec_cxt = None

		if OpenRTM.isDataFlowParticipant(rtobj):
			ectype = self._config.getProperty("exec_cxt.periodic.type")
			exec_cxt = self._ecfactory.find(ectype).create()
			rate = self._config.getProperty("exec_cxt.periodic.rate")
			exec_cxt.set_rate(float(rate))
		else:
			ectype = self._config.getProperty("exec_cxt.evdriven.type")
			exec_cxt = self._ecfactory.find(ectype).create()
		exec_cxt.add(rtobj)
		exec_cxt.start()
		self._ecs.append(exec_cxt)
		return True


	def deleteComponent(self, instance_name):
		"""
		\if jp
		\brief Manager ����Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ�������
		\param instance_name(string)
		\else
		\brief Unregister RT-Component that is registered in the Manager
		\param instance_name(string)
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::deleteComponent(%s)", instance_name)


	def getComponent(self, instance_name):
		"""
		\if jp
		\brief Manager ����Ͽ����Ƥ���RT����ݡ��ͥ�Ȥ��������
		\param instance_name(string)
		\else
		\brief Get RT-Component's pointer
		\param instance_name(string)
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::getComponent(%s)", instance_name)
		return self._compManager.find(instance_name)


	def getComponents(self):
		"""
		\if jp
		\brief Manager ����Ͽ����Ƥ�����RT����ݡ��ͥ�Ȥ��������
		\else
		\brief Get all RT-Component's pointer
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::getComponents()")
		return self._compManager.getObjects()


    #============================================================
    # CORBA ��Ϣ
    #============================================================

	def getORB(self):
		"""
		\if jp
		\brief ORB �Υݥ��󥿤��������
		\else
		\brief Get the pointer to the ORB
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::getORB()")
		return self._orb


	def getPOA(self):
		"""
		\if jp
		\brief Manager ������ RootPOA �Υݥ��󥿤��������
		\else
		\brief Get the pointer to the RootPOA 
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::getPOA()")
		return self._poa

	
	def getPOAManager(self):
		self._rtcout.RTC_DEBUG("Manager::getPOAManager()")
		return self._poaManager


    
    #============================================================
    # Manager initialize and finalization
    #============================================================

	def initManager(self, argc, argv):
		"""
		\if jp
		\brief Manager ���������������
		\else
		\brief Manager internal initialization
		\endif
		"""
		config = OpenRTM.ManagerConfig(argc, argv)
		self._config = config.configure(OpenRTM.Properties())
		self._config.setProperty("logger.file_name",self.formatString(self._config.getProperty("logger.file_name"), self._config))

		self._module = OpenRTM.ModuleManager(self._config)
		self._terminator = self.Terminator(self)
		guard = ScopedLock(self._terminate.mutex)
		self._terminate.waiting = 0
		del guard

		if OpenRTM.toBool(self._config.getProperty("timer.enable"), "YES", "NO", True):
			tm = OpenRTM.TimeValue(0, 100000)
			tick = self._config.getProperty("timer.tick")
			if tick != "":
				tm = tm.set_time(float(tick))
				self._timer = OpenRTM.Timer(tm)
				self._timer.start()


	def shutdownManager(self):
		"""
		\if jp
		\brief Manager �ν�λ����
		\else
		\brief Manager internal finalization
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::shutdownManager()")
		if self._timer:
			self._timer.stop()
	

    #============================================================
    # Logger initialize and terminator
    #============================================================

	def initLogger(self):
		"""
		\if jp
		\brief System logger �ν����
		\else
		\brief System logger initialization
		\endif
		"""

		logfile = self._config.getProperty("logger.file_name")
		if logfile == "":
			logfile = "./rtc.log"
			

		if OpenRTM.toBool(self._config.getProperty("logger.enable"), "YES", "NO", True):
			self._Logbuf = OpenRTM.Logbuf(fileName = logfile)
			self._rtcout = OpenRTM.LogStream(self._Logbuf)
			self._rtcout.setLogLevel(self._config.getProperty("logger.log_level"))
			self._rtcout.setLogLock(OpenRTM.toBool(self._config.getProperty("logger.stream_lock"),
												  "enable", "disable", False))

			self._rtcout.RTC_INFO("%s", self._config.getProperty("openrtm.version"))
			self._rtcout.RTC_INFO("Copyright (C) 2003-2007")
			self._rtcout.RTC_INFO("  Noriaki Ando")
			self._rtcout.RTC_INFO("  Task-intelligence Research Group,")
			self._rtcout.RTC_INFO("  Intelligent Systems Research Institute, AIST")
			self._rtcout.RTC_INFO("Manager starting.")
			self._rtcout.RTC_INFO("Starting local logging.")
		else:
			self._rtcout = OpenRTM.LogStream()

		return True


	def shutdownLogger(self):
		"""
		\if jp
		\brief System Logger �ν�λ����
		\else
		\brief System Logger finalization
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::shutdownLogger()")
	

    #============================================================
    # ORB initialization and finalization
    #============================================================

	def initORB(self):
		"""
		\if jp
		\brief CORBA ORB �ν��������
		\else
		\brief CORBA ORB initialization
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::initORB()")

		try:
			args = OpenRTM.split(self.createORBOptions(), " ")
			argv = OpenRTM.toArgv(args)
			argc = len(args)
			self._orb = CORBA.ORB_init(argv)

			self._poa = self._orb.resolve_initial_references("RootPOA")

			if CORBA.is_nil(self._poa):
				self._rtcout.RTC_ERROR("Could not resolve RootPOA")
				return False

			self._poaManager = self._poa._get_the_POAManager()
			self._objManager = OpenRTM.CorbaObjectManager(self._orb, self._poa)
		except:
			self._rtcout.RTC_ERROR("Exception: Caught unknown exception in initORB().")
			return False

		return True


	def createORBOptions(self):
		"""
		\if jp
		\brief ORB �Υ��ޥ�ɥ饤�󥪥ץ�������
		\else
		\brief ORB command option creation
		\endif
		"""
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


	def shutdownORB(self):
		"""
		\if jp
		\brief ORB �ν�λ����
		\else
		\brief ORB finalization
		\endif
		"""
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

	def initNaming(self):
		"""
		\if jp
		\brief NamingManager �ν����
		\else
		\brief NamingManager initialization
		\endif
		"""
		self._rtcout.RTC_DEBUG("Manager::initNaming()")
		self._namingManager = OpenRTM.NamingManager(self)

		if not OpenRTM.toBool(self._config.getProperty("naming.enable"), "YES", "NO", True):
			return True

		meths = OpenRTM.split(self._config.getProperty("naming.type"),",")
		
		for meth in meths:
			names = OpenRTM.split(self._config.getProperty(meth+".nameservers"), ",")
			for name in names:
				self._rtcout.RTC_DEBUG("Register Naming Server: %s/%s", (meth, name))
				self._namingManager.registerNameServer(meth,name)

		if OpenRTM.toBool(self._config.getProperty("naming.update.enable"), "YES", "NO", True):
			tm = OpenRTM.TimeValue(10,0)
			intr = self._config.getProperty("naming.update.interval")
			if intr != "":
				tm = OpenRTM.TimeValue(intr)

			if self._timer:
				self._timer.registerListenerObj(self._namingManager,OpenRTM.NamingManager.update,tm)
	
		return True


	def shutdownNaming(self):
		self._rtcout.RTC_DEBUG("Manager::shutdownNaming()")
		self._namingManager.unbindAll()


	def initExecContext(self):
		self._rtcout.RTC_DEBUG("Manager::initExecContext()")
		OpenRTM.PeriodicExecutionContextInit(self)
		OpenRTM.ExtTrigExecutionContextInit(self)
		return True


	def initTimer(self):
		return True


	def shutdownComponents(self):
		self._rtcout.RTC_DEBUG("Manager::shutdownComponents()")
		comps = self._namingManager.getObjects()
		for comp in comps:
			try:
				comp.exit()
				p = OpenRTM.Properties(key=comp.getInstanceName())
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


	def cleanupComponent(self, comp):
		"""
		 \brief ����ݡ��ͥ�ȥ��֥������Ȥκ��
		 \param comp(OpenRTM.RTObject_impl)
		"""
		self._rtcout.RTC_DEBUG("Manager::cleanupComponents")
		self.unregisterComponent(comp)

			
    
	def configureComponent(self, comp):
		"""
		 \brief ����ݡ��ͥ�ȥ��֥������Ȥ�����
		 \param comp(OpenRTM.RTObject_impl)
		"""
		category  = comp.getCategory()
		type_name = comp.getTypeName()
		inst_name = comp.getInstanceName()

		type_conf = category + "." + type_name + ".config_file"
		name_conf = category + "." + inst_name + ".config_file"

		type_prop = OpenRTM.Properties()

		name_prop = OpenRTM.Properties()

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

		naming_formats = ""
		comp_prop = OpenRTM.Properties(prop=comp.getProperties())

		naming_formats += self._config.getProperty("naming.formats")
		naming_formats += ", " + comp_prop.getProperty("naming.formats")

		naming_formats = OpenRTM.flatten(OpenRTM.unique_sv(OpenRTM.split(naming_formats, ",")))

		naming_names = self.formatString(naming_formats, comp.getProperties())
		comp.getProperties().setProperty("naming.formats",naming_formats)
		comp.getProperties().setProperty("naming.names",naming_names)




	def mergeProperty(self, prop, file_name):
		"""
		 \brief �ץ�ѥƥ��Υޡ���
		 \param prop(OpenRTM.Properties)
		 \param file_name(string)
		"""
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

	
	def formatString(self, naming_format, prop):
		"""
		 \brief configuration���ץ����Υޥåԥ�
		 \param naming_format(string)
		 \param prop(OpenRTM.Properties)
		"""
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


	def getLogbuf(self):
		return self._rtcout

	
	def getConfig(self):
		return self._config
    
    

    #============================================================
    # ����ݡ��ͥ�ȥޥ͡�����
    #============================================================
    # ObjectManager ���Ϥ��Ҹ쥯�饹
	class InstanceName:
		def __init__(self, name=None, factory=None):
			if factory != None:
				self._name = factory.getInstanceName()
			elif name != None:
				self._name = name

		#def func(self, factory):
		def __call__(self, factory):
			return self._name == factory.getInstanceName()


    #============================================================
    # ����ݡ��ͥ�ȥե����ȥ�
    #============================================================
    # ����ݡ��ͥ�ȥե����ȥ���Ϥ��Ҹ쥯�饹
	class FactoryPredicate:
		def __init__(self, name=None, factory=None):
			if name != None:
				self._name = name
			elif factory != None:
				self._name = factory.profile().getProperty("implementation_id")

		#def func(self, factory):
		def __call__(self, factory):
			return self._name == factory.profile().getProperty("implementation_id")


    #============================================================
    # ExecutionContext�ե����ȥ�
    #============================================================
    # EC�ե����ȥ���Ϥ��Ҹ쥯�饹
	class ECFactoryPredicate:
		def __init__(self, name=None, factory=None):
			if name != None:
				self._name = name
			elif factory != None:
				self._name = factory.name()

		#def func(self, factory):
		def __call__(self, factory):
			return self._name == factory.name()

		

    # �ե����ȥ�̾��ꥹ�ȥ��åפ��뤿��Υե��󥯥�
	class ModuleFactories:
		def __init__(self):
			self._modlist = []
			pass
		
		#def func(self, f):
		def __call__(self, f):
			self._modlist.append(f.profile().getProperty("implementation_id"))


    #------------------------------------------------------------
    # ORB runner
    #------------------------------------------------------------
	class OrbRunner:

		def __init__(self, orb):
			self._orb = orb
			self._th = threading.Thread(target=self.run)
			self._th.start()
			self._evt = threading.Event()

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

		def wait(self):
			self._evt.wait()

		def close(self, flags):
			return 0


    #------------------------------------------------------------
    # Manager Terminator
    #------------------------------------------------------------
	class Terminator:

		def __init__(self, manager):
			self._manager = manager


		def terminate(self):
			self._manager.shutdown()

	
	class Term:
		def __init__(self):
			self.waiting = 0
			self.mutex   = threading.RLock()
