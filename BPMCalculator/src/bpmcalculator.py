import time
import threading
import random

__author__ = "dominikschmidtlein"
__date__ = "$Nov 20, 2015 3:43:40 PM$"

READ_THREAD = 0
SEND_THREAD = 1

SAMPLE_PERIOD_IN_SEC = 10
SECONDS_PER_SEND = 1
HUMAN_BPM_LIMIT = 240
SECONDS_PER_MIN = 60
THRESHOLD = 0.9


#= []*(int((SAMPLE_PERIOD_IN_SEC * HUMAN_BPM_LIMIT) / SECONDS_PER_MIN))
bt_index = 0
min_seconds_per_beat = SECONDS_PER_MIN/HUMAN_BPM_LIMIT
send = None

flag = [False, False]
turn = READ_THREAD

def send(BPM):
    print("", BPM)
    
def read():
    return random.random();

def sender_thread(beat_times):
    while(True):
        time.sleep(SECONDS_PER_SEND)
        send(calculate_average_BPM(beat_times))
        
def reader_thread(beat_times):
    while True:
        voltage = read()
        if voltage > THRESHOLD:
            flag[READ_THREAD] = True
            turn = SEND_THREAD
            while flag[SEND_THREAD] and turn == SEND_THREAD:
                pass
            #CS start
            beat_times.append(voltage)
            #CS end
            flag[READ_THREAD] = False
            time.sleep(min_seconds_per_beat)

def calculate_average_bpm(beat_times):
    new_beat_times = []
    ref_time = time.time()
    
    flag[SEND_THREAD] = True
    turn = READ_THREAD
    while flag[READ_THREAD] and turn == READ_THREAD:
        pass
    #CS start
    for b_time in beat_times:
        if(ref_time - b_time < SAMPLE_PERIOD_IN_SEC):
            new_beat_times.append(b_time)
    beat_times = new_beat_times
    #CS end
    flag[SEND_THREAD] = False
    
    return len(new_beat_times)*SECONDS_PER_MIN/SAMPLE_PERIOD_IN_SEC

if __name__ == "__main__": 
    beat_times = []
    reader = threading.Thread(target=reader_thread, args=(beat_times))
    sender = threading.Thread(target=sender_thread, args=(beat_times))
    reader.start()
    sender.start()
    
            
                        