#!/usr/bin/python

#set the paths so python can find the comedi module
import sys, os, string, struct, time, mmap, array
import comedi as c
import numpy

#open a comedi device
dev=c.comedi_open('/dev/comedi0')
device = dev
if not dev: 
    raise "Error openning Comedi device"

#get a file-descriptor for use later
fd = c.comedi_fileno(dev)
if fd<=0: 
    raise "Error obtaining Comedi device file descriptor"

freq=50000 # as defined in demo/common.c
subdevice=0 #as defined in demo/common.c
secs = 3 # used to stop scan after "secs" seconds
packetSize = 512

#three lists containing the chans, gains and referencing
#the lists must all have the same length
#~ chans=[0,1,2,3]
#~ gains=[0,0,0,0]
#~ aref =[c.AREF_GROUND, c.AREF_GROUND, c.AREF_GROUND, c.AREF_GROUND]

#nchans = 16
nchans = 2

chans= range(nchans)
gains= [ 0 for i in chans ]
aref =[c.AREF_GROUND for i in chans ]

cmdtest_messages = [
    "success",
    "invalid source",
    "source conflict",
    "invalid argument",
    "argument conflict",
    "invalid chanlist"]


#wrappers include a "chanlist" object (just an Unsigned Int array) for holding the chanlist information
mylist = c.chanlist(nchans) #create a chanlist of length nchans

#now pack the channel, gain and reference information into the chanlist object
#N.B. the CR_PACK and other comedi macros are now python functions
for index in range(nchans):
    mylist[index]=c.cr_pack(chans[index], gains[index], aref[index])

size = c.comedi_get_buffer_size(dev, subdevice)
print "buffer size is ", size

map = mmap.mmap(fd, size, mmap.MAP_SHARED, mmap.PROT_READ)
print "map = ", map

def dump_cmd(cmd):
    print "---------------------------"
    print "command structure contains:"
    print "cmd.subdev : ", cmd.subdev
    print "cmd.flags : ", cmd.flags
    print "cmd.start :\t", cmd.start_src, "\t", cmd.start_arg
    print "cmd.scan_beg :\t", cmd.scan_begin_src, "\t", cmd.scan_begin_arg
    print "cmd.convert :\t", cmd.convert_src, "\t", cmd.convert_arg
    print "cmd.scan_end :\t", cmd.scan_end_src, "\t", cmd.scan_end_arg
    print "cmd.stop :\t", cmd.stop_src, "\t", cmd.stop_arg
    print "cmd.chanlist : ", cmd.chanlist
    print "cmd.chanlist_len : ", cmd.chanlist_len
    print "cmd.data : ", cmd.data
    print "cmd.data_len : ", cmd.data_len
    print "---------------------------"

def prepare_cmd(dev, subdev, C):
    #global cmd
    C.subdev = subdev
    C.flags = 0
    C.start_src = c.TRIG_NOW
    C.start_arg = 0
    C.scan_begin_src = c.TRIG_FOLLOW
    C.scan_begin_arg = 0
    C.convert_src = c.TRIG_TIMER
    C.convert_arg = int(1e9/freq/16)
    C.scan_end_src = c.TRIG_COUNT
    C.scan_end_arg = nchans
    C.stop_src = c.TRIG_NONE
    C.stop_arg = 0
    C.chanlist = mylist
    C.chanlist_len = nchans

## ret = c.comedi_get_buffer_size(dev, subdevice)
## if ret==-1:
## 	raise "Error fetching comedi buffer size"
## else:
## 	print "buffer size = ", ret
## ret = c.comedi_get_max_buffer_size(dev, subdevice)
## if ret==-1:
## 	raise "Error fetching comedi max buff size"
## else:
## 	print "max buff size = ", ret
#construct a comedi command
cmd = c.comedi_cmd_struct()
cmd.chanlist = mylist # adjust for our particular context
cmd.chanlist_len = nchans
cmd.scan_end_arg = nchans

prepare_cmd(dev,subdevice,cmd)

print "command before testing"
dump_cmd(cmd)

#test our comedi command a few times. 
ret = c.comedi_command_test(dev,cmd)
print "first cmd test returns ", ret, cmdtest_messages[ret]
if ret<0:
    raise "comedi_command_test failed"
dump_cmd(cmd)

ret = c.comedi_command_test(dev,cmd)
print "second test returns ", ret, cmdtest_messages[ret]
if ret<0:
    raise "comedi_command_test failed"
if ret !=0:
    dump_cmd(cmd)
    raise "ERROR preparing command"
dump_cmd(cmd)

front = 0
back = 0

flag = 1

time_limit = nchans*freq*2*secs # stop scan after "secs" seconds
print 'time_limit' , time_limit
t0 = time.time()

pause = float(packetSize)/nchans/freq/4
print 'pause' , pause

alldata = numpy.empty((time_limit/2) , dtype = 'i2')

ret = c.comedi_command(dev,cmd)
if ret<0:
    raise "error executing comedi_command"


while flag:
    print 'buffer offset', c.comedi_get_buffer_offset(device, subdevice)
    print '	buffer contents', c.comedi_get_buffer_contents(device, subdevice)	
    front += c.comedi_get_buffer_contents(dev,subdevice)

    print "front = ", front
    if front > time_limit:
        flag = 0
        t1 = time.time() # reached "secs" seconds
        c.comedi_cancel(device, subdevice)
        c.comedi_poll(device, subdevice)
        c.comedi_close(dev)
        break

    if (front<back):
        t1 = time.time() # reached "secs" seconds
        print "front<back"
        print "ERROR comedi_get_buffer_contents"
        c.comedi_cancel(device, subdevice)
        c.comedi_poll(device, subdevice)
        break
    if (front==back):
        print 'sleep'
        #~ time.sleep(.001)
        time.sleep(pause)
        continue

    if back%size>front%size:
        print '			back%size>front%size:'
        data = map[back%size:size]
        alldata[back/2:back/2+len(data)/2] = numpy.fromstring(data , dtype = 'i2')

        ret = c.comedi_mark_buffer_read(dev, subdevice, size - back%size)
        if ret<0:
            raise "error comedi_mark_buffer_read"
        back += (size - back%size)
	
    data = map[back%size:front%size]
    print 'data', len(data)
    #~ alldata += data
    print back,front
    print numpy.fromstring(data , dtype = 'i2').size
    alldata[back/2:back/2+len(data)/2] = numpy.fromstring(data , dtype = 'i2')
    print 'alldata',len(alldata)

    ret = c.comedi_mark_buffer_read(dev, subdevice, front-back)
    if ret<0:
        raise "error comedi_mark_buffer_read"
    back = front	


c.comedi_close(dev)
	
if ret<0:
    raise "ERROR executing comedi_close"
print "Elapsed time = %d seconds" % (t1-t0)
	
	
# plot
import pylab
buf = alldata
buf = buf.astype('f')
buf = buf.reshape((buf.size/nchans,nchans))
t = numpy.arange((buf.shape[0])).astype('f')/freq
for i in range(nchans):
    pylab.plot(t,buf[:,i]+i*2**12)
pylab.show()




