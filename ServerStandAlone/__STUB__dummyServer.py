#!/usr/bin/env python

from __future__ import print_function


__author__ = "Irusha Vidanamadura"
__date__ = "11-23-2015"


import os
import sys
import random

sys.path.append(os.getcwd()+'/lib')

import socket
import time
from threading import Thread
import json
import sqlite3


#Custom files
import UDPFunc
import databaseFunc as dbFunc



class ServerController():

	def __init__(self, ip, port_Listen, port_Send):
		"""
		Function:
		To initialize the instance variables

		Input arguments:

		dataBasePath: The path of the database
		IP: The IP the server is binded to
		PORT: The port the server is binded to
		servModel: The model that handles the database communications


		"""
		self.listen_ip = ip
		self.listen_port = port_Listen
		self.send_port = port_Send;





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

			if data_decoded['command'] == 'getLatestData':
				print ('\t'+"Sending latest Data")


				response = {'id':'server','command':'putLatestData','data':{'pulse':random.randint(50,160),'accell':random.randint(0,10)}}
				conn.sendto(json.dumps(response, (received_ip,self.send_port)))


			elif data_decoded['command'] == 'getPastDataSet':
				print ('\t'+"Sending past Data")
				currTime = time.time();

				dataSet = {}
				for i in range (currTime- data_decoded['data'], currTime):
					dataSet[i] = [random.randint(50,160),random.randint(0,5)]

				response = {'id':'server','command':'putPastDataSet','data':dataSet}
				conn.sendto(json.dumps(response), (received_ip,self.send_port))


			elif data_decoded['command'] == 'addEmergencyContact':
				print ('\t'+"Adding Emergency Data")



			elif data_decoded['command'] == 'getEmergencyContact':
				print ('\t'+"Adding Emergency Data")


				dataSet = 	{	'1':{'name':'Nate','phone':'6281937281' , 'email':'gg@gg.com'},
								'2':{'name':'Gabe','phone':'6243433242' , 'email':'gg@dsadasdgg.com'}
							}

				response = {'id':'server','command':'putEmergencyData','data':dataSet }

				conn.sendto(json.dumps(response), (received_ip,self.send_port))



			elif data_decoded['command'] == 'remEmergencyContact':
				print ('\t'+"Removing Emergency Data")
			else:
				print('\t Unknown command')


		elif data_decoded['id'] == "wearable":
			print (str(time.ctime())+"Wearable data Received from "+str(received_ip))

			if data_decoded['command'] == 'addSensorData':
				print ('\t'+"Adding pulse data to database")

			elif data_decoded['command'] == 'truePositiveAlarm':
				print ('\t'+"Adding True Positive Alarm to database")


			elif data_decoded['command'] == 'falsePositiveAlarm':
				print ('\t'+"Adding False Positive Alarm to database")

			elif data_decoded['command'] == 'getPatientInfo':
				dataSet = {'name':'George', 'averageHeartRate':random.randint(60,80)}

				response = {'id':'server','command':'putPatientInfo','data':dataSet}
				conn.sendto(json.dumps(response), (received_ip,self.send_port))
			else:
				print('\t Unknown command')



	def run_server(self):
		"""
		Function:
		Coordinates incoming network requests to the server

		Input arguments:
		None

		Output variables:
		None
		"""

		server = UDPFunc.createUDPSocket(self.listen_ip,self.listen_port)


		print("Server STUB Created")
		try:
			while True:

				#Accept each communication
				data, addr = UDPFunc.recvUDP(server)
				#Create a new thread for each connection that is made
				thread = Thread(target = self.network_handler, args = (server,data,addr))
				thread.start()
		except (KeyboardInterrupt, SystemExit):
			closeTCP(conn)
			server.close()


def main():
	databse_path = 'lifeBandDB.db'
	listen_ip ='0.0.0.0'#'172.17.144.192'
	listen_port = 5005
	send_port = 6006


	controller = ServerController(listen_ip,listen_port,send_port) #receivelisten_port,sendlisten_port)
	controller.run_server()



if __name__ == "__main__":
    main()
