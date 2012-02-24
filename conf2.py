#!/usr/bin/python

class parameter:
	def __init__(self, group, name, value=None, unit="", hint="", min=None, max=None):
		self.hint = hint
		self.name = name
		self.unit = unit
		self.group = group
		self.min = min
		self.max = max
		self.value = value
		if value != None:
			self.set(value)
	def __str__(self):
#	    if self.value != None:
  		ret = self.name + " = " + str(self.value)
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
	def display(self):
#	    if self.value != None:
  		ret = self.name + " = " + str(self.value)
		if self.unit != "":
			ret = ret + " " + self.unit
		ret = ret + " (" + self.hint
		if self.min != None:
			ret = ret + ", min = " + str(self.min)
		if self.max != None:
			ret = ret + ", max = " + str(self.max)
		ret = ret + ")"
		return ret

class expt:
    def __init__(self, name):
        self.name = name
        self.conf = []
        pass
    def __str__(self):
        ret = self.name + "\n"
        for p in self.conf:
            ret = ret + "  " + str(p) + "\n"
        return ret
    def run(self):
        pass
    def addpar(self, new):
        self.conf.append(new)
    def get(self, group, name):
        for par in self.conf:
#            print par.name
            if par.name == name and par.group == group: 
                return par.value

print "hi there"

e = expt("expt 1")
p = parameter(group = "Some", name = "Mag", value = 10)
print e
e.addpar(parameter(group = "X channel", name = "Mag", value = 10))
e.addpar(parameter(group = "General", name = "Mag2", value = 100))



print "experiment"
print e

print "parameter"

print e.get(None, "Mag2")
print e.get("X channel", "Mag")



