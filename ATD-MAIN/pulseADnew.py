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
def arraythread (num):



# it starts the thread every time needed
def start (x,num):
	thread = threading.Thread(target = arraythread , args = (x,num) )
	threads.append (thread)
	thread.start()

threads = []
timeStamp = [0]*60	
	
if __name__ == '__main__':
beat_num = 0

while True:
	beat = read()
	time = time.time()
	if (beat >= 0.65):
		timeStamp[beat_num] = time
		beat_num = beat_num + 1
		 	
