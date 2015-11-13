#!/usr/bin/env python
from __future__ import print_function
import os
import sys

sys.path.append(os.getcwd()+'/lib')

import socket
import pickle
import time
from threading import Thread #import thread
import json, socket
import sqlite3


#Google Email API
import httplib2
import os
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


#Custom files
import UDPFunc
import databaseFunc as dbFunc
import googleEmailApiFunc as emailAPI

DEF_DB_PATH = 'lifeBandDB.db'
DEF_IP = '127.0.0.1'
DEF_PORT = 8080

DEF_DAYS_IN_SECONDS = 7776000

pulseID = 0
respID = 0
accellID = 0



"""Dictionaries for established database structure"""
emergListCols = [ 
					['contactID','TEXT'] , 
					['name', 'TEXT'] , 
					['phone', 'INT'] , 
					['email','TEXT'] , 
					['twitter','TEXT'] 
				]


devListCols = 	[	 
					['DEVID','TEXT'] , 
					['devName', 'TEXT'] , 
					['sampRate', 'INT'] , 
					['unit','TEXT'] 
				]


alarmListCols = [	 
					['timeStamp','TEXT'] , 
					['status', 'TEXT'] 
				]


def serverController(args): 
	"""
	Function:	
	Serve the requests that is received by Phone or wearable

	Input arguments:
	args[0] : data that is contained in UDP packets
	args[1] : Address from the connection
	"""
	data = args[0]
	addr = args[1]
	database = sqlite3.connect(DEF_DB_PATH)
	#print "Transmitted data: "+ data
	dataDecoded = json.loads(data)
	print ("Decoded data: " + str(dataDecoded))

	if dataDecoded['id'] == "phone":
		print ("Phone data Received!")
		if dataDecoded['command'] == 'getLatestData':
			print ("Sending latest Data")

		elif dataDecoded['command'] == 'getPastData':

		elif dataDecoded['command'] == 'addEmergencyContact':
			addEmergContactInfo(conn,'emergList',dataDecoded['data'])
		elif dataDecoded['command'] == 'remEmergencyContact':
			remEmergContactInfo(conn,'emergList',dataDecoded['data'])

	elif dataDecoded['id'] == "wearable":
		print ("Wearable data Received!")
		if dataDecoded['command'] == 'addPulseData':
			print ("Adding pulse data to database")
			dbFunc.addSensorData(database,'pulse',pulseID,dataDecoded['data'])
			dbFunc.printTable(database,'pulseData')

		elif dataDecoded['command'] == 'addRespData':
			print ("Adding respiratory data to database")
			dbFunc.addSensorData(database,'resp',respID,dataDecoded['data'])
			
		elif dataDecoded['command'] == 'addAccelData':
			print (str(time.time()) +"Adding accelerometer data to database")
			dbFunc.addSensorData(database,'accell',accellID,dataDecoded['data'])

		elif dataDecoded['command'] == 'truePositiveAlarm':
			print (str(time.time())+"Adding False Positive Alarm to database")
			dbFunc.addAlarmData(database,'alarmList','TRUE')

		elif dataDecoded['command'] == 'falsePositiveAlarm':
			print (str(time.time())+"Adding True Positive Alarm to database")
			dbFunc.addAlarmData(database,'alarmList','FALSE')

def createSensorDatabase():
	"""
	Function:	
	Create the Database tables for syste

	Input arguments:
	None

	Output variables:
	None
	"""

	global pulseID
	global respID
	global accellID

	conn = sqlite3.connect(DEF_DB_PATH)
	cursor = conn.cursor()

	dbFunc.createTable(conn,'deviceList',devListCols )
	dbFunc.createTable(conn,'emergContactList', emergListCols )
	dbFunc.createTable(conn,'alarmList', emergListCols )

	pulseID = dbFunc.addDevice(conn,'pulse','bpm')
	accellID = dbFunc.addDevice(conn,'accell','N')
	respID = dbFunc.addDevice(conn,'resp','mps')



def maintainDatabaseSize():
	"""
	Function:	
	Maintain the Database of sensor reading to within 90 days

	Input arguments:
	None

	Output variables:
	None
	"""

	conn = sqlite3.connect(DEF_DB_PATH)
	conn.cursor().execute('DELETE FROM deviceList WHERE timeStamp<'+str(time.time()-DEF_DAYS_IN_SECONDS))
	conn.commit()

def emailHandler():
	"""
	Function:	
	Creates a connection with the Google Email API and sends a message
	Upon alert
	
	Input arguments:
	None

	Output variables:
	None
	"""

	print("Email Sender started")
	credentials = emailAPI.get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)

	message = emailAPI.CreateMessage('LifeBandCenter@gmail.com', 'irusha.dilshan@gmail.com', 'Test123', 'Hey! How\'s it hanging?')
	emailAPI.SendMessage(service, 'me', message)



def main():
	#Create the server socket and bind it to the IP and the PORT
	server = UDPFunc.createUDPSocket(DEF_IP,DEF_PORT)

	createSensorDatabase()
	#thread.start_new_thread( maintainDatabaseSize,(None,None)) 
	#thread.start_new_thread( emailHandler,(None,None)) 
	try:
		while True:
			print("Email Thread Creation")
			thread = Thread(target = emailHandler, args = [])
			thread.start()
			print("Email Thread Creation")
			#Accept each communication
			data, addr = UDPFunc.recvUDP(server)
			#Create a new thread for each connection that is made
			thread = Thread(target = serverController, args = (data,addr))
			#thread.start_new_thread( serverController, (data,addr)) 
	except (KeyboardInterrupt, SystemExit):
		closeTCP(conn) 
		server.close()


if __name__ == "__main__":
    main()





