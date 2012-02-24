#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import numpy
import time 
import datetime
from time import localtime, strftime

# Check if we are working in the source tree or from the installed 
# package and mangle the python path accordingly
if os.path.dirname(sys.argv[0]) != ".":
    if sys.argv[0][0] == "/":
        fullPath = os.path.dirname(sys.argv[0])
    else:
        fullPath = os.getcwd() + "/" + os.path.dirname(sys.argv[0])
else:
    fullPath = os.getcwd()

import comedi

def diowrite(subdevice, channel, data):
	dev = comedi.comedi_open("/dev/comedi0")
	ret1 = comedi.comedi_dio_config(dev, subdevice, channel, comedi.COMEDI_OUTPUT)

	if ret1 == 1:
		pass
	else:
		print "initialisation failed"
		
	ret=comedi.comedi_dio_write(dev, subdevice, channel, data)

	if ret == 1:
		pass
	else:
		print "setting failed"
	comedi.comedi_close(dev)
	
def writeline(delayperpoint,vx,vy,dvx,dvy,N):
    beamblank()
    for i in range(0, N+1):
        setx(vx+float(dvx)*(float(i)-float(N)/2)/(float(N)))
        print "x", (vx+float(dvx)*(float(i)-float(N)/2)/(float(N)))
        sety(vy+float(dvy)*(float(i)-float(N)/2)/(float(N)))
        print "y", (vy+float(dvy)*(float(i)-float(N)/2)/(float(N)))
        timedbeamunblank(delayperpoint)
    beamblank()

def timedbeamunblank(delay):
    dev = comedi.comedi_open("/dev/comedi0")

    subdevice = 2
    channel = 0
    data = 0
    ret1 = comedi.comedi_dio_config(dev, subdevice, channel, comedi.COMEDI_OUTPUT)

    if ret1 == 1:
        pass
    else:
        print "initialisation failed"

    start_time = datetime.datetime.now()   
    ret=comedi.comedi_dio_write(dev, subdevice, channel, data)
    blanked_time = datetime.datetime.now()
    
    if ret == 1:
        pass
    else:
        print "setting failed"

    time.sleep(delay)
        
    data = 1
    ret=comedi.comedi_dio_write(dev, subdevice, channel, data)
    end_time = datetime.datetime.now()

    print "blanked_time =", blanked_time  - start_time
    print "end_time =", end_time  - start_time
    
    if ret == 1:
        pass
    else:
        print "setting failed"

    comedi.comedi_close(dev)
    
	
def acquirecontrol():
	diowrite(2, 1, 1)

def releasecontrol():
	diowrite(2, 1, 0)

def beamblank():
	diowrite(2, 0, 1)
	
def beamunblank():
	diowrite(2, 0, 0)
	
def getimage(nx, ny, n):
	dev = comedi.comedi_open("/dev/comedi0")
	outsubdevice = 1
	insubdevice = 0
	xchannel = 0
	ychannel = 1
	inchannel = 0
	analogref = comedi.AREF_GROUND
	arange =  0
	
	image = numpy.zeros((nx,ny), float)
	
	for y in range(0, ny):
		write_data = int(  (float(y)/(ny-1) ) * 65535)	
		msg = comedi.comedi_data_write(dev, outsubdevice, ychannel, arange, analogref, write_data)
		for x in range(0, nx):
			write_data = int(  (float(x)/(nx-1) ) * 65535)
			msg = comedi.comedi_data_write(dev, outsubdevice, xchannel, arange, analogref, write_data)
			pixel = 0.0
			for i in range(0, n):
				result = comedi.comedi_data_read(dev,insubdevice,inchannel,arange,analogref)
				pixel = pixel + float(result[1])
			pixel = pixel/n
#			print pixel,
			msg=result[0]
			image[x][y] = pixel
#		print
		
	comedi.comedi_close(dev)
	return pixel

def sety(voltage):
    dev = comedi.comedi_open("/dev/comedi0")
    outsubdevice = 1
    insubdevice = 0
    xchannel = 0
    ychannel = 1
    inchannel = 0
    analogref = comedi.AREF_GROUND
    arange =  0
    write_data = int(  (float(voltage)+10)/20*65535)
    msg = comedi.comedi_data_write(dev, outsubdevice, ychannel, arange, analogref, write_data)
    comedi.comedi_close(dev)
	
def setx(voltage):
    dev = comedi.comedi_open("/dev/comedi0")
    outsubdevice = 1
    insubdevice = 0
    xchannel = 0
    ychannel = 1
    inchannel = 0
    analogref = comedi.AREF_GROUND
    arange =  0
    write_data = int(  (float(voltage)+10)/20*65535)
    msg = comedi.comedi_data_write(dev, outsubdevice, xchannel, arange, analogref, write_data)
    comedi.comedi_close(dev)
			
def imagecapture_part(xb, yb, xe, ye, nx, ny, n):
    dev = comedi.comedi_open("/dev/comedi0")
    outsubdevice = 1
    insubdevice = 0
    xchannel = 0
    ychannel = 1
    inchannel = 0
    analogref = comedi.AREF_GROUND
    arange =  0

    image = numpy.zeros((nx,ny), float)
	
    for y in range(ny, 0, -1):
        y = y-1
        write_data = int(  (float(y)/(ny-1) *(ye-yb) + yb ) * 65535)
        msg = comedi.comedi_data_write(dev, outsubdevice, ychannel, arange, analogref, write_data)
        for x in range(0, nx):
#            print "( " + str(x) + ", " + str(y) + ")" 
            write_data = int(  (float(x)/(nx-1) * (xe-xb) + xb ) * 65535)
            msg = comedi.comedi_data_write(dev, outsubdevice, xchannel, arange, analogref, write_data)
            pixel = 0.0
            for i in range(0, n):
                result = comedi.comedi_data_read(dev,insubdevice,inchannel,arange,analogref)
                pixel = pixel + float(result[1])
            pixel = pixel/n
#            print pixel,
            msg=result[0]
            image[x][y] = pixel
        print
		
    comedi.comedi_close(dev)
    return image

def writegrid(nx, ny, tmin, tmax):
    deltat = (tmax-tmin)/(float(nx)*ny-1)
    print "nx =", nx, ", ny =", ny
    print "deltat = ", deltat
    t = tmin
    for x in range(0, nx):
        setx(10-(float(x)/(nx-1))*20)
#        print "x: ", 10-(float(x)/(nx-1))*20
#        print "(nx) ", x
        for y in range(0, ny):
            sety((float(y)/(ny-1))*20-10)
            print "t (", 10-(float(x)/(nx-1))*20, ",", (float(y)/(ny-1))*20-10, ") = ", t
#            print " (ny) ", y, 
#            print "  t", t, 
            time.sleep(0.3)
            timedbeamunblank(t)
            t = t+deltat
        print

