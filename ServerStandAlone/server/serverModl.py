__author__ = "Irusha Vidanamadura"
__date__ = "11-23-2015"

import databaseFunc as dbFunc
import sqlite3
import random
import time
from threading import Timer
import numpy

"""Dictionaries for established database structure"""
DEF_HALF_MINUTE_IN_SECONDS = 30 #1800
DEF_1_DAY_IN_SECONDS = 60
DEF_TABLE_NAME_EMERG = 'emergList'
DEF_TABLE_NAME_ALARM = 'alarmList'
DEF_TABLE_NAME_SENSOR_DATA = 'sensorData'
DEF_TABLE_NAME_SNAPSHOT_DATA = 'snapshotData'
DEF_SNAPSHOT_DATA_INTERVAL = DEF_HALF_MINUTE_IN_SECONDS
DEF_WEARABLE_ID = 1

DEF_TABLE_COLS_EMERG = [
					['DEVID','INT'],
					['contactID','TEXT'] ,
					['name', 'TEXT'] ,
					['phone', 'INT'] ,
					['email','TEXT']
				]


DEF_TABLE_COLS_DEVICES = 	[
					['DEVID','INT'] ,
					['devName', 'TEXT'] ,
					['sampRate', 'INT'] ,
					['unit','TEXT']
				]


DEF_TABLE_COLS_ALARM = [
					['timeStamp','REAL'] ,
					['status', 'TEXT']
				]

DEF_TABLE_COLS_SNAPSHOT_DATA= [
					['timeStamp','REAL'],
					['bpm', 'REAL'],
					['forceMag', 'REAL']
				]
DEF_TABLE_COLS_SENSOR_DATA = [
					['DEVID','INT'] ,
					['timeStamp', 'REAL'] ,
					['bpm', 'REAL'] ,
					['forceMag','REAL']
				]

