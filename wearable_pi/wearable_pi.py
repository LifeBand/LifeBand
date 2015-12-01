from __future__ import division 
from adxl345 import ADXL345
import spidev 
from time import sleep
import threading 
from math import sqrt

__author__ = "Amr Gawish"
__date__ = "$Nov 20, 2015 3:43:40 PM$"

READ_THREAD = 0
SEND_THREAD = 1

SAMPLE_PERIOD_IN_SEC = 30
SECONDS_PER_SEND = 1
HUMAN_BPM_LIMIT = 150
SECONDS_PER_MIN = 60
THRESHOLD = 0.65

CONN_MAX_SPEED_HZ = 1200000
CONN_MODE = 0
bt_index = 0
min_seconds_per_beat = SECONDS_PER_MIN/HUMAN_BPM_LIMIT
send = None

flag = [False, False]
turn = READ_THREAD

MAGNITUDE_THRESHOLD = 2.5
PERIOD_BETWEEN_SAMPLES = 0.01

def bitstring(num):
	s=bin(num)[2:]
	return '0'*(8-len(s))+s

def read_pulse (adc_channel=0 , spi_channel=0):
	conn = spidev.SpiDev(0,spi_channel)
	conn.max_speed_hz = CONN_MAX_SPEED_HZ
	conn.mode = CONN_MODE
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

def BPM_sender_thread(beat_times, n):
    while(True):
        time.sleep(SECONDS_PER_SEND)
        send(calculate_average_bpm(beat_times))
        
def BPM_reader_thread(beat_times, n):
    while True:
        voltage = read_pulse()
        if voltage > THRESHOLD:
            print "pulse"
	    print  voltage
	    thread_sync (READ_THREAD,SEND_THREAD)
            beat_times.append(time.time())
            flag[READ_THREAD] = False
            time.sleep(min_seconds_per_beat)

def thread_sync (thread1,thread2):
    flag[thread1] = True
    turn = thread2
    while flag[thread2] and turn == thread2:
        pass
		
def calculate_average_bpm(beat_times):
    old_beat_times = []
    ref_time = time.time()
    thread_sync (SEND_THREAD,READ_THREAD)
    remove_from_pulse (beat_times,ref_time,old_beat_times)
    length = len(beat_times)
    flag[SEND_THREAD] = False
    if length == 0:
        return 0
    return length*SECONDS_PER_MIN/(beat_times[length - 1] - beat_times[0])

def remove_from_pulse (beat_times,ref_time,old_beat_times):
    for b_time in beat_times:
        if(abs(ref_time - b_time) > SAMPLE_PERIOD_IN_SEC):
            old_beat_times.append(b_time)
                
    for b_time in old_beat_times:
        beat_times.remove(b_time)
		
		
def test_thread(b, n):
    return -1

def get_magnitude(x, y, z):
    return sqrt(x**2 + y**2 + z**2)

def get_magnitude_dict(axes):
    return get_magnitude(axes['x'], axes['y'], axes['z'])
    
def read_acceleration_to_dict(adxl345):
    return adxl345.getAxes(True)

def send_magnitude(magnitude):
    print "accel"
    print magnitude
    
def check_magnitude(magnitude):
    return magnitude > MAGNITUDE_THRESHOLD

def send_alarm():
    print "                                 ALARM"
	
def acceloremetor_thread():
    adxl345 = ADXL345()
    while True:
       sleep(PERIOD_BETWEEN_SAMPLES)
       magnitude = get_magnitude_dict(read_acceleration_to_dict(adxl345))
       send_magnitude(magnitude)
       if check_magnitude(magnitude):
           send_alarm()
			
def start_threads():
    BPM_reader = threading.Thread(target = BPM_reader_thread, args=(beat_times,))
    BPM_sender = threading.Thread(target=BPM_sender_thread, args=(beat_times,))
    accelerometer = threading.Thread(target= acceloremetor_thread)
    threads.append(BPM_reader)
    threads.append(BPM_sender)
    threads.append(accelerometer)
    BPM_reader.start()
    BPM_sender.start()
    accelerometer.start()
	
	
threads = []
if __name__ == "__main__": 
    beat_times = []
    start_threads()
	

