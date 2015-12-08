import unittest
import time
import os
import databaseFunc
import sqlite3


class TestDatabaseFunctions(unittest.TestCase):

	def setUp(self):
		try:
		    os.remove(filename)
		except OSError:
		    pass
		self.testDBFile = 'testDB.db'
		conn = sqlite3.connect(self.testDBFile)
		self.assertTrue( os.path.isfile(self.testDBFile))

	def test_create_database(self):
		seed = time.time(self)
		self.testDBFile = 'testDB'+str(seed)+'.db'
		conn = sqlite3.connect(self.testDBFile)
		self.assertTrue( os.path.isfile(self.testDBFile))
		os.remove(self.testDBFile)


	def test_create_table(self):

		create_table(conn,tableName,columns)


	def test_delete_table(self,conn,tableName):

	def test_add_emergency_contact_info(self,conn,tableName,data):

		add_emergency_contact_info(conn,tableName,data)

	def test_rem_emergency_contact_info(self):
		rem_emergency_contact_info(conn,tableName,data)

	def test_get_emergency_contact_info(self):
		get_emergency_contact_info(conn, tableName)

	def test_add_alarm_data(self):
		add_alarm_data(conn,tableName,status)

	def create_sensor_data_table(self):

		create_sensor_data_table(conn,devCols)

	def test_add_sensor_data(self):
		add_sensor_data(conn,tableName, data)

	def test_add_snapshot_data(self):

		add_snapshot_data(conn, tableName, data):


	def test_print_table(self):
		print_table(conn,tableName):


	def test_checkForSQLInjection(self):

		checkForSQLInjection(checkString)


if __name__ == '__main__':
    unittest.main(self)
