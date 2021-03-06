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


CUR_IP = '0.0.0.0'
CUR_PORT = 6006

SERVER_IP = '192.168.1.102' #27.0.0.1'
SERVER_PORT = 5005

pulseID = 0
respID = 0
accellID = 0



def main(argv):
	initTime = time.time
	#Create the server socket and bind it to the IP and the PORT
	server = UDPFunc.createUDPSocket(CUR_IP,CUR_PORT)

	SERVER_IP = str(argv[1])

	time.sleep(2)

	sendData = {'id':'wearable','command':'getPatientInfo','data':1}
	server.sendto(json.dumps(sendData),(SERVER_IP,SERVER_PORT))


	data_received, addr = UDPFunc.recvUDP(server)
	data_decodded = json.loads(data_received)

	print(	"Sender: "+ str(data_decodded['id']) +
			"\tName: " + str(data_decodded['data']['name']) +
			'\taverage HeartRate: ' + str(data_decodded['data']['min'])
			)

	data = {'id':'wearable','command':'addData','data':{'timeStamp':time.time(),'number':0}}

	while True:
		time.sleep(1)
		data['command'] = 'addBPMData'
		data['data']['timeStamp'] = time.time()
		data['data']['number'] = random.randint(50,160)
		print ( 'Time: '+ str(time.time()) + '\tBPM: '+ str(data['data']['number']))
		server.sendto(json.dumps(data),(SERVER_IP,SERVER_PORT))

		if data['data']['number'] >150:
			if random.choice([True, False]):
				server.sendto(json.dumps(
							{'id':'wearable',
							'command':'truePositiveAlarm',
							'data':{'timeStamp':time.time()}}
							),
							(SERVER_IP,SERVER_PORT))
			else:
				server.sendto(json.dumps(
							{'id':'wearable',
							'command':'falsePositiveAlarm',
							'data':{'timeStamp':time.time()}}
							),
							(SERVER_IP,SERVER_PORT))

		data['command'] = 'addForceMagData'
		data['data']['timeStamp'] = time.time()
		data['data']['number'] = random.randint(0,6)

		print ( 'Time: '+ str(time.time()) + '   \tforceMag: ' + str(data['data']['number']) )

		server.sendto(json.dumps(data),(SERVER_IP,SERVER_PORT))


if __name__ == "__main__":
    main(sys.argv)