class ServerModel():




	def __init__(self,database_path):
		self.dev_id_count = 0
		self.db_path = database_path
		self.contactID = 0
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
		dbFunc.create_table(conn,DEF_TABLE_NAME_SENSOR_DATA, DEF_TABLE_COLS_SENSOR_DATA)


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
		Function: Getting latest BPM and Accell Data from the Database
		Input arguments:
			None
		Outputs arguments:
		 	response (Dictionary) <-- Contains fields to be sent back
		'''
		conn = sqlite3.connect(self.db_path)
		query_data = conn.cursor().execute('SELECT bpm,forceMag FROM ' + DEF_TABLE_NAME_SENSOR_DATA +' ORDER BY timeStamp DESC LIMIT 1' ).fetchone()
		return {'id':'server','command':'putLatestData','data':{'bpm':query_data[0],'forceMag':query_data[1]} }


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
		query_data = conn.cursor().execute('SELECT timeStamp,bpm,forceMag FROM  ' + DEF_TABLE_NAME_SENSOR_DATA + ' ORDER BY timeStamp DESC LIMIT '+str(received_data['numPoints']) ).fetchall()
		#print query_data

		for row in query_data:
			#print row[1]
			response_data[str(row[0])] = [row[1],row[2]]
		print response_data
		response =  {'id':'server','command':'putLatestData','data':response_data}
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
						' (DEVID,contactID,name,phone,email) VALUES (?,?,?,?,?)',
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
				str(DEF_TABLE_NAME_EMERG)+ ' WHERE DEVID = 1' ).fetchall();
		conn.close()
		return {'id':'server','command':'putEmergencyContact','data':response}


	def add_sensor_data_to_db(self,sensor_name,sensor_data):
		if type(sensor_name) == type(str()) and type(sensor_data) == type(dict()):
			conn = sqlite3.connect(self.db_path)

			dbFunc.checkForSQLInjection(str(sensor_data['timeStamp']))
			dbFunc.checkForSQLInjection(str(sensor_data['bpm']))
			dbFunc.checkForSQLInjection(str(sensor_data['forceMag']))

			conn.cursor().execute('INSERT INTO '+str(DEF_TABLE_NAME_SENSOR_DATA)+'(DEVID,timeStamp,bpm,forceMag) VALUES (?,?,?,?)',
					(DEF_WEARABLE_ID,
					float(sensor_data['timeStamp']),
					float(sensor_data['bpm']),
					float(sensor_data['forceMag'])) )
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



#	def get_latest_pulse_from_db(self,numPoints):
#		conn = sqlite3.connect(self.db_path)
#		query_data = conn.cursor().execute('SELECT timeStamp,pulse FROM pulseData DESC LIMIT '+str(numPoints)).fetchall()
#
#
#		response = {'id':'server','command':'putLatestData','data':query_data}
#
	#	return response

	def start_snpashot_routine(self):
		self.wait_priodic_thread(1,0,DEF_SNAPSHOT_DATA_INTERVAL,self.calculate_snapshot_data)
		self.wait_priodic_thread(1,0,DEF_1_DAY_IN_SECONDS,self.remove_older_sensor_data)


		#Timer(DEF_SNAPSHOT_DATA_INTERVAL, self.calculate_snapshot_data, () ).start()
		#Timer(DEF_1_DAY_IN_SECONDS, self.remove_older_sensor_data, () ).start()

	def wait_priodic_thread(self,interval,accu,total,subroutine):
		if accu >= total:
			subroutine()
		else:
			accu +=interval
			Timer(interval,self.wait_priodic_thread, (interval,accu,total,subroutine)).start()


	def remove_older_sensor_data(self):
		try:
			print ('\t'+str(time.ctime())+"Deleting data older than 2 days")
			conn = sqlite3.connect(self.db_path)
			conn.cursor().execute('DELETE FROM '+DEF_TABLE_NAME_SENSOR_DATA+' WHERE timeStamp < '+ str(time.time() - DEF_1_DAY_IN_SECONDS*2) )
			conn.commit()
			conn.close()
			self.wait_priodic_thread(1,0,DEF_1_DAY_IN_SECONDS,self.remove_older_sensor_data)
			#Timer(DEF_1_DAY_IN_SECONDS, self.remove_older_sensor_data, () ).start()
		except KeyboardInterrupt:
			print ("Shutdown requested...exiting")
			sys.exit(0)

	def calculate_snapshot_data(self):
		try:
			print ('\t'+str(time.ctime())+"Calculating average values")
			conn = sqlite3.connect(self.db_path)
			data = list()
			last_30_second_floor = time.time() - 30 #((time.time()-10)%DEF_SNAPSHOT_DATA_INTERVAL)
			query = conn.cursor().execute('SELECT bpm,forceMag FROM '+DEF_TABLE_NAME_SENSOR_DATA+' WHERE timeStamp > '+ str(last_30_second_floor) ).fetchall()
			#print query
			if query is not None:
				for row in query:
					data.append(row[0])
				avgBPM =  reduce(lambda x, y: x + y, data) / len(data)

				data = list()
				for row in query:
					data.append(row[1])
				avgForceMag =  reduce(lambda x, y: x + y, data) / len(data)

				print avgBPM , avgForceMag

				conn.cursor().execute('INSERT INTO '+ DEF_TABLE_NAME_SNAPSHOT_DATA + ' (timeStamp,bpm, forceMag) Values (?,?,?)',(last_30_second_floor,avgBPM,avgForceMag))
				conn.commit()

				#dbFunc.print_table(conn,DEF_TABLE_NAME_SNAPSHOT_DATA)

				conn.close()
			self.wait_priodic_thread(1,0,DEF_SNAPSHOT_DATA_INTERVAL,self.calculate_snapshot_data)
			#Timer(DEF_SNAPSHOT_DATA_INTERVAL, self.calculate_snapshot_data, () ).start()
		except KeyboardInterrupt:
			print ("Shutdown requested...exiting")
			sys.exit(0)
