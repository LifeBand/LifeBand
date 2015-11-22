import unittest
import os
import databaseFunc
import sqlite3


class TestDatabaseFunctions(unittest.TestCase):
	def setUp(self):
		self.testDBFile = 'testDB.db'
		conn = sqlite3.connect(self.testDBFile)
		self.assertTrue( os.path.isfile(self.testDBFile))

	def testAddTable(self):
		conn.cursor().execute('CREATE TABLE TestTable(ID INT, STR TEXT)')
		


def main():
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

