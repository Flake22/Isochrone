import os

import google_maps as api

def get_access_type():
	return api.access_type

def get_key(): 
	#get access type
	access_type=get_access_type()

	#get Google Maps configuration settings
	if access_type == 'personal':
		return api.api_number
	if access_type == 'business':
		return api.client_id

def get_dbname ():
	return api.dbname 

def get_user():
	return api.user

def get_host():
	return api.host

def get_password():
	return api.password

c = "dbname='"+get_password()+"' user='"+get_user()+"' host='"+get_host()+"' passord='"+get_password()+"'"
print c