import psycopg2

def create_query():
	pass

def connect():
	connection = psycopg2.connect("dbname='spatial' user='postgres' host='localhost' password='password'")
	return connection

def executeQuery(iso, connection):
	query = create_query(iso)
	cursor = connection.cursor()
	cursor.execute(query)
	records = cursor.fetchall()
	return records

def disconnect(connection):
	connection.close()