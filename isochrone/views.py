from django.shortcuts import render_to_response
from django.http import HttpResponse
import os

import isochrone_computation
import key_getter
import db_connection

def parse_query_results(res):
	#get data for computations
	percentage = float(res[0])

	#retrive population by age and sex
	m1 =int(round(res[4]*percentage))						#men 0-29
	m2 =int(round(res[5]*percentage))						#men 30-54
	m3 =int(round(res[6]*percentage))						#men >=55
	men = m1+m2+m3

	w1 =int(round(res[1]*percentage))-m1					#women 0-29
	w2 =int(round(res[2]*percentage))-m2					#women 30-54
	w3 =int(round(res[3]*percentage))-m3					#women >=55
	women = (w1+w2+w3)

	age_and_sex = [m1, m2, m2, w1, w2, w3, women, men]

	#retrive family composition
	family_composition=[int(round(res[7]*percentage)),		#families with 1 component
						int(round(res[8]*percentage)),		#families with 1 component
						int(round(res[9]*percentage)),		#families with 1 component
						int(round(res[10]*percentage)),		#families with 1 component
						int(round(res[11]*percentage)),		#families with 1 component
						int(round(res[12]*percentage))]		#families with 1 component

	#retrive commuters
	commuters=[int(round(res[13]*percentage)),				#within residence town
						int(round(res[14]*percentage))]		#outside residence town

	print age_and_sex, family_composition, commuters

def index(request):
	key = key_getter.get_key()
	if request.method == "GET":
		try:
			#checks whether isochrone has been requested
			latitude = request.GET["latitude"]
			longitude = request.GET["longitude"]
			duration = request.GET["duration"]
			travelMode = request.GET["travelMode"]
			angles = request.GET["angles"]
			tolerance = request.GET["tolerance"]

			#get isochrone and its html versrion
			iso, htmltext = isochrone_computation.compute_isochrone(latitude, longitude, duration, travelMode, angles, tolerance)

			#print htmltext to file	
			try:
				script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
				rel_path = "templates/iso_map.html"
				abs_file_path = os.path.join(script_dir, rel_path)
				with open(abs_file_path, 'w+') as f:
					f.write(htmltext)
			except Exception as e:
				print e
				#return HttpResponse("Hello world")
			
			#open connection with pgadming ad run query
			# try:
			#	#connect to the db
			# 	conn = db_connection.connect()
			# 	records = db_connection.executeQuery(iso, conn)

			# 	age_and_sex, family_composition, commuters = parse_query_results(records)

			# 	#close connection
			# 	conn.close()
			# except Exception as e:
			# 	raise

			#return HttpResponse("Hello world")
			return render_to_response('isochrone/index.html', {'key' : key, 'map': "iso_map.html", 'main': "main.html", 'menu': "menu.html"})
		except Exception:
			pass
	return render_to_response('isochrone/index.html', {'key' : key, 'map': "map.html", 'main': "main.html", 'menu': "menu.html"})