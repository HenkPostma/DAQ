#!/usr/bin/python


import sys
import os
import gtk
import time 
import commands
import glob
from PythonMagick import Image
from numpy import *
from numpy import histogram
from numpy.fft import * 
from pylab import * 

def filter(x, window, lpf, hpf):
    newx = x
    n = int(floor(len(x)/window))
#    print lpf
#    print hpf
#    print window
    for windowcount in range(0, n):
        
        fx = fft(x[windowcount*window:(windowcount+1)*window-1])
        
        for i in range(len(fx)):
            if i > lpf:
                fx[i] = 0
            if i < hpf:
                fx[i] = 0
        
        filtereddata = ifft(fx)
#        print size(filtereddata)
#        newx[i*window:(i+1)*window-1] = filtereddata
#        print "i=", i
        for count in range(len(filtereddata)):
            newx[count+window*windowcount] = filtereddata[count]
    return newx
    
data=loadtxt('/home/www/hiral-20110318-124051-0.dat')
print size(data)
newdata=filter(data[:,1], 1000, 100, 10)

import matplotlib.pyplot as pltfx

plt.figure(1)
plt.subplot(211)
plt.plot(data[1:100,0], data[1:100,1])
#plt.ylabel('some numbers')
plt.subplot(212)
plt.plot(newdata)
plt.show()

