from __future__ import division
import xlwt 
import spidev 
import time

__author__ = "dominikschmidtlein"
__date__ = "$Nov 22, 2015 7:35:40 PM$"

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

if __name__ == "__main__":    
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('voltages vs time')
    
    row = 1
    t1 = time.time()
    while abs(time.time() - t1)  < 10:
        t2 = time.time()
        delta_t = t2 - t1
        voltage = read()
	print voltage
        ws.write(row, 0,delta_t)
        ws.write(row, 1, voltage)
        row += 1
	time.sleep(0.05)
    wb.save('voltages.xls')
        
        
