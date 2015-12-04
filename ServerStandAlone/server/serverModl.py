__author__ = "Irusha Vidanamadura"
__date__ = "11-23-2015"

import databaseFunc as dbFunc
import sqlite3
import random
import time
from threading import Timer
import numpy
import uuid
from collections import defaultdict

"""Dictionaries for established database structure"""
DEF_HALF_MINUTE_IN_SECONDS = 30 #1800
DEF_1_DAY_IN_SECONDS = 60
DEF_TABLE_NAME_EMERG = 'emergList'
DEF_TABLE_NAME_ALARM = 'alarmList'
DEF_TABLE_NAME_SENLIST = 'senList'
DEF_TABLE_NAME_SENSOR_DATA = 'sensorData'
DEF_TABLE_NAME_SNAPSHOT_DATA = 'snapshotData'
DEF_SNAPSHOT_DATA_INTERVAL = 10
DEF_WEARABLE_ID = 1

DEF_TABLE_COLS_EMERG = [
					['WearableID','INT'],
					['contactID','TEXT'] ,
					['name', 'TEXT'] ,
					['phone', 'INT'] ,
					['email','TEXT']
				]


DEF_TABLE_COLS_SENLIST = 	[
					['WearableID','INT'] ,
					['senID','TEXT'],
					['senName','TEXT'],
					['sampFreq', 'INT']
				]


DEF_TABLE_COLS_ALARM = [
					['timeStamp','INT'] ,
					['status', 'TEXT']
				]

DEF_TABLE_COLS_SNAPSHOT_DATA= [
					['timeStamp','INT'],
					['bpm', 'REAL'],
					['forceMag', 'REAL']
				]


DEF_TABLE_COLS_SENSOR_DATA = [
					['WearableID','INT'] ,
				#	['senID','TEXT'],
					['timeStamp', 'REAL'] ,
					['number', 'REAL']
				]

DEF_TABLE_COLS_BPM_DATA = [
					['WearableID','INT'] ,
					['senID','TEXT'],
					['timeStamp', 'REAL'] ,
					['bpm', 'REAL']
				]

DEF_TABLE_COLS_FORCEMAG_DATA = [
					['WearableID','INT'] ,
					['senID','TEXT'],
					['timeStamp', 'REAL'] ,
					['forceMag', 'REAL']
				]




