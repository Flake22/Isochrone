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