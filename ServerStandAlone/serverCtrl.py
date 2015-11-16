#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import random

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


import sched, time

DEF_DB_PATH = 'lifeBandDB.db'
#DEF_IP = '0.0.0.0'
DEF_IP = '172.17.148.20'
DEF_PORT = 5005

DEF_HALF_HOUR_IN_SECONDS = 10 #1800
DEF_1_DAY_IN_SECONDS = 86400
DEF_2_DAYS_IN_SECONDS = 172800

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

snapshotDataCols= [
					['timeStamp','REAL'],
					['heartBeat', 'REAL'],
					['breatheRate', 'REAL']
				]


def serverController(server,data,addr): 
	"""
	Function:	
	Serve the requests that is received by Phone or wearable

	Input arguments:
	args[0] : data that is contained in UDP packets
	args[1] : Address from the connection
	"""
	database = sqlite3.connect(DEF_DB_PATH)
	#print "Transmitted data: "+ data
	dataDecoded = json.loads(data)
	#print ("Decoded data: " + str(dataDecoded))

	if dataDecoded['id'] == "phone":
		print ("Phone data Received from "+str(addr))
		if dataDecoded['command'] == 'getLatestData':
			print ("Sending latest Data")

			pulseD = random.randint(50,160)
			respD = random.randint(50,160)
			accellD = random.randint(50,160)
			accellD = random.randint(50,160)
			resp = {'id':'server','command':'putLatestData','data':{'pulse':pulseD,'resp':respD,'accell':accellD}}
			server.sendto(json.dumps(resp), addr)

		elif dataDecoded['command'] == 'getPastData':
			print ("Sending past Data")

		elif dataDecoded['command'] == 'addEmergencyContact':
			addEmergContactInfo(conn,'emergList',dataDecoded['data'])
		elif dataDecoded['command'] == 'remEmergencyContact':
			remEmergContactInfo(conn,'emergList',dataDecoded['data'])

	elif dataDecoded['id'] == "wearable":
		print ("Wearable data Received from "+str(addr))
		if dataDecoded['command'] == 'addPulseData':
			print ("Adding pulse data to database")
			dbFunc.addSensorData(database,'pulse',pulseID,dataDecoded['data'])
			#dbFunc.printTable(database,'pulseData')

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

	database.close()


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
	dbFunc.createTable(conn,'snapshotData', snapshotDataCols )

	pulseID = dbFunc.addDevice(conn,'pulse','bpm')
	accellID = dbFunc.addDevice(conn,'accell','N')
	respID = dbFunc.addDevice(conn,'resp','mps')

	conn.close()


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

	conn.cursor().execute('DELETE FROM deviceList WHERE timeStamp < '+str(time.time()-DEF_2_DAYS_IN_SECONDS))
	
	conn.commit()

	conn.close()




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

def calculateHourlyData(sched): 
	try:
		print ("\tCalculating average values")
		conn = sqlite3.connect(DEF_DB_PATH)
		#dbFunc.printTable(conn,'pulseData')
		data = list()
		query = conn.cursor().execute('SELECT pulse FROM pulseData WHERE timeStamp > ? ', [(time.time()-(time.time()%DEF_HALF_HOUR_IN_SECONDS))] )
		#query = conn.cursor().fetchall()
		#print (str(conn.cursor().fetchall()))
		for row in query:
			data.append(str(row))
			#print(row)

		print(data)
		#query =  [i[1] for i in query]
		#print(type(query))
		#print(query)
		#print(type(query[0]))
		pulsePerHour = (lambda x, y: x + y, data )/ len(data)

		#query =conn.cursor().execute('SELECT resp FROM respData WHERE timeStamp<'+str(time.time())+' AND timeStamp > '+str(time.time()-(time.time()%DEF_HALF_HOUR_IN_SECONDS)))
		#query = conn.fetchall()
		#respPerHour = (lambda x, y: x + y, query )/ len(query)

		#dbFunc.addSnapshotData(conn,'snapshotData',{'heartBeat':pulsePerHour,'breatheRate':respPerHour})

		conn.close()

		sched.enter(DEF_HALF_HOUR_IN_SECONDS, 1, calculateHourlyData, (sched,))
	except KeyboardInterrupt:
		print ("Shutdown requested...exiting")
		sys.exit(0)
	#except Exception:
#		traceback.print_exc(file=sys.stdout)
	#sys.exit(0)

def timerSched():
	s = sched.scheduler(time.time, time.sleep)
	s.enter(DEF_HALF_HOUR_IN_SECONDS, 1, calculateHourlyData, (s,))
	s.run()


def main():



	#Create the server socket and bind it to the IP and the PORT
	server = UDPFunc.createUDPSocket(DEF_IP,DEF_PORT)

	createSensorDatabase()
	#timerThread = Thread(target = timerSched, args = [])
	#timerThread.start()
	
	#thread.start_new_thread( maintainDatabaseSize,(None,None)) 
	try:
		while True:
			#print("Email Thread Creation")
			#thread = Thread(target = emailHandler, args = [])
			#thread.start()
			#print("Email Thread Creation")
			#Accept each communication
			data, addr = UDPFunc.recvUDP(server)
			#Create a new thread for each connection that is made
			thread = Thread(target = serverController, args = (server,data,addr))
			thread.start()
			#thread.start_new_thread( serverController, (data,addr)) 
	except (KeyboardInterrupt, SystemExit):
		closeTCP(conn) 
		server.close()


if __name__ == "__main__":
    main()