class ServerModel():




	def __init__(self,database_path):
		self.dev_id_count = 0
		self.db_path = database_path
		self.contactID = 0
		self.sensor_ID_dict = dict()
		#self.pulse_id = 0
		#self.resp_id = 0
		#self.accell_id = 0

	def create_sensor_database(self):
		"""
		Function:
		Create the Database tables for syste

		Input arguments:
		None

		Output variables:
		None
		"""

		conn = sqlite3.connect(self.db_path)

		#dbFunc.create_table(conn,'deviceList',self.DEF_TABLE_COLS_DEVICES )

		dbFunc.create_table(conn,DEF_TABLE_NAME_EMERG, DEF_TABLE_COLS_EMERG )
		dbFunc.create_table(conn,DEF_TABLE_NAME_ALARM, DEF_TABLE_COLS_ALARM )
		dbFunc.create_table(conn,DEF_TABLE_NAME_SNAPSHOT_DATA, DEF_TABLE_COLS_SNAPSHOT_DATA )
		dbFunc.create_table(conn,DEF_TABLE_NAME_SENLIST, DEF_TABLE_COLS_SENLIST)


		conn.close()


	def maintain_databse_size(self):
		"""
		Function:
		Maintain the Database of sensor reading to within 90 days

		Input arguments:
		None

		Output variables:
		None
		"""

		conn = sqlite3.connect(self.db_path)

		conn.cursor().execute('DELETE FROM deviceList WHERE timeStamp < '+str(time.time()-DEF_2_DAYS_IN_SECONDS))
		conn.commit()

		conn.close()




	def get_latest_data_from_db(self):
		'''
		Function: Getting latest bpm and force Data from the Database
		Input arguments:
			None
		Outputs arguments:
		 	response (Dictionary) <-- Contains fields to be sent back
		'''
		conn = sqlite3.connect(self.db_path)
		query_data = list()
		response =  {'id':'server','command':'putLatestData','data':{'bpm':0,'forceMag':0} }

		query_data.append(conn.cursor().execute('SELECT bpm FROM bpmData ORDER BY timeStamp DESC LIMIT 1').fetchone())
		query_data.append(conn.cursor().execute('SELECT forceMag FROM forceMagData ORDER BY timeStamp DESC LIMIT 1').fetchone())

		#query_data =conn.cursor().execute('SELECT max(id) bpm, forceMag FROM bpmData INNER JOIN forceMagData on bpmData.timeStamp = forceMagData.timeStamp').fetchone()


		if query_data is not None:
			response['data']['bpm'] = query_data[0]
			response['data']['forceMag'] = query_data[1]
		return response


	def get_past_data_from_db(self,received_data):
		'''
		Function: Getting past BPM and Accell Data from the Database
		Input arguments:
			None
		Outputs arguments:
		 	response (Dictionary) <-- Contains fields to be sent back
		'''
		response_data ={}
		print received_data
		conn = sqlite3.connect(self.db_path)
		dbFunc.checkForSQLInjection(str(received_data['numPoints']))

		query_data = conn.cursor().execute('SELECT timeStamp,bpm,forceMag FROM  ' + DEF_TABLE_NAME_SNAPSHOT_DATA + ' ORDER BY timeStamp DESC LIMIT '+str(received_data['numPoints']) ).fetchall()
		#print query_data

		for row in query_data:
			#print row[1]
			response_data[str(row[0])] = [row[1],row[2]]
		print response_data
		response =  {'id':'server','command':'putLatestData','data':response_data,'latest':self.get_latest_data_from_db()['data']}
		return response


	def change_emerg_contact_in_db(self,behaviour,emerg_contact_data):
		"""
		Function: Removes or Adds the Emergency contact with the name passed in data
		"""
		if type(behaviour) == type(str()) and type(emerg_contact_data) == type(dict()):
			conn = sqlite3.connect(self.db_path)
			if behaviour == 'add':

				dbFunc.checkForSQLInjection(str(emerg_contact_data['name']))
				dbFunc.checkForSQLInjection(str(emerg_contact_data['phone']))
				dbFunc.checkForSQLInjection(str(emerg_contact_data['email']))

				conn.cursor().execute('INSERT INTO '+
						str(DEF_TABLE_NAME_EMERG)+
						' (WearableID,contactID,name,phone,email) VALUES (?,?,?,?,?)',
						(DEF_WEARABLE_ID,
						self.contactID,
						emerg_contact_data['name'],
						int(emerg_contact_data['phone']),
						emerg_contact_data['email']))
				conn.commit()
				self.contactID+= 1

			elif behaviour == 'rem':
				dbFunc.checkForSQLInjection(str(emerg_contact_data['name']))
				conn.cursor().execute('DELETE FROM '+str(DEF_TABLE_NAME_EMERG)+' WHERE name = \'' + str(emerg_contact_data['name'])+'\'')
				conn.commit()

			conn.close()
		else:
			print ("Error: change_emerg_contact_in_db: Incompatible Input parameter type "+ sys.exc_info()[0])
			raise

	def get_emerg_contact_from_db(self):
		"""
		Function: Gets all Emergency contact with the same name passed in data
		"""
		conn = sqlite3.connect(self.db_path)
		response = conn.cursor().execute('SELECT DISTINCT name,phone,email FROM '+
				str(DEF_TABLE_NAME_EMERG)+ ' WHERE WearableID = 1' ).fetchall();
		conn.close()
		return {'id':'server','command':'putEmergencyContact','data':response}

	def add_device_to_db(self,conn,sensor_name,samp_freq):

		self.sensor_ID_dict[str(sensor_name)] = str(uuid.uuid1())

		conn.cursor().execute('INSERT INTO '+DEF_TABLE_NAME_SENLIST+'(WearableID,senID, senName, sampFreq) VALUES (?,?,?,?)',(DEF_WEARABLE_ID,self.sensor_ID_dict[str(sensor_name)],sensor_name,str(samp_freq)))
		if(sensor_name=='bpm'):
			dbFunc.create_table(conn,sensor_name+'Data', DEF_TABLE_COLS_BPM_DATA)
		elif(sensor_name=='forceMag'):
			dbFunc.create_table(conn,sensor_name+'Data', DEF_TABLE_COLS_FORCEMAG_DATA)
		conn.commit()


	def remove_device_from_db(conn,sensor_name):

		conn.cursor().execute('DELETE FROM '+DEF_TABLE_NAME_SENLIST+' WHERE WearableID = '+str(DEF_WEARABLE_ID)+' AND senID = \'' + str(self.sensor_ID_dict[str(sensor_name)])+'\'')
		conn.commit()


	def add_sensor_data_to_db(self,sensor_name,sensor_data):
		if type(sensor_name) == type(str()) and type(sensor_data) == type(dict()):
			conn = sqlite3.connect(self.db_path)
			dbFunc.checkForSQLInjection(str(sensor_name))
			dbFunc.checkForSQLInjection(str(sensor_data['timeStamp']))
			dbFunc.checkForSQLInjection(str(sensor_data['number']))

			if(sensor_name not in self.sensor_ID_dict):
				self.add_device_to_db(conn,sensor_name,1);


			if(sensor_name=='bpm'):
				conn.cursor().execute('INSERT INTO '+str(sensor_name)+'Data(WearableID,senID,timeStamp,bpm) VALUES (?,?,?,?)',
							(DEF_WEARABLE_ID,
							self.sensor_ID_dict[str(sensor_name)],
							int(sensor_data['timeStamp']),
							round(sensor_data['number'],1)))
			elif(sensor_name=='forceMag'):
				conn.cursor().execute('INSERT INTO '+str(sensor_name)+'Data(WearableID,senID,timeStamp,forceMag) VALUES (?,?,?,?)',
							(DEF_WEARABLE_ID,
							self.sensor_ID_dict[str(sensor_name)],
							int(sensor_data['timeStamp']),
							round(sensor_data['number'],2)))
			conn.commit()
			conn.close()

		else:
			print ("Error: add_sensor_data_to_db: Incompatible Input parameter type "+ sys.exc_info()[0])
			raise




	def add_alarm_to_db(self,alarm_status,alarm_data):
		if type(alarm_status) == type(str()):
			conn = sqlite3.connect(self.db_path)
			conn.cursor().execute('INSERT INTO '+str(DEF_TABLE_NAME_ALARM)+'(timeStamp,status) VALUES (?,?)',(float(alarm_data['timeStamp']),alarm_status))
			conn.commit()
			conn.close()
		else:
			print ("Error: add_alarm_to_db: Input parameter not string"+ sys.exc_info()[0])
			raise

	def get_patient_info_from_db(self):
		try:
			#conn = sqlite3.connect(self.db_path)
			#data = get_emergency_contact_info(conn, tableName)
			#conn.close()
			dataSet = {'name':'George', 'min':60, 'max':100, 'change':15}

			return {'id':'server','command':'putPatientInfo','data':dataSet}

		except:
			print ("Error: get_patient_info_from_db: "+ sys.exc_info()[0])
			raise




	def start_snpashot_routine(self):
		self.wait_priodic_thread(1,0,DEF_SNAPSHOT_DATA_INTERVAL,self.calculate_snapshot_data)
		self.wait_priodic_thread(1,0,DEF_1_DAY_IN_SECONDS,self.remove_older_sensor_data)




	def wait_priodic_thread(self,interval,accu,total,subroutine):
		if accu >= total:
			subroutine()
		else:
			accu +=interval
			Timer(interval,self.wait_priodic_thread, (interval,accu,total,subroutine)).start()


	def remove_older_sensor_data(self):
		try:
			print ('----------------------------------\r\n'+str(time.ctime())+"\r\nDeleting data older than 2 days")
			conn = sqlite3.connect(self.db_path)
			for key in self.sensor_ID_dict:
				conn.cursor().execute('DELETE FROM '+key+'Data WHERE timeStamp < '+ str(int(time.time() - DEF_1_DAY_IN_SECONDS*2)) )
			conn.commit()
			conn.close()
			print ('----------------------------------\r\n')
			self.wait_priodic_thread(1,0,DEF_1_DAY_IN_SECONDS,self.remove_older_sensor_data)

		except KeyboardInterrupt:
			print ("Shutdown requested...exiting")
			sys.exit(0)

	def calculate_snapshot_data(self):
		try:
			print ('----------------------------------\r\n'+str(time.ctime())+"\r\nCalculating average values")
			data = list()
			dd = defaultdict(list)
			avgBPM = 0
			avgForceMag = 0
			conn = sqlite3.connect(self.db_path)
			last_check_time = time.time() - DEF_SNAPSHOT_DATA_INTERVAL
			conn.cursor().execute('CREATE TEMP TABLE lastBMP AS SELECT * FROM bpmData WHERE timeStamp > '+ str(last_check_time))
			conn.cursor().execute('CREATE TEMP TABLE lastForceMag AS SELECT * FROM forceMagData WHERE timeStamp > '+ str(last_check_time))

			conn.cursor().execute('SELECT bpm, forceMag FROM lastBMP INNER JOIN lastForceMag ON lastBMP.timeStamp = lastForceMag.timeStamp').fetchall()


			query_data_joined =conn.cursor().execute('SELECT bpm, forceMag FROM bpmData INNER JOIN forceMagData on bpmData.timeStamp = forceMagData.timeStamp').fetchall()

			conn.cursor().execute('DROP TABLE IF EXISTS lastBMP')
			conn.cursor().execute('DROP TABLE IF EXISTS lastForceMag')

			query_bpm = [row[0] for row in query_data_joined]
			query_force_mag = [row[1] for row in query_data_joined]

			avgBPM =  round(reduce(lambda x, y: x + y, query_bpm) / len(query_bpm),1)
			avgForceMag = round( reduce(lambda x, y: x + y, query_force_mag) / len(query_force_mag),2)

			print('Average BPM: '+str(avgBPM)+' Force: '+ str(avgForceMag))

			conn.cursor().execute('INSERT INTO '+ DEF_TABLE_NAME_SNAPSHOT_DATA + ' (timeStamp,bpm, forceMag) Values (?,?,?)',(last_check_time,avgBPM,avgForceMag))
			conn.commit()

			conn.close()
			print ('----------------------------------\r\n')
			self.wait_priodic_thread(1,0,DEF_SNAPSHOT_DATA_INTERVAL,self.calculate_snapshot_data)
		except KeyboardInterrupt:
			print ("Shutdown requested...exiting")
			sys.exit(0)
