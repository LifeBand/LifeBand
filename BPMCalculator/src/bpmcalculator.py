from __future__ import division 
import spidev 
import time
import threading 


__author__ = "dominikschmidtlein"
__date__ = "$Nov 20, 2015 3:43:40 PM$"

READ_THREAD = 0
SEND_THREAD = 1

SAMPLE_PERIOD_IN_SEC = 30
SECONDS_PER_SEND = 1
HUMAN_BPM_LIMIT = 150
SECONDS_PER_MIN = 60
THRESHOLD = 0.65

bt_index = 0
min_seconds_per_beat = SECONDS_PER_MIN/HUMAN_BPM_LIMIT
send = None

flag = [False, False]
turn = READ_THREAD

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

def send(BPM):
    print BPM

def sender_thread(beat_times, n):
    while(True):
        time.sleep(SECONDS_PER_SEND)
        send(calculate_average_bpm(beat_times))
        
def reader_thread(beat_times, n):
    while True:
        voltage = read()
        if voltage > THRESHOLD:
            print voltage
            flag[READ_THREAD] = True
            turn = SEND_THREAD
            while flag[SEND_THREAD] and turn == SEND_THREAD:
                pass
            #CS start
            beat_times.append(time.time())
            #CS end
            flag[READ_THREAD] = False
            time.sleep(min_seconds_per_beat)

def calculate_average_bpm(beat_times):
    old_beat_times = []
    ref_time = time.time()
    
    flag[SEND_THREAD] = True
    turn = READ_THREAD
    while flag[READ_THREAD] and turn == READ_THREAD:
        pass
    #CS start
    for b_time in beat_times:
        if(abs(ref_time - b_time) > SAMPLE_PERIOD_IN_SEC):
            old_beat_times.append(b_time)
                
    for b_time in old_beat_times:
        beat_times.remove(b_time)
    length = len(beat_times)
    #CS end
    flag[SEND_THREAD] = False
    
    return length*SECONDS_PER_MIN/(beat_times[length - 1] - beat_times[0])

def test_thread(b, n):
    return -1

threads = []
if __name__ == "__main__": 
    
    beat_times = []
    num = 0
    
    reader = threading.Thread(target = reader_thread, args=(beat_times, num))
    sender = threading.Thread(target=sender_thread, args=(beat_times, num))
    threads.append(reader)
    threads.append(sender)
    reader.start()
    sender.start()
    
            
                        