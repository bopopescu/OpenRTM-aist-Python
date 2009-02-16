#!/usr/bin/env python
# -*- Python -*-

import sys
import time
sys.path.append(".")

# Import RTM module
import OpenRTM_aist
import RTC

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
AutoControl_spec = ["implementation_id", "AutoControl", 
		    "type_name",         "AutoControl", 
		    "description",       "Auto controller component for MobileRobot", 
		    "version",           "1.0.0", 
		    "vendor",            "AIST", 
		    "category",          "example", 
		    "activity_type",     "DataFlowComponent", 
		    "max_instance",      "1", 
		    "language",          "Python", 
		    "lang_type",         "SCRIPT",
		    "conf.default.velocity", "80.0",
		    "conf.default.turn_velocity", "80.0",
		    "conf.default.distance_to_env", "40.0",
		    ""]
# </rtc-template>

class AutoControl(OpenRTM_aist.DataFlowComponentBase):
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_sens = RTC.TimedFloatSeq(RTC.Time(0,0),[])
		self._sensIn = OpenRTM_aist.InPort("sens", self._d_sens, OpenRTM_aist.RingBuffer(8))
		self._d_vel = RTC.TimedFloatSeq(RTC.Time(0,0),[])
		self._velOut = OpenRTM_aist.OutPort("vel", self._d_vel, OpenRTM_aist.RingBuffer(8))
		
		# Set InPort buffers
		self.registerInPort("sens",self._sensIn)
		
		# Set OutPort buffers
		self.registerOutPort("vel",self._velOut)

		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		self._velocity = [80.0]
		self._turn_velocity = [80.0]
		self._distance_to_env = [40.0]
		

		 
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("velocity", self._velocity, "80.0")
		self.bindParameter("turn_velocity", self._turn_velocity, "80.0")
		self.bindParameter("distance_to_env", self._distance_to_env, "40.0")
		
		return RTC.RTC_OK


	
	def onActivated(self, ec_id):
		self._d_vel.data  = [0.0, 0.0]
		self._velOut.write()
		return RTC.RTC_OK
	
	def onDeactivated(self, ec_id):
		self._d_vel.data  = [0.0, 0.0]
		self._velOut.write()
		return RTC.RTC_OK
	
	def onExecute(self, ec_id):
		if self._sensIn.isNew():
			self._d_sens = self._sensIn.read()
			self._d_vel.data  = self.calcVel()
			self._velOut.write()
			time.sleep(0.1)
			return RTC.RTC_OK

		time.sleep(0.1)
		return RTC.RTC_OK
		
	

	def calcVel(self):
		if self._d_sens.data[3] <= self._distance_to_env[0]:
			return [self._turn_velocity[0], -(self._turn_velocity[0])]

		elif self._d_sens.data[3] > self._distance_to_env[0]:
			return [self._velocity[0] for i in range(2)]
		else:
			return [0.0 for i in range(2)]
		
		

def MyModuleInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=AutoControl_spec)
    manager.registerFactory(profile,
                            AutoControl,
                            OpenRTM_aist.Delete)

    # Create a component
    comp = manager.createComponent("AutoControl")



def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()
