from __future__ import division 
import spidev 
import time 
import ctypes as C
import threading 


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
def arraythread ():
    i = 1 
#    global beat_num
 #   global timeStamp
    while True:
       time.sleep (1)
       print ("threadss %d",timeStamp[beat_num%60] )
       BPM = [0]*10
       if (beat_num%60 != 0):
   	   #print "in first"
           diff = timeStamp[i%60] - timeStamp[(i%60)-1]
	   #print ("in for loop %d",diff)
           if diff >= 0.4:
               BPM [i%10] = (1/diff)*60
	       print ("thread %d",BPM[i%10])
	       i = i +1
   
                
# it starts the thread every time needed
def start ():
    
    thread = threading.Thread(target = arraythread )
    threads.append (thread)
    thread.start()

threads = []
beat_num = 0
timeStamp = [0]*60

if __name__ == '__main__':
    global beat_num
    global timeStamp
    start()
    while True:
	time.sleep(0.2)
        beat = read()
        timee = time.time()
        if (beat >= 0.65):
            timeStamp[beat_num%60] = timee                
            print ("main %d",timeStamp[beat_num%60])
	    beat_num = beat_num + 1
	                
                
