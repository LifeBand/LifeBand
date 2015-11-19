#!/usr/bin/env python


from __future__ import print_function
import os
import sys
import random


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
import serverModl


import sched, time

DEF_HALF_HOUR_IN_SECONDS = 10 #1800
DEF_1_DAY_IN_SECONDS = 86400
DEF_2_DAYS_IN_SECONDS = 172800






class serverController():

	def __init__(self, dataBasePath, IP, PORT,servModel):

		self.DEF_DB_PATH = dataBasePath #'lifeBandDB.db'
		self.DEF_IP = IP#'172.17.148.20'
		self.DEF_PORT = PORT#5005
		#self.DEF_PORT_SEND = PORT_Send
		self.model = servModel





	def networkHandler(self,conn,receivedData,(receivedIP,receivedPORT)): 
		"""
		Function:	
		Serve the requests that is received by Phone or wearable

		Input arguments:
		args[0] : data that is contained in UDP packets
		args[1] : Address from the connection
		"""

		#database = sqlite3.connect(DEF_DB_PATH)

		dataDecoded = json.loads(receivedData)
		
		if dataDecoded['id'] == "phone":
			print (str(time.ctime())+"Phone data Received from "+str(receivedIP))

			if dataDecoded['command'] == 'getLatestData':
				print ('\t'+"Sending latest Data")
				conn.sendto(json.dumps(self.model.getLatestDataFromDB()), (receivedIP,self.DEF_PORT))


			elif dataDecoded['command'] == 'getPastData':
				print ('\t'+"Sending past Data")


			elif dataDecoded['command'] == 'addEmergencyContact':
				print ('\t'+"Adding Emergency Data")
				self.model.emergContactChangeToDB('add','emergList',dataDecoded['data'])


			elif dataDecoded['command'] == 'remEmergencyContact':
				print ('\t'+"Removing Emergency Data")
				self.model.emergContactChangeToDB('rem','emergList',dataDecoded['data'])


		elif dataDecoded['id'] == "wearable":
			print (str(time.ctime())+"Wearable data Received from "+str(receivedIP))

			if dataDecoded['command'] == 'addPulseData':
				print ('\t'+"Adding pulse data to database")
				self.model.addSensorDataToDB('pulse',dataDecoded['data'])


			elif dataDecoded['command'] == 'addRespData':
				print ('\t'+"Adding respiratory data to database")
				self.model.addSensorDataToDB('resp',dataDecoded['data'])

				
			elif dataDecoded['command'] == 'addAccelData':
				print ('\t'+"Adding accelerometer data to database")
				self.model.addSensorDataToDB('accell',dataDecoded['data'])


			elif dataDecoded['command'] == 'truePositiveAlarm':
				print ('\t'+"Adding True Positive Alarm to database")
				self.model.addAlarmToDB('TRUE')


			elif dataDecoded['command'] == 'falsePositiveAlarm':
				print ('\t'+"Adding False Positive Alarm to database")
				self.model.addAlarmToDB('FALSE')



	




	def emailHandler(self):
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

	

	def runServer(self):
		server = UDPFunc.createUDPSocket(self.DEF_IP,self.DEF_PORT)

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
				thread = Thread(target = self.networkHandler, args = (server,data,addr))
				thread.start()
		except (KeyboardInterrupt, SystemExit):
			closeTCP(conn) 
			server.close()


#	if __name__ == "__main__":
#	    main()





