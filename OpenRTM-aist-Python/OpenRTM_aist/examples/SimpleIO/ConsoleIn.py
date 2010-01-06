#!/usr/bin/env python
# -*- Python -*-

import sys

import OpenRTM_aist
import RTC

consolein_spec = ["implementation_id", "ConsoleIn",
                  "type_name",         "ConsoleIn",
                  "description",       "Console input component",
                  "version",           "1.0",
                  "vendor",            "Shinji Kurihara",
                  "category",          "example",
                  "activity_type",     "DataFlowComponent",
                  "max_instance",      "10",
                  "language",          "Python",
                  "lang_type",         "script",
                  ""]


class DataListener(OpenRTM_aist.ConnectorDataListenerT):
    def __init__(self, name):
        self._name = name

    def __del__(self):
        print "dtor of ", self._name

    def __call__(self, info, cdrdata):
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedLong(RTC.Time(0,0),0))
        print "------------------------------"
        print "Listener:       ", self._name
        print "Profile::name:  ", info.name
        print "Profile::id:    ", info.id
        print "Data:           ", data.data
        print "------------------------------"




class ConsoleIn(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._data = RTC.TimedLong(RTC.Time(0,0),0)
        self._outport = OpenRTM_aist.OutPort("out", self._data)


    def onInitialize(self):
        # Set OutPort buffer
        self.registerOutPort("out", self._outport)

        self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,
                                               DataListener("ON_BUFFER_WRITE"))
        self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_FULL, 
                                               DataListener("ON_BUFFER_FULL"))
        self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE_TIMEOUT, 
                                               DataListener("ON_BUFFER_WRITE_TIMEOUT"))
        self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_OVERWRITE, 
                                               DataListener("ON_BUFFER_OVERWRITE"))
        self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_READ, 
                                               DataListener("ON_BUFFER_READ"))
        self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_SEND, 
                                               DataListener("ON_SEND"))
        self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED,
                                               DataListener("ON_RECEIVED"))
        self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_FULL, 
                                               DataListener("ON_RECEIVER_FULL"))
        self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_TIMEOUT, 
                                               DataListener("ON_RECEIVER_TIMEOUT"))
        self._outport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_ERROR,
                                               DataListener("ON_RECEIVER_ERROR"))

        return RTC.RTC_OK

        
    def onExecute(self, ec_id):
        print "Please input number: ",
        self._data.data = long(sys.stdin.readline())
        OpenRTM_aist.setTimestamp(self._data)
        print "Sending to subscriber: ", self._data.data
        self._outport.write()
        return RTC.RTC_OK


def MyModuleInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=consolein_spec)
    manager.registerFactory(profile,
                            ConsoleIn,
                            OpenRTM_aist.Delete)

    # Create a component
    comp = manager.createComponent("ConsoleIn")

def main():
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)

    # Set module initialization proceduer
    # This procedure will be invoked in activateManager() function.
    mgr.setModuleInitProc(MyModuleInit)

    # Activate manager and register to naming service
    mgr.activateManager()

    # run the manager in blocking mode
    # runManager(False) is the default
    mgr.runManager()

    # If you want to run the manager in non-blocking mode, do like this
    # mgr.runManager(True)

if __name__ == "__main__":
	main()
