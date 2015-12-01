#!/usr/bin/env python
import os
import sys
import random
sys.path.append(os.getcwd()+'/lib')
import socket
import pickle
import time
import thread
import json, socket
import sqlite3
import UDPFunc
import databaseFunc as dbFunc


CUR_IP = '127.0.0.1'
CUR_PORT = 6006

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5005

pulseID = 0
respID = 0
accellID = 0



def main():
	initTime = time.time
	#Create the server socket and bind it to the IP and the PORT
	server = UDPFunc.createUDPSocket(CUR_IP,CUR_PORT)
	time.sleep(5)

	sendData = {'id':'wearable','command':'getPatientInfo','data':1}
	server.sendto(json.dumps(sendData),(SERVER_IP,SERVER_PORT))


	data_received, addr = UDPFunc.recvUDP(server)
	data_decodded = json.loads(data_received)

	print(	"Sender: "+ str(data_decodded['id']) +
			"\tName: " + str(data_decodded['data']['name']) +
			'\taverage HeartRate: ' + str(data_decodded['data']['averageHeartRate'])
			)

	data = {'id':'wearable','command':'addSensorData','data':{'bpm':0,'forceMag':0}}

	while True:
		time.sleep(1)
		data['data']['pulse'] = random.randint(50,160)
		data['data']['forceMag'] = random.randint(0,6)
		print ( 'Time: '+ str(time.time()) + '\tBPM: '+ str(data['data']['pulse']) + '   \tforceMag: ' + str(data['data']['forceMag']) )
		server.sendto(json.dumps(data),(SERVER_IP,SERVER_PORT))

		if data['data']['forceMag'] >4 and data['data']['pulse'] >130:
			if random.choice([True, False]):
				server.sendto(json.dumps(
							{'id':'wearable',
							'command':'truePositiveAlarm'}
							),
							(SERVER_IP,SERVER_PORT))
			else:
				server.sendto(json.dumps(
							{'id':'wearable',
							'command':'falsePositiveAlarm'}
							),
							(SERVER_IP,SERVER_PORT))
if __name__ == "__main__":
    main()
