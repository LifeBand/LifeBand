#!/usr/bin/env python
import os
import sys

sys.path.append(os.getcwd()+'/lib')

import socket
import pickle
import time
import thread
import json, socket
import sqlite3
import UDPFunc
import databaseFunc as dbFunc

DEF_IP = '127.0.0.1'
DEF_PORT = 8080

pulseID = 0
respID = 0
accellID = 0

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


alarmListCols = 	[	 
					['timeStamp','TEXT'] , 
					['Status', 'TEXT'] 
				]


def serverController(data, addr):
	database = sqlite3.connect('lifeBandDB.db')
	#print "Transmitted data: "+ data
	dataDecoded = json.loads(data)
	print "Decoded data: " + str(dataDecoded)

	if dataDecoded['id'] == "phone":
		print "Phone data Received!"
		if dataDecoded['command'] == 'getLatestData':
			print "Sending latest Data"


	elif dataDecoded['id'] == "wearable":
		if dataDecoded['command'] == 'addPulseData':
			print "Adding pulse data to database"
			dbFunc.addSensorData(database,'pulse',pulseID,dataDecoded['data'])
			dbFunc.printTable(database,'pulseData')
		elif dataDecoded['command'] == 'addRespData':
			print "Adding respiratory data to database"
			dbFunc.addSensorData(database,'resp',respID,dataDecoded['data'])
		elif dataDecoded['command'] == 'addAccelData':
			print "Adding accelerometer data to database"
			dbFunc.addSensorData(database,'accell',accellID,dataDecoded['data'])

		elif dataDecoded['command'] == 'truePositiveAlarm':
			#dbFunc.addSensorData(database,'accell',accellID,dataDecoded['data'])

			print "Adding new sensor data to database"
		elif dataDecoded['command'] == 'falsePositiveAlarm':
			print "Adding new sensor data to database"

def createSensorDatabase():
	global pulseID
	global respID
	global accellID

	conn = sqlite3.connect('lifeBandDB.db')
	cursor = conn.cursor()
	dbFunc.createTable(conn,'deviceList',devListCols )
	dbFunc.createTable(conn,'emergContactList', emergListCols )
	dbFunc.createTable(conn,'alarmList', emergListCols )

	pulseID = dbFunc.addDevice(conn,'pulse','bpm')
	accellID = dbFunc.addDevice(conn,'accell','N')
	respID = dbFunc.addDevice(conn,'resp','mps')



def main():
	#Create the server socket and bind it to the IP and the PORT
	server = UDPFunc.createUDPSocket(DEF_IP,DEF_PORT)

	createSensorDatabase()
	#dbFunc.printTable(database,'accellData')

	#dbFunc.printTable(database,'respData')

	try:
		while True:
			#Accept each communication
			data, addr = UDPFunc.recvUDP(server)
			#Create a new thread for each connection that is made
			thread.start_new_thread( serverController, (data,addr)) 
	except (KeyboardInterrupt, SystemExit):
		closeTCP(conn)
		server.close()


if __name__ == "__main__":
    main()









'''
	dbFunc.addEmergContactInfo(database,'emergList','Dom',6138239379,'dom@lalaland.com','_domkickone')

	pulseID = dbFunc.addDevice(database,'pulse','bpm')
	accellID = dbFunc.addDevice(database,'accell','N')
	respID = dbFunc.addDevice(database,'resp','mps')
	
	dbFunc.printTable(database,'deviceList')
	dbFunc.printTable(database,'emergList')
	#removeDevice(database,'accell')
	#deleteTable(database,'deviceList')
	dbFunc.addSensorData(database,'accell',accellID,{'fx':2,'fy':2,'fz':2,'ax':23.4,'ay':13.4,'az':3.4,})
	dbFunc.addSensorData(database,'pulse',pulseID,{'pulse':83.4})
	dbFunc.addSensorData(database,'resp',respID,{'resp':18.2})

	dbFunc.printTable(database,'accellData')
	dbFunc.printTable(database,'pulseData')
	dbFunc.printTable(database,'respData')
	'''