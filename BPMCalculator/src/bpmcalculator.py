from __future__ import division 
import spidev 
import time
import threading 


__author__ = "AmrGawish"
__date__ = "$22-Nov-2015 6:20:56 PM$"

# constants for the sync of the threads
READ_THREAD = 0
SEND_THREAD = 1
# constants for the code
SAMPLE_PERIOD_IN_SEC = 30
SECONDS_PER_SEND = 1
HUMAN_BPM_LIMIT = 150
SECONDS_PER_MIN = 60
THRESHOLD = 0.65
min_seconds_per_beat = SECONDS_PER_MIN/HUMAN_BPM_LIMIT

flag = [False, False]
turn = READ_THREAD

def bit_string(n):
	s=bin(n)[2:]
	return '0'*(8-len(s))+s
#Function to read a value from the pulse sensor attached through the ADC coverter
def read_pulse (adc_channel=0 , spi_channel=0):
	conn = spidev.SpiDev(0,spi_channel)
	conn.max_speed_hz = 1200000
	conn.mode = 0
	cmd =192 
	if adc_channel:
		cmd+=32
	reply_bytes= conn.xfer2([cmd,0])
	reply_bitstring = ''.join(bit_string(n) for n in reply_bytes)
	reply = reply_bitstring[5:15]
	conn.close()
	return int(reply,2)/ 2**10


# sync between the two threads (READ and Send)
def sync_threads (thread1,thread2):
    flag[thread1] = True
    turn = thread2
    while flag[thread2] and turn == thread2:
        pass


# Sender thread that puts the BPM in to its array and print it on the screen
def sender_thread(beat_times):
    BPM_array = []                                  # making new array for the BPM
    count_of_BPM = 0                        
    while True:                                    # go through a loop where it calculates the average
        time.sleep(SECONDS_PER_SEND)                # an inputs the average in to the array
	temp = calculate_average_bpm(beat_times)
        
	BPM_array.append(temp)
        
        print temp
	count_of_BPM = count_of_BPM + 1
  
  
# Reader thread: it reads the beats that is recicved from the sensor 
# and it adds the beat times to the beat_times array
def reader_thread(beat_times):
    while True:
        voltage = read_pulse()
        if voltage > THRESHOLD:                     # if the reading recived from sensor above 0.65 (heart beat)
        
            sync_thread (READ_THREAD,SEND_THREAD)
            
            beat_times.append(time.time())
            
            flag[READ_THREAD] = False
            time.sleep(min_seconds_per_beat)


# this function calculate the average BPM and it calls another function to delete the old value
def calculate_average_bpm(beat_times):
    old_beat_times = []
    ref_time = time.time()
    
    sync_thread (SEND_THREAD,READ_THREAD)
    
    remove_old_values (old_beat_times,beat_times,ref_time)      # remove the values tha is more than 30 seconds away
    
    length = len(beat_times)
    
    flag[SEND_THREAD] = False
    if length <= 1 :
        return 0
    return length*SECONDS_PER_MIN/(beat_times[length - 1] - beat_times[0])


def remove_old_values (old_beat_times,beat_times,ref_time):
    for b_time in beat_times:
        if(abs(ref_time - b_time) > SAMPLE_PERIOD_IN_SEC):
            old_beat_times.append(b_time)
                
    for b_time in old_beat_times:
        beat_times.remove(b_time)


if __name__ == "__main__": 
    
    beat_times = []
    threads = []
    
    reader = threading.Thread(target = reader_thread, args=(beat_times,))
    sender = threading.Thread(target=sender_thread, args=(beat_times,))
    threads.append(reader)
    threads.append(sender)
    reader.start()
    sender.start()
    
            
                        
