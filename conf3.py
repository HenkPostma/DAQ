#!/usr/bin/python

class parameter:
	def __init__(self, value=None, unit="", hint="", min=None, max=None):
		self.hint = hint
		self.unit = unit
		self.min = min
		self.max = max
		self.value = value
		if value != None:
			self.set(value)
	def __str__(self):
#	    if self.value != None:
  		ret = str(self.value)
		if self.unit != "":
			ret = ret + " " + self.unit
		ret = ret + " (" + self.hint
		if self.min != None:
			ret = ret + ", min = " + str(self.min)
		if self.max != None:
			ret = ret + ", max = " + str(self.max)
		ret = ret + ")"
		return ret
	def set(self, value):
		tempvalue = value
		if self.min != None:
			if tempvalue < self.min:
				tempvalue = self.min
		if self.max != None:
			if tempvalue > self.max:
				tempvalue = self.max	
		self.value = tempvalue
	def setmin(self, value):
		self.min  = value
		if self.max != None and self.min != None:
			if self.min > self.max:
				self.min = self.max
		if self.max != None and self.min != None:
			if self.value < self.min:
				self.value = self.min
	def setmax(self, value):
		self.max  = value
		if self.max != None and self.min != None:	
			if self.max < self.min:
				self.max = self.min
		if self.max != None and self.min != None:
			if self.value > self.max:
				self.value = self.max	
	def get(self):
		return self.value


class expt:
    def __init__(self, name):
        self.name = name
        self.conf = dict()
        pass
    def __str__(self):
        ret = self.name + "\n"
        for group in sorted(self.conf.keys()):
            ret = ret + "  " + group + "\n"
            gr = self.conf[group]
            for p in sorted(gr.keys()):
                ret = ret + "    " + p + " = " + str(gr[p]) + "\n"
        return ret
    def run(self):
        pass
    def addpar(self, group, name, new):
        if group in self.conf.keys():
            gr = self.conf[group]
            gr[name] = new
            print name + " added to " + group
        else:
            print name + " is new"
            self.conf[group] = dict()
            gr = self.conf[group]
            gr[name] = new
    def get(self, group, name):
        if group in self.conf.keys():
            gr = self.conf[group]
            if name in gr.keys():
                return gr[name]
            else:
                return None
        else:
            return None


print "hi there"

e = expt("Linear Scan")

e.addpar("X axis", "Channel", parameter(value = 0))
e.addpar("X axis", "Amplification", parameter(value = 1))
e.addpar("X axis", "Offset", parameter(value = 0))
e.addpar("X axis", "Legend", parameter(value = "Analog out"))
e.addpar("X axis", "Unit", parameter(value = "V"))

print "experiment"
print e

e.addpar("Y axis", "Channel", parameter(value = 0))
e.addpar("Y axis", "Amplification", parameter(value = 1))
e.addpar("Y axis", "Offset", parameter(value = 0))
e.addpar("Y axis", "Legend", parameter(value = "Analog out"))
e.addpar("Y axis", "Unit", parameter(value = "V"))

print "experiment"
print e

e.addpar("Sweep Parameters", "From", parameter(-5, max=10, min=-10))
e.addpar("Sweep Parameters", "To", parameter(5))
e.addpar("Sweep Parameters", "Increment", parameter(0.1))
e.addpar("Sweep Parameters", "Cycle", parameter(True))
e.addpar("Sweep Parameters", "Wait", parameter(0))
e.addpar("Sweep Parameters", "Sweep rate", parameter(value = 10, unit="V/s"))

print "experiment"
print e



