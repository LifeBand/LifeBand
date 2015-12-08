import sqlite3
import time
import datetime
import uuid



def create_table(conn,tableName,columns):
	'''
	Function: Create a table with the specified name and columns passed in
	'''
	checkForSQLInjection(tableName)

	query = 'CREATE TABLE IF NOT EXISTS '+str(tableName)+' ('

	for i in range(0,len(columns)-1):
		query +=str(columns[i][0])+' ' +str(columns[i][1])+', '
	query +=str(columns[len(columns)-1][0])+' ' +str(columns[len(columns)-1][1])
	query +=')'
	conn.cursor().execute(query)



def delete_table(conn,tableName):
	'''
	Function: Delete a table with the specified name passed in
	'''
	checkForSQLInjection(tableName)
	conn.cursor().execute('DROP TABLE IF EXISTS '+str(tableName))


def print_table(conn,tableName):
	'''
	Function: Print the table in the database with column names
	'''
	print'\n-------------------------\nPrinting Table ',tableName
	cursor = conn.execute('SELECT * from '+str(tableName))
	colNames = [description[0] for description in cursor.description]
	print colNames

	table = conn.cursor().execute('SELECT * FROM '+str(tableName))
	for row in table:
		print row



def checkForSQLInjection(checkString):
	'''
	Function: Check if the the input string has any malicious code injections
	'''
	assert('\'' not in checkString)
	assert(';' not in checkString)
	assert('AND' not in checkString)
	assert('OR' not in checkString)
