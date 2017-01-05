import os

import config

def get_access_type():
	return config.access_type

def get_key(): 
	#get access type
	access_type=get_access_type()

	#get Google Maps configuration settings
	if access_type == 'personal':
		return config.api_number
	if access_type == 'business':
		return config.client_id

def get_dbname ():
	return config.dbname 

def get_user():
	return config.user

def get_host():
	return config.host

def get_password():
	return config.password

c = "dbname='"+get_dbname()+"' user='"+get_user()+"' host='"+get_host()+"' password='"+get_password()+"'"