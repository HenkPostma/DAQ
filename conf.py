#!/usr/bin/python

class parameter:
	def __init__(self, value=None, name="", unit="", hint="", min=None, max=None):
		self.hint = hint
		self.name = name
		self.unit = unit
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
    def __init__(self, name=None):
        self.conf = None
        self.pars = []
        self.name = name
    def addpar(self, p):
        self.pars.append(p)
    def display(self):
        print self.name
        for par in self.pars:
            if par.display() != None:
                print "  " + str(par)
    def runfunc(self, func):
        self.run = func
    def get(self, name):
        for par in self.pars:
#            print par.name
            if par.name == name: 
                return par
    def getvalue(self, group, name):
        par = self.get(group)
        return par.get(name).value
        
    def howfast(self):
        return float(self.getvalue("Sweep Parameters", "Increment"))/float(self.getvalue("Sweep Parameters", "Sweep rate"))
                
def saysomething():
    print "sayit"
    
class linearscan(expt):
    def __init__(self):
        x = expt("X axis")
        x.addpar(parameter(name = "Channel", value = "0"))
        x.addpar(parameter(name = "Amplification", value = "1"))
        x.addpar(parameter(name = "Offset", value = "0"))
        x.addpar(parameter(name = "Legend", value = "Analog out"))
        x.addpar(parameter(name = "Unit", value = "V"))

        y = expt("Y axis")
        y.addpar(parameter(name = "Channel", value = "0"))
        y.addpar(parameter(name = "Amplification", value = "1"))
        y.addpar(parameter(name = "Offset", value = "0"))
        y.addpar(parameter(name = "Legend", value = "Analog in"))
        y.addpar(parameter(name = "Unit", value = "V"))

        s = expt("Sweep Parameters")
        s.addpar(parameter(name = "From", value = "-5"))
        s.addpar(parameter(name = "To", value = "5"))
        s.addpar(parameter(name = "Increment", value = "1"))
        s.addpar(parameter(name = "Cycle", value = True))
        s.addpar(parameter(name = "Wait", value = "0"))
        s.addpar(parameter(name = "Sweep rate", value = "10", unit="V/s"))

        self = expt(name="Linear Scan")
        self.addpar(x)
        self.addpar(y)
        self.addpar(s)
        
    def tell(self):
        return float(self.getvalue("Sweep Parameters", "Sweep rate"))/float(self.getvalue("Sweep Parameters", "Increment"))
	
x = expt("X axis")
x.addpar(parameter(name = "Channel", value = "0"))
x.addpar(parameter(name = "Amplification", value = "1"))
x.addpar(parameter(name = "Offset", value = "0"))
x.addpar(parameter(name = "Legend", value = "Analog out"))
x.addpar(parameter(name = "Unit", value = "V"))

y = expt("Y axis")
y.addpar(parameter(name = "Channel", value = "0"))
y.addpar(parameter(name = "Amplification", value = "1"))
y.addpar(parameter(name = "Offset", value = "0"))
y.addpar(parameter(name = "Legend", value = "Analog in"))
y.addpar(parameter(name = "Unit", value = "V"))

s = expt("Sweep Parameters")
s.addpar(parameter(name = "From", value = "-5"))
s.addpar(parameter(name = "To", value = "5"))
s.addpar(parameter(name = "Increment", value = "1"))
s.addpar(parameter(name = "Cycle", value = True))
s.addpar(parameter(name = "Wait", value = "0"))
s.addpar(parameter(name = "Sweep rate", value = "10", unit="V/s"))

f = linearscan()
#f.addpar(x)
#f.addpar(y)
#f.addpar(s)
#f.runfunc(saysomething)
f.display()

#f.run()


#p = f.get("Sweep Parameters").get("Increment").value

#print p
#p.display()


print f.getvalue("Sweep Parameters", "Increment")
print f.getvalue("Sweep Parameters", "Cycle")

print f.howfast()

q = linearscan()
q.tell()

#f.get("Sweep Parameters").get("Increment").display()

