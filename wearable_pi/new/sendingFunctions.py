#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     
#
# Author:      Asus
#
# Created:     03/12/2015
# Copyright:   (c) Asus 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import spidev, time, threading, json, socket
import RPi.GPIO as GPIO
MY_PORT = '6006'
MY_IP = '0.0.0.0'
SERVER_PORT = '5005'
SERVER_IP = '108.192.168.0.108'

sendingSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
def send_BPM_data(BPM):
    time = time.time()
    message['id'] = 'wearable'
    message['command'] = 'addSensorData'
    message['data'] = {'bpm': BPM, 'time': time}
    sendingSock.sendto(json.dumps(message), (SERVER_IP, SERVER_PORT))
    if BPM > HUMAN_BPM_LIMIT or BPM < 1.0/min_seconds_per_beat:
        send_alarm()
        
def send_alarm ():
    message['command'] = 'truePositiveAlarm'
    message['data'] = time.time()
    sendingSock.sendto(json.dumps(message), (SERVER_IP, SERVER_PORT))
    
def send_mag_data(magnitude):
    message['id'] = 'wearable'
    message['command'] = 'addSensorData'
    message['data'] = {'forceMag': magnitude, 'time': time()}
    sendingSock.sendto(json.dumps(message), (SERVER_IP, SERVER_PORT))