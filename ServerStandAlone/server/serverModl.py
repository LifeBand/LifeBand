import databaseFunc as dbFunc
import sqlite3
import random
import time
class serverModel():

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

	pulseDataCols = [	 
						['DEVID','TEXT'] , 
						['timeStamp', 'REAL'] , 
						['pulse', 'REAL'] 
					]

	respDataCols = 	[	 
						['DEVID','TEXT'] , 
						['timeStamp', 'REAL'] , 
						['resp', 'REAL'] 
					]

	accellDataCols= [	 
						['DEVID','TEXT'] , 
						['timeStamp', 'REAL'] , 
						['fx', 'REAL'] ,
						['fy', 'REAL'] ,
						['fz', 'REAL'] ,
						['ax', 'REAL'] ,
						['ay', 'REAL'] ,
						['az', 'REAL'] 
					]

	def __init__(self,dataBasePath):
		self.devIDCount = 0
		self.DEF_DB_PATH = dataBasePath 
		self.pulseID = 0
		self.respID = 0
		self.accellID = 0


	def addAlarmToDB(self,alarmStatus):
		if type(alarmStatus) == type(str()):
			conn = sqlite3.connect(self.DEF_DB_PATH)
			dbFunc.addAlarmData(conn,'alarmList',alarmStatus)
			conn.close()
		else:
			print ("Error: addAlarmToDB: Input parameter not string"+ sys.exc_info()[0])
			raise 

	def addSensorDataToDB(self,sensorName,sensorData):
		if type(sensorName) == type(str()) and type(sensorData) == type(dict()):
			conn = sqlite3.connect(self.DEF_DB_PATH)
			if sensorName == 'accell':
				dbFunc.addSensorData(conn,sensorName,self.accellID,sensorData)
			elif sensorName == 'resp':
				dbFunc.addSensorData(conn,sensorName,self.respID,sensorData)
			elif sensorName == 'pulse':
				dbFunc.addSensorData(conn,sensorName,self.pulseID,sensorData)
			conn.close()
		else:
			print ("Error: addSensorDataToDB: Incompatible Input parameter type "+ sys.exc_info()[0])
			raise 



	def changeEmergContactTDB(self,behaviour,emergContactData):
		if type(behaviour) == type(str()) and type(emergContactData) == type(dict()):
			if behaviour == 'add':
				addEmergContactInfo('add','emergList',emergContactData)
			elif behaviour == 'rem':
					remEmergContactInfo('rem','emergList',emergContactData)
			conn.close()
		else:
			print ("Error: changeEmergContactTDB: Incompatible Input parameter type "+ sys.exc_info()[0])
			raise 

	

	def createSensorDatabase(self):
		"""
		Function:	
		Create the Database tables for syste

		Input arguments:
		None

		Output variables:
		None
		"""

		conn = sqlite3.connect(self.DEF_DB_PATH)

		dbFunc.createTable(conn,'deviceList',self.devListCols )
		dbFunc.createTable(conn,'emergContactList', self.emergListCols )
		dbFunc.createTable(conn,'alarmList', self.emergListCols )
		dbFunc.createTable(conn,'snapshotData', self.snapshotDataCols )

		self.pulseID = dbFunc.addDevice(conn,'pulse','bpm',self.pulseDataCols)
		self.accellID = dbFunc.addDevice(conn,'accell','N',self.accellDataCols)
		self.respID = dbFunc.addDevice(conn,'resp','mps',self.respDataCols)

		conn.close()


	def maintainDatabaseSize(self):
		"""
		Function:	
		Maintain the Database of sensor reading to within 90 days

		Input arguments:
		None

		Output variables:
		None
		"""

		conn = sqlite3.connect(self.DEF_DB_PATH)

		conn.cursor().execute('DELETE FROM deviceList WHERE timeStamp < '+str(time.time()-DEF_2_DAYS_IN_SECONDS))
		conn.commit()

		conn.close()


	def getLatestDataFromDB(self):
		conn = sqlite3.connect(self.DEF_DB_PATH)
		queryPulse = conn.cursor().execute('SELECT pulse FROM pulseData ORDER BY timeStamp DESC LIMIT 1' ).fetchone()
			
		'''
		pulseD = random.randint(50,160)
		respD = random.randint(50,160)
		accellD = random.randint(50,160)
		accellD = random.randint(50,160)
		conn.close()
		response = {'id':'server','command':'putLatestData','data':{'pulse':pulseD,'resp':respD,'accell':accellD}}
		'''
		
		response = {'id':'server','command':'putLatestData','data':{'pulse':queryPulse[0],'resp':99,'accell':62}}
		
		return response

	def getpulseDataSetFromDB(self,numPoints):
		conn = sqlite3.connect(self.DEF_DB_PATH)
		queryPulse = conn.cursor().execute('SELECT timeStamp,pulse FROM pulseData DESC LIMIT '+str(numPoints)).fetchall()
			
		'''
		pulseD = random.randint(50,160)
		respD = random.randint(50,160)
		accellD = random.randint(50,160)
		accellD = random.randint(50,160)
		conn.close()
		response = {'id':'server','command':'putLatestData','data':{'pulse':pulseD,'resp':respD,'accell':accellD}}
		'''
		
		response = {'id':'server','command':'putLatestData','data':queryPulse}
		
		return response


	def startDataCalculation(self):
		s = sched.scheduler(time.time, time.sleep)
		s.enter(DEF_HALF_HOUR_IN_SECONDS, 1, calculateHourlyData, (s,))
		s.run()

	def calculateHourlyData(self,sched): 
		try:
			print ('\t'+str(time.ctime())+"Calculating average values")
			conn = sqlite3.connect(DEF_DB_PATH)
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
			#traceback.print_exc(file=sys.stdout)
		#sys.exit(0)


