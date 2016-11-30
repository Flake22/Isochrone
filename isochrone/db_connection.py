import psycopg2

def connect():
	connection = psycopg2.connect("dbname='spatial' user='postgres' host='localhost' password='password'")
	return connection

def executeQuery(query, connection):
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    return records

def disconnect(connection):
	connection.close()