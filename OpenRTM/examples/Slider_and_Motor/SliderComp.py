#!/usr/bin/env python
# -*- Python -*-

import sys
import time
sys.path.append(".")

import OpenRTM
import RTC

import slider


channels = (
	("motor0", -360, 360, 0.1, 200),
	("motor1", -360, 360, 0.1, 200),
	("motor2", -360, 360, 0.1, 200),
	("motor3", -360, 360, 0.1, 200),
	("motor4", -360, 360, 0.1, 200),
	("motor5", -360, 360, 0.1, 200))

mod_spec = ["implementation_id", "SliderComp", 
	    "type_name", "SliderComp", 
	    "description", "slider component", 
	    "version", "1.0", 
	    "vendor", "Noriaki Ando and Shinji Kurihara", 
	    "category", "Generic", 
	    "activity_type", "DataFlowComponent", 
	    "max_instance", "10", 
	    "language", "Python", 
	    "lang_type""SCRIPT",
	    ""]

sl = slider.SliderMulti(channels)
# thread.start_new_thread(sl.mainloop, ())

class SliderComp(OpenRTM.DataFlowComponentBase):
	def __init__(self, manager):
		OpenRTM.DataFlowComponentBase.__init__(self, manager)
		self._sl_data = RTC.TimedFloatSeq(RTC.Time(0,0), [])
		self._slOut = OpenRTM.OutPort("slider", self._sl_data, OpenRTM.RingBuffer(8))

		self.registerOutPort("slider", self._slOut)
		return
        

	def onActivated(self, ec_id):
		print sl.get()
		time.sleep(1)
		return RTC.RTC_OK


	def onExecute(self, ec_id):
		sl.update()
		self._sl_data.data = sl.get()
		self._slOut.write()
#		time.sleep(0.01)
		return RTC.RTC_OK


	def onShutdown(self, ec_id):
		sl.quit()
		return RTC.RTC_OK



def MyModuleInit(manager):
	profile = OpenRTM.Properties(defaults_str=mod_spec)
	manager.registerFactory(profile,
				SliderComp,
				OpenRTM.Delete)

	# Create a component
	comp = manager.createComponent("SliderComp")

	print "Componet created"


def main():
	# Initialize manager
	mgr = OpenRTM.Manager.init(len(sys.argv), sys.argv)

	# Set module initialization proceduer
	# This procedure will be invoked in activateManager() function.
	mgr.setModuleInitProc(MyModuleInit)

	# Activate manager and register to naming service
	mgr.activateManager()

	# run the manager in blocking mode
	# runManager(False) is the default
	#mgr.runManager()

	# If you want to run the manager in non-blocking mode, do like this
	mgr.runManager(True)
	sl.mainloop()
#	import thread
#	thread.start_new_thread(sl.mainloop, ())
	mgr.runManager(False)



if __name__ == "__main__":
	main()