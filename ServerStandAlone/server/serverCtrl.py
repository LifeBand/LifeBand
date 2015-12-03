#!/usr/bin/env python

from __future__ import print_function

__author__ = "Irusha Vidanamadura"
__date__ = "11-23-2015"


import os
import sys
import random


import socket
import time
from threading import Thread
import json, socket
import sqlite3
import sched


#Google Email API
import httplib2
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


#Custom files
import UDPFunc
import databaseFunc as dbFunc
import googleEmailApiFunc as emailAPI
import serverModl

#Google Cloud Messenging API
from gcm import GCM




DEF_HALF_HOUR_IN_SECONDS = 1800
DEF_1_DAY_IN_SECONDS = 86400
DEF_2_DAYS_IN_SECONDS = 172800






class ServerController():

	def __init__(self, database_path, ip, listen_port,send_port,serv_model):
		"""
		Function:
		To initialize the instance variables

		Input arguments:

		dataBasePath: The path of the database
		IP: The IP the server is binded to
		PORT: The port the server is binded to
		servModel: The model that handles the database communications


		"""
		self.DEF_DB_PATH = database_path
		self.DEF_IP = ip
		self.DEF_LISTEN_PORT = listen_port
		self.DEF_SEND_PORT = send_port
		self.DEF_MODEL = serv_model





	def network_handler(self,conn,received_data,(received_ip,received_port)):
		"""
		Function:
		Serve the requests that is received by Phone or wearable

		Input arguments:
		args[0] : data that is contained in UDP packets
		args[1] : Address from the connection
		"""


		data_decoded = json.loads(received_data)

		if data_decoded['id'] == "phone":
			print (str(time.ctime())+"Phone data Received from "+str(received_ip))
			self.phone_network_handler(conn,received_data,(received_ip,received_port))

		elif data_decoded['id'] == "wearable":
			print (str(time.ctime())+"Wearable data Received from "+str(received_ip))
			self.wearable_network_handler(conn,received_data,(received_ip,received_port))
		else:
			print('ERROR:Message from unknown sender')


	def phone_network_handler(self,conn,received_data,(received_ip,received_port)):
		if data_decoded['command'] == 'getPastDataSet':
			print ('\t'+"Sending past Pulse Data")
			conn.sendto(
					json.dumps(
							self.DEF_MODEL.get_past_data_from_db(
									json.loads(data_decoded['data'].decode('utf-8'))
							)
					),
					(received_ip,self.DEF_SEND_PORT))



		elif data_decoded['command'] == 'addEmergencyContact':
			print ('\t'+"Adding Emergency Data")
			self.DEF_MODEL.emerg_contact_change_to_db(
					'add',
					'emergList',
					json.loads(data_decoded['data'].decode('utf-8')))

		elif data_decoded['command'] == 'getEmergencyContact':
			print ('\t'+"Getting Emergency Data")
			conn.sendto(
					json.dumps(
							self.DEF_MODEL.emerg_contact_get_from_db(
									json.loads(data_decoded['data'].decode('utf-8'))
							)
					),
					(received_ip,self.DEF_SEND_PORT))


		elif data_decoded['command'] == 'remEmergencyContact':
			print ('\t'+"Removing Emergency Data")
			self.DEF_MODEL.emerg_contact_change_to_db('rem',
					json.loads(data_decoded['data'].decode('utf-8'))
					)
		else:
			print('\t ERROR: Unknown Command Received from Phone')





	def wearable_network_handler(self,conn,received_data,(received_ip,received_port)):
		if data_decoded['command'] == 'addSensorData':
			print ('\t'+"Adding pulse data to database")
			self.DEF_MODEL.add_sensor_data_to_db(
					'pulse',
					data_decoded['data']
			)

		elif data_decoded['command'] == 'truePositiveAlarm':
			print ('\t'+"Adding True Positive Alarm to database")
			self.DEF_MODEL.add_alarm_to_db(

				'TRUE',
					data_decoded['data'])

			self.send_alert_phone()
			emergency_contact_data = self.DEF_MODEL.get_emerg_contact_from_db()['data']

			for contact in emergency_contact_data:
				self.send_alert_email(emergency_contact_data[index])

		elif data_decoded['command'] == 'falsePositiveAlarm':
			print ('\t'+"Adding False Positive Alarm to database")
			self.DEF_MODEL.add_alarm_to_db('FALSE',
					data_decoded['data'])

		elif data_decoded['command'] == 'getPatientInfo':
			print ('\t'+"Sending Patient Info from database")
			conn.sendto(
					json.dumps(self.DEF_MODEL.get_patient_info_from_db(
							data_decoded['data'])
							),
					(received_ip,self.DEF_SEND_PORT))

		else:
			print('\t ERROR: Unknown Command Received from Wearable')



	def send_alert_email(self, conn,contact_data,latest_data):
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

		message = emailAPI.CreateMessage('LifeBandCenter@gmail.com',
				str(contact_data[2]),
				'LifeBand: PATIENT AT RISK AT '+str(time.time()),
				'Dear '+contact_data[0]+
				'\r\n LifeBand is measuring alarming biometrics.'+
				' Please check on your Patient\r\n\n'+
				'Patient: '+
				str(self.DEF_MODEL.get_patient_info_from_db()['data']['name'])+
				' IS AT RISK. BPM: '+
				str(self.DEF_MODEL.get_latest_data_from_db()['data']['bpm'])+
				' Force felt: '+
				str(self.DEF_MODEL.get_latest_data_from_db()['data']['forceMag'])+
				'\r\n\nThis message is automatically created by LifeBand')

		emailAPI.SendMessage(service, 'me', message)


	def run_server(self):
		"""
		Function:
		Coordinates incoming network requests to the server

		Input arguments:
		None

		Output variables:
		None
		"""


		try:
			server = UDPFunc.createUDPSocket(self.DEF_IP,self.DEF_LISTEN_PORT)

			self.DEF_MODEL.start_snpashot_routine()
			self.DEF_MODEL.change_emerg_contact_in_db('add',{'name':'Irusha','phone':8002394231,'email':'irusha.dilshan@gmail.com'})
			
			while True:

				#Accept each communication
				data, addr = UDPFunc.recvUDP(server)
				#Create a new thread for each connection that is made
				thread = Thread(target = self.network_handler, args = (server,data,addr))
				thread.daemon = True
				thread.start()
		except (KeyboardInterrupt, SystemExit):
			closeTCP(conn)
			server.close()

	def send_alert_phone(self):
		self.sendNotification('ALERT for Patient: '+
				str(self.DEF_MODEL.get_patient_info_from_db()['data']['name'])+
				' IS AT RISK. BPM: '+
				str(self.DEF_MODEL.get_latest_data_from_db()['data']['bpm'])+
				' Force felt: '+
				str(self.DEF_MODEL.get_latest_data_from_db()['data']['forceMag'])
				)

	def sendNotification(self,send_message):
		gcm = GCM('AIzaSyBsLNoI0qIGImUA31Fbz9YZeAZXMMmHktg')
		data = {'message':str(send_message),'to':'/topics/global'}
		# Topic Messaging
		topic = 'global'
		gcm.send_topic_message(topic=topic, data=data)
