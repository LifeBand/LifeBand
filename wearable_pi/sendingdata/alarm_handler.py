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

    def __init__(self, server_IP, server_PORT):
        self.alarming = 10
        self.alarm = False
        self.lastTime = time.mktime(time.localtime())
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
        self.lastBPM = {}
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
    def check_button(health):
        if((GPIO.input(17) or health) and alarming < 10):
            alarm = False

    """
    does the countdown for the alarm and sending the message to the server once it has been reached
    """
    def heartbeat_alarm_signal(time):
        if alarming > 1:
            alarming -= 1
        elif not alarm:
            alarm = True
            send_message('truePositiveAlarm',{'time':time})

    def send(acc, bpm):
        send_message('addSensorData', {'accel': acc, 'time': time.time(), 'bpm': bpm})


    """
    Puts the given heartbeat into the heartbeats array and checks it for safe values
    """
    def put_into_array(heartbeat):
        time = time.mktime(time.localtime())
        lastBPM = {'data':heartbeat, 'time':time}
        if heartbeat > maxThreshold or heartbeat < minThreshold or abs(heartbeat - lastBPM) > maxChange:
            heartbeat_alarm_signal(time)
        elif alarming < 10:
            alarming = 10
            send_message('falsePositiveAlarm',{'time':time})
        lastBPM = heartbeat


    """
    Calculates the average bpm from the last time this function was called
    and sends the data to the server. The time sent is from the middle of the time period
    """
    def calc_average():
        i = 0
        while i < 5 and i < currentIndex:
            runningTotal += lastBPM['bpm']
            i+=1
        message = {'bpm':runningTotal/i, 'time':time.mktime(time.localtime())}
        send_message('addSensorData',message)

    def accelerometer_thread():
        ref_time = time.time()
        counter = 0
        while True:
            curr_mag = get_axes()
            if time.time() > ref_time + 1:



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

if __name__ == "__main__":
    module = alarm_handler()
    time.sleep(3)
    module.get_new_thresholds()









