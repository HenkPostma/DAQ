#!/usr/bin/python

import os
try:
    import comedi
except:
    print "Cannot load comedi module, please install python-libcomedi"

def SetComediDevice():
    if os.path.isfile("/proc/comedi"):
        device = "/dev/comedi0"
        try:
            dev = comedi.comedi_open(device)
            global insubdevice
            insubdevice = comedi.comedi_get_read_subdevice(dev)
        #    print "subdevice for input = " + str(insubdevice)
            global outsubdevice
            outsubdevice = comedi.comedi_get_write_subdevice(dev)
        #    print "subdevice for output = " + str(outsubdevice)

            return "/dev/comedi0"
        except:
            print "cannot open /dev/comedi0, permissions?"
    else:
        return ""

device = SetComediDevice()
print "DAQ device is " + device 
print "subdevice for input = " + str(insubdevice)
print "subdevice for output = " + str(outsubdevice)

#

dev = comedi.comedi_open(device)
comedi.comedi_set_global_oor_behavior(comedi.COMEDI_OOR_NUMBER)
comedi.comedi_close(dev)
