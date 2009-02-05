#/usr/bin/env python
# -*- Python -*-

import sys

import OpenRTM_aist
import RTC

import random
import time

seqout_spec = ["implementation_id", "SeqOut",
               "type_name",         "SequenceOutComponent",
               "description",       "Sequence OutPort component",
               "version",           "1.0",
               "vendor",            "Shinji Kurihara",
               "category",          "example",
               "activity_type",     "DataFlowComponent",
               "max_instance",      "10",
               "language",          "Python",
               "lang_type",         "script",
               ""]



class SeqOut(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._short     = RTC.TimedShort(RTC.Time(0,0),0)
        self._long      = RTC.TimedLong(RTC.Time(0,0),0)
        self._float     = RTC.TimedFloat(RTC.Time(0,0),0)
        self._double    = RTC.TimedDouble(RTC.Time(0,0),0)
        self._shortSeq  = RTC.TimedShortSeq(RTC.Time(0,0),[])
        self._longSeq   = RTC.TimedLongSeq(RTC.Time(0,0),[])
        self._floatSeq  = RTC.TimedFloatSeq(RTC.Time(0,0),[])
        self._doubleSeq = RTC.TimedDoubleSeq(RTC.Time(0,0),[])

        self._shortOut     = OpenRTM_aist.OutPort("Short", self._short, OpenRTM_aist.RingBuffer(8))
        self._longOut      = OpenRTM_aist.OutPort("Long", self._long, OpenRTM_aist.RingBuffer(8))
        self._floatOut     = OpenRTM_aist.OutPort("Float", self._float, OpenRTM_aist.RingBuffer(8))
        self._doubleOut    = OpenRTM_aist.OutPort("Double", self._double, OpenRTM_aist.RingBuffer(8))
        self._shortSeqOut  = OpenRTM_aist.OutPort("ShortSeq", self._shortSeq, OpenRTM_aist.RingBuffer(8))
        self._longSeqOut   = OpenRTM_aist.OutPort("LongSeq", self._longSeq, OpenRTM_aist.RingBuffer(8))
        self._floatSeqOut  = OpenRTM_aist.OutPort("FloatSeq", self._floatSeq, OpenRTM_aist.RingBuffer(8))
        self._doubleSeqOut = OpenRTM_aist.OutPort("DoubleSeq", self._doubleSeq, OpenRTM_aist.RingBuffer(8))


        # Set OutPort buffer
        self.registerOutPort("Short", self._shortOut)
        self.registerOutPort("Long", self._longOut)
        self.registerOutPort("Float", self._floatOut)
        self.registerOutPort("Double", self._doubleOut)

        self.registerOutPort("ShortSeq", self._shortSeqOut)
        self.registerOutPort("LongSeq", self._longSeqOut)
        self.registerOutPort("FloatSeq", self._floatSeqOut)
        self.registerOutPort("DoubleSeq", self._doubleSeqOut)



    def onExecute(self, ec_id):
        shortSeq  = []
        longSeq   = []
        floatSeq  = []
        doubleSeq = []

        self._short.data = int(random.uniform(0, 10))
        self._long.data = int(random.uniform(0, 10))
        self._float.data = float(random.uniform(0.0, 10.0))
        self._double.data = float(random.uniform(0.0, 10.0))

        print "-:  short     long      float            double"
        print "     ", self._short.data, "      ", self._long.data, "   ", self._float.data, "    ", self._double.data
        print "---------------------------------------------------"
        print "                 Sequence Data                     "
        print "---------------------------------------------------"
        for i in range(10):
            shortSeq.append(int(random.uniform(0, 10)))
            longSeq.append(long(random.uniform(0, 10)))
            floatSeq.append(float(random.uniform(0.0, 10.0)))
            doubleSeq.append(float(random.uniform(0.0, 10.0)))
            print str(i), " : ", shortSeq[i], "      ", longSeq[i], "    ", floatSeq[i], "    ", doubleSeq[i]

        # $B%+!<%=%k$N0\F0(B   (^[[nA : n$B9T>e$X0\F0(B)
        print "[A\r[A\r[A\r[A\r[A\r[A\r[A\r[A\r[A\r[A\r[A\r[A\r[A\r[A\r[A\r[A\r"
        
        self._shortSeq.data = shortSeq
        self._longSeq.data = longSeq
        self._floatSeq.data = floatSeq
        self._doubleSeq.data = doubleSeq

        self._shortOut.write()
        self._longOut.write()
        self._floatOut.write()
        self._doubleOut.write()
        self._shortSeqOut.write()
        self._longSeqOut.write()
        self._floatSeqOut.write()
        self._doubleSeqOut.write()

        time.sleep(1)

        return RTC.RTC_OK


def MyModuleInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=seqout_spec)
    manager.registerFactory(profile,
                            SeqOut,
                            OpenRTM_aist.Delete)

    # Create a component
    comp = manager.createComponent("SeqOut")

    print "Component created"


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
