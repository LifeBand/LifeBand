#-------------------------------------------------------------------------------
# Name:        LifeBand/alarm_handler
# Purpose:
#
# Author:      Derek White
#
# Created:     20/11/2015
# Copyright:   (c) Asus 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import RPi.GPIO as GPIO
import json, socket, time



GPIO.setmode (GPIO.BCM)
GPIO.setup (17, GPIO.IN)

class alarm_handler:

    def __init__(self, buffer, bufsize, server_IP, server_PORT):
        self.alarming = 10
        self.alarm = False
        self.buffer = buffer
        self.bufsize = bufsize
        self.lastTime = 0
        self.minThreshold = 60
        self.maxThreshold = 100
        self.maxChange = 15
        self.message = {'id':'wearable'}
        self.MY_PORT = '6006'
        self.MY_IP = '0.0.0.0'
        self.SERVER_PORT = server_PORT
        self.SERVER_IP = server_IP
        self.rcvSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rcvSock.bind((MY_IP,MY_PORT))
        self.sendingSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.heartbeats = []
        self.currentIndex = 0
        send_message('getPatientInfo', '')

    """
    Simple method to send a message to the server with the command and data given
    """
    def send_message(command, data):
        message['command'] = command
        message['data'] = data
        sendingSock.sendto(json.dumps(self.message), (self.SERVER_IP, self.SERVER_PORT))
        
    """
    checks the button to see if it is pressed.
    if the button has been pressed and alarming data was found, it will reset the countdown
    """
    def check_button():
        if(GPIO.input(17) and alarming < 10):
            send_message('falsePositiveAlarm','')
            alarm = False
            
    """
    does the countdown for the alarm and sending the message to the server once it has been reached
    """
    def heartbeat_alarm_signal():
        if alarming > 1:
            alarming -= 1
            if alarming == 0:
                alarm = True
        elif not alarm:
            send_message('truePositiveAlarm','')
    
    """
    Puts the given heartbeat into the heartbeats array and checks it for safe values
    """
    def put_into_array(heartbeat):
        heartbeats[currentIndex] = [heartbeat, time.mktime(time.localtime())]
        currentIndex = (currentIndex + 1)%bufsize
        if heartbeat > maxThreshold or heartbeat < minThreshold or abs(heartbeat - heartbeats[currentIndex - 1]) > maxChange:
            heartbeat_alarm_signal()
        else:
            alarming = 10

    """
    Calculates the average bpm from the last time this function was called
    and sends the data to the server. The time sent is from the middle of the time period
    """
    def calc_average():
        currentTime = time.mktime(time.localtime())
        i = 0
        while i < currentIndex:
            if heartbeats[currentIndex - i]['time'] > lastTime:
                message = {'bpm':runningTotal/i, 'time':(lastTime + currentTime)/2}
                send_message('addSensorData',message)
                lastTime = currentTime
                return
            runningTotal += heartbeats[currentIndex - i]['bpm']
            i+=1
            
  """
  checks for a response from the server for its getPatientInfo request
  """
    def get_new_thresholds():
        data, addr = rcvSock.recvfrom(MY_PORT)
        stuff = json.loads(data)
        if stuff['id'] == 'server' and stuff['command'] == 'putPatientInfo':
            if type(stuff['data']['max']) == type(1) and type(stuff['data']['min']) == type(1) and type(stuff['data']['change']) == type(1):
                maxThreshold = stuff['data']['max']
                minThreshold = stuff['data']['min']
                maxChange = stuff['data']['change']










