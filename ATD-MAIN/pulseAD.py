from __future__ import division 
import spidev 
import time 
import ctypes as C
import threading 
import socket
import json

#the function bitstring and read gets the pulse from the pulse sensor through the analog to digital converter
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

#gets a ratio of the pulse per min (freq) and it saves in an array and sends the average ever new data entered
# if there was no pulse it sends the signals envoking the allarm to start 
def arraythread (x,num,val):
	data = {}
	data ['id'] ='wearable'	
	if val == 0 :
		data ['command']= 'possibleAlarm'
		data ['data']={'pulse':'val'}
		ave = 0
		#json_data = json.dumps(data)
		#sock.sentto(json_data.encode('utf-8'),(SERVER_IP,UDP_PORT))
		print "ALAAAAAAAAAAAAARM"
	else:	
		data ['command']= 'addPulseData'
		z = num%10
		x[z]= val
		total=0
		if (z == 0):
			total = val
			ave = total
		else:

			for i in range (0,z):
				total = total + x[i]

			ave = total / z
			data['data']= {'pulse':'ave'}
			#json_data = json.dumps(data)
			#sock.sentto(json_data.encode('utf-8'),(SERVER_IP,UDP_PORT))
		print ("the average number of beats is %d", ave)
	
# the class pulse is the struction where the time stamp of each pulse is saved 
# it has methods to set and change its pointers and values
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

# it starts the thread every time needed
def start (x,num,freq):
	thread = threading.Thread(target = arraythread , args = (x,num,freq) )
	threads.append (thread)
	thread.start()

threads = []		
if __name__ == '__main__':
	x = [0]*10
	count = 0
	num = 0
	# setting the ips and ports for connection between the server 
	MY_IP = "10.0.0.23"
	SERVER_IP= ""
	UDP_PORT = 5005


	#sock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	#sock.bind((MY_IP,UDP_PORT))
		
	while True:
		
		time.sleep(0.1)
		# getting the reading and there time stamp
		p = read()
		timee = time.time()
		#if the voltage recived by read is more than 0.65 that means that there is beat
		# if there is a beat it inputs it in the queue making a new node in the queue
		if (p > 0.65):		
			if (count == 0):
				node = pulse(timee)
				headnode = node
			else:
				node = pulse(timee)

			count = count + 1	
			
			# sending data to the thread every second
			if ((node.getTime() - headnode.getTime() ) >= 1):	
				freq=( 1 / (node.getTime() - headnode.getTime() ))* 60
			
				start (x,num,freq)
			
				num = num + 1
				buf = headnode
				headnode = node
				buf.delet()
				count = 0
            
			node.nodeinc()

		# if there is no pulse for more than 3 seconds that means there might be a danger which sends to the thread a signal of danger 
		elif num != 0 :
			if ((time.time()-node.getTime()) >= 3):
				freq = 0
			
				start(x,num,freq)

				time.sleep(1)
