import sqlite3
import time
import datetime
import uuid

DEF_HALF_HOUR_IN_SECONDS = 60 #3600
DEF_1_DAY_IN_SECONDS = 86400
devIDCount = 0

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
				

def createTable(conn,tableName,columns):
	
	query = 'CREATE TABLE IF NOT EXISTS '+str(tableName)+' ('
	for i in range(0,len(columns)-1):
		query +=str(columns[i][0])+' ' +str(columns[i][1])+', '
	query +=str(columns[len(columns)-1][0])+' ' +str(columns[len(columns)-1][1])
	query +=')'
	
	conn.cursor().execute(query)
	


def addEmergContactInfo(conn,tableName,data):

	contactUUID = str(uuid.uuid1()) 
	conn.cursor().execute('INSERT INTO '+str(tableName)+' (contactID,name,phone,email,twitter) VALUES (?,?,?,?,?)',(contactUUID,data['name'],data['phone'],data['email'],data['twitter']))
	conn.commit()
	return contactUUID

def remEmergContactInfo(conn,tableName,data):
	"""
	Function: Removes the Emergency contact with the same name passed in data
	"""
	conn.cursor().execute('DELETE FROM'+str(tableName)+' WHERE name = \'' + str(data['name'])+'\'')
	conn.commit()


def addAlarmData(conn,tableName,status):

	conn.cursor().execute('INSERT INTO '+str(tableName)+' (timeStamp,status) VALUES (?,?)',(int(time.time()),status))
	conn.commit()


def createSensorDataTable(conn,devName):
	if devName=='accell':
		createTable(conn,devName+'Data',accellDataCols)

	elif devName == 'pulse':
		createTable(conn,devName+'Data',pulseDataCols)


	elif devName == 'resp':
		createTable(conn,devName+'Data',respDataCols)

def deleteTable(conn,tableName):
	conn.cursor().execute('DROP TABLE IF EXISTS '+str(tableName))



def addDevice(conn,devName,unit):
	global devIDCount
	devUUID =str(uuid.uuid1()) 
	conn.cursor().execute('INSERT INTO deviceList (DEVID, devName,unit) VALUES (?,?,?)',(devUUID,str(devName),unit))
	devIDCount+=1
	conn.commit()
	createSensorDataTable(conn,str(devName))
	return devUUID

def removeDevice(conn,devName,devID):
	global devIDCount
	conn.cursor().execute('DELETE FROM deviceList WHERE DEVID = \'' + str(devID)+'\'')
	conn.cursor().execute('DELETE FROM '+str(devName)+'Data WHERE DEVID = \'' + str(devID)+'\'')
	devIDCount-=1
	conn.commit()

def addSensorData(conn,devName,devID,data):

	if devName=='accell':
		conn.cursor().execute('INSERT INTO '+str(devName)+'Data (DEVID,timeStamp,fx,fy,fz,ax,ay,az) VALUES (?,?,?,?,?,?,?,?)',(devID,int(time.time()),data['fx'],data['fy'],data['fz'],data['ax'],data['ay'],data['az']))
		conn.commit()

	elif devName == 'pulse':
		conn.cursor().execute('INSERT INTO '+str(devName)+'Data (DEVID,timeStamp,pulse) VALUES (?,?,?)',(devID,int(time.time()),data['pulse']))
		conn.commit()

	elif devName == 'resp':
		conn.cursor().execute('INSERT INTO '+str(devName)+'Data (DEVID,timeStamp,resp) VALUES (?,?,?)',(devID,int(time.time()),data['resp']))
		conn.commit()
	
def addSnapshotData(conn,tableName, data):
	conn.cursor().execute('INSERT INTO '+str(timeScale)+'Data (timeStamp,heartBeat, breatheRate) Values (?,?,?)',(time.time()-(time.time()%DEF_HALF_HOUR_IN_SECONDS),data['heartBeat'],data['breatheRate']))
	conn.commit()
	
def printTable(conn,tableName):
	print'\n-------------------------\nPrinting Table ',tableName
	cursor = conn.execute('SELECT * from '+str(tableName))
	colNames = [description[0] for description in cursor.description]
	print colNames

	table = conn.cursor().execute('SELECT * FROM '+str(tableName))
	for row in table:
		print row

'''
def main():
	global devIDCount
	devIDCount = 0
	conn = sqlite3.connect('ddd.db')
	cursor = conn.cursor()
	createTable(conn,'deviceList',devListCols )
	createTable(conn,'emergList', emergListCols )
	
	
	pulseID = addDevice(conn,'pulse','bpm')
	accellID = addDevice(conn,'accell','N')
	respID = addDevice(conn,'resp','mps')
	printTable(conn,'deviceList')
	printTable(conn,'emergList')
	#removeDevice(conn,'accell')
	#deleteTable(conn,'deviceList')
	addSensorData(conn,'accell',accellID,{'fx':2,'fy':2,'fz':2,'ax':23.4,'ay':13.4,'az':3.4,})
	addSensorData(conn,'pulse',pulseID,{'pulse':83.4})
	addSensorData(conn,'resp',respID,{'resp':18.2})

	printTable(conn,'accellData')
	printTable(conn,'pulseData')
	printTable(conn,'respData')


if __name__ == "__main__":
	main()
'''
