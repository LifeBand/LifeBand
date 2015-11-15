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
CUR_PORT = 9090

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080

pulseID = 0
respID = 0
accellID = 0



def main():
	initTime = time.time
	#Create the server socket and bind it to the IP and the PORT
	server = UDPFunc.createUDPSocket(CUR_IP,CUR_PORT)

	data = {'id':'wearable','command':'addPulseData','data':{'pulse':0}}

	while True:
		randInt = random.randint(50,160)
		data['data']['pulse'] = randInt
		time.sleep(2)
		print 'Sending to server' + str(randInt)
		server.sendto(json.dumps(data),(SERVER_IP,SERVER_PORT))


if __name__ == "__main__":
    main()
