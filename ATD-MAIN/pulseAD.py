from __future__ import division 
import spidev 
import time 
import ctypes as C
import threading 

def bitstring(n):
	s=bin(n)[2:]
	return '0'*(8-len(s))+s

def read (adc_channel=0 , spi_channel=0):
	conn = spidev.SpiDev(0,spi_channel)
	conn.max_speed_hz = 1200000
	conn.mode = 0
	cmd =192 
	if adc_channel:
		cmd+=32
	reply_bytes= conn.xfer2([cmd,0])
	reply_bitstring = ''.join(bitstring(n) for n in reply_bytes)
	reply = reply_bitstring[5:15]
	conn.close()
	return int(reply,2)/ 2**10

def inarray (x,num,val):
	x[num] = value
	total = 0

	for i in range (0,num):
		total = total + x[num]

	print ("the average number of beats is %d", total)
	
class pulse:
	def __init__ (self,time):
		self.time = time
		self.next = None

	def getTime(self):
		return self.time

	def getNext(self):
		return self.next

	def settime(self,newtime):
		self.time = newtime

	def setnext(self,next):
		self.next = next

	def nodeinc(self):
		self = self.next

	def size(self):
		current = self
		count = 0
		while current != None:
			count = count + 1
			current = current.next

		return count

	def delet(self):
		del self

		
if __name__ == '__main__':
	x = [0]*10
	count = 0
	num = 0
	
	while True:
		time.sleep(0.1)
		p = read()
		
		timee = time.time()
		if (p > 0.65):		
			if (count == 0):
				node = pulse(timee)
				headnode = node
			else:
				print ("node added")
				node = pulse(timee)

			count = count + 1

			#print ("head time %d",headnode.getTime())
			#print ("node time %d",node.getTime())
			#print count	

			if ((node.getTime() - headnode.getTime() ) >= 1):
				val =( count / (node.getTime() - headnode.getTime() ))* 60
				thread = thread (target = inarray, args = (x,num,val)			
				num = num + 1
				buf = headnode
				headnode = node
				buf.delet()
				count = 0
            
			node.nodeinc()
