import os

import config as c

def get_access_type():
	return c.access_type

def get_key(): 
	#get access type
	access_type=get_access_type()

	#get Google Maps configuration settings
	if access_type == 'personal':
		return c.api_number
	if access_type == 'business':
		return api.client_id

def get_dbname ():
	return c.dbname 

def get_user():
	return c.user

def get_host():
	return c.host

def get_password():
	return c.password

c = "dbname='"+get_dbname()+"' user='"+get_user()+"' host='"+get_host()+"' password='"+get_password()+"'"
print c