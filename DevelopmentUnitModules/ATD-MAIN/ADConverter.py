from __future__ import division
import spidev
import time
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
	return int(reply,2)/ 2**10

if __name__ == '__main__':
	count = 0
#	for x in range (0,100):
#		print read()
#		time.sleep(0.2)
	
	while True:
		time.sleep(0.1)
		if read() > 0.65:
			count = count + 1
			print "     ---"
			print "    ----------------"
			print "      ----------------------"
			print "      ----------------------------- %d" % count
			print "     ----------------------"
			print "    ------------"
			print "     ---"
			print "     --------"
			print "      ---------"
			print "     ------"
			print "     ---"
		elif read() < 0.5:
			print "     ---  %.10f "%read()
                       
