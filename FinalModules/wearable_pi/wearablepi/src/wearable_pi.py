from __future__ import division 
from adxl345 import ADXL345
import spidev 
import time
import threading
import json
import socket
import RPi.GPIO as GPIO
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

SERVER_IP = '192.168.0.104'
MY_IP = "0.0.0.0"
SERVER_PORT = 5005
MY_PORT = 6006

CONN_MAX_SPEED_HZ = 1200000
CONN_MODE = 0
bt_index = 0
min_seconds_per_beat = SECONDS_PER_MIN/HUMAN_BPM_LIMIT
send = None

flag = [False, False]
turn = READ_THREAD

MAGNITUDE_THRESHOLD = 2.5
PERIOD_BETWEEN_SAMPLES = 0.01
beat_times_length = 0

#global variables to access the pulse and the max magnitude together 
GBPM = int()
# these two functions read from the pulse from the sensor and it has been called from 
# the other function in order to read
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

# sending the Beat Per second to server
def save(BPM):
    global GBPM
    GBPM = BPM
    print "BPM"
    print BPM

# sends the pulse to the server by geting the calculate average and sending the average
def BPM_sender_thread(beat_times):
    while(True):
        time.sleep(SECONDS_PER_SEND)
        save(calculate_average_bpm(beat_times))

# calls the read function and append the time stamp of that beat to beat times
def BPM_reader_thread(beat_times):
    while True:
        check_for_time(beat_times)
        voltage = read_pulse()
        if voltage > THRESHOLD:
	    thread_sync (READ_THREAD,SEND_THREAD)
            beat_times.append(time.time())
            beat_times_length+=1;
            if(beat_times_length>SAMPLE_PERIOD_IN_SEC):
                beat_times_length = SAMPLE_PERIOD_IN_SEC
            flag[READ_THREAD] = False
            time.sleep(min_seconds_per_beat)

# a semaphore for the threads so that they do not be change the beat per second at the time 
def thread_sync (thread1,thread2):
    flag[thread1] = True
    turn = thread2
    while flag[thread2] and turn == thread2:
        pass

# it calculates the BPM by comparing the times of the beats coming and getting the frequency 
def calculate_average_bpm(beat_times):
    old_beat_times = []
    ref_time = time.time()
    thread_sync (SEND_THREAD,READ_THREAD)
    remove_from_pulse (beat_times,ref_time,old_beat_times)
    length = beat_times_length
    flag[SEND_THREAD] = False
    if length == 0:
        return 0
    if length == 1:
        return length*SECONDS_PER_MIN/(beat_times[length] - beat_times[0])
    else:
        return length*SECONDS_PER_MIN/(beat_times[length - 1] - beat_times[0])

def check_for_time(beat_times):
    length = beat_times_length #len (beat_times)
    if len(beat_times)==0:
        return
    if (time.time()- beat_times[length-1]) > 3:
        send_message('truePositiveAlarm', {'time':time.time()})
        alarm = True
        
# it removes the Old beats which has a time stamp more than the sample period chosen from the list 
def remove_from_pulse (beat_times,ref_time,old_beat_times):
    for b_time in beat_times:
        if(abs(ref_time - b_time) > SAMPLE_PERIOD_IN_SEC):
            old_beat_times.append(b_time)
                
    for b_time in old_beat_times:
        beat_times.remove(b_time)

#gets the magnitude of the axcels from the axceletometer 
def get_magnitude(x, y, z):
    return sqrt(x**2 + y**2 + z**2)

# get the magnitude in dictinary
def get_magnitude_dict(axes):
    return get_magnitude(axes['x'], axes['y'], axes['z'])
    
# reads data from the accelerometer by checking the forces on each axes
def read_acceleration_to_dict(adxl345):
    return adxl345.getAxes(True)

#makes sure that the magnitude calculates is above threshold
def check_magnitude(magnitude):
    return magnitude > MAGNITUDE_THRESHOLD

# end an alarm in case of emergency
def send_alarm():
    print "                                 ALARM"
    
def get_axes():  
        adxl345 = ADXL345()
        magnitude = get_magnitude_dict(read_acceleration_to_dict(adxl345))
        if check_magnitude(magnitude):
            send_message('truePositiveAlarm', {'timeStamp':time.time()})
            alarm = True
            
#starts the accelerometer thread
def acceloremetor_thread():
    ref_time = time.time()
    counter = 0
    while True:
        curr_mag = get_axes()
        if (time.time() - ref_time )< 1:
            if counter == 0 :
                max_magnitude = curr_mag
                counter = counter+1
            else:
                if curr_mag > max_magnitude:
                    max_magnitude = curr_mag
        else:
            check_GBPM(max_magnitude)
            ref_time = time.time
            counter = 0
            check_button()
 
def check_GBPM (max_magnitude):
    if (GBPM is not None):
        send_message('addSensorData',{'forceMag':max_magnitude,'bpm':GBPM, 'timeStamp':time.time()})
        

            
# starts all the threads which is all  the program			
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
	
def send(acc, bpm):
    message['command'] = 'addSensorData'
    message['data'] = {'bpm': bpm, 'forceMag':acc,'time':time.time()}
    sendingSock.sendto(json.dumps(message), (SERVER_IP, SERVER_PORT))

def check_button():
    if GPIO.input(17) and alarm:
        alarm = False
        send_message('falsePositiveAlarm', {'time': time.time()})
        
def send_message(command, data):
    message['command'] = command
    message['data'] = data
    sendingSock.sendto(json.dumps(message), (SERVER_IP, SERVER_PORT))
        
def heartbeat_alarm_signal(time):
    if alarming > 1:
        alarming -=1
    elif not alarm:
        alarm = True
        send_message('truePositiveAlarm', {'time': time})
    
        
threads = []
if __name__ == "__main__": 
    beat_times = []
    alarm = False
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN)
    rcvSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rcvSock.bind((MY_IP,MY_PORT))
    sendingSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = {'id':'wearable'}
    start_threads()
	

