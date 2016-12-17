from django.shortcuts import render_to_response
from django.http import HttpResponse
import os

import isochrone_computation
import key_getter
import db_connection

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

			print "HELLO\n\n\n"

			#get isochrone and its html versrion
			iso, htmltext = isochrone_computation.compute_isochrone(latitude, longitude, duration, travelMode, angles, tolerance)

			print iso
			
			#open connection with pgadming ad run query
			# try:
			# 	conn = db_connection.connect()
			# 	records = db_connection.executeQuery(iso, connection)

			# 	#do something with records

			# 	#close connection
			# 	conn.close()
			# except Exception as e:
			# 	raise

			# print htmltext
			# print iso

			# try:
			# 	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
			# 	rel_path = "templates/iso_map.html"
			# 	abs_file_path = os.path.join(script_dir, rel_path)
			# 	with open(abs_file_path, 'w+') as f:
			# 		f.write(htmltext)
			# except Exception as e:
			# 	print e


			#return HttpResponse("Hello world")
			return render_to_response('isochrone/index.html', {'key' : key, 'map': "iso_map.html", 'main': "main.html", 'menu': "menu.html"})
		except Exception:
			pass
	return render_to_response('isochrone/index.html', {'key' : key, 'map': "map.html", 'main': "main.html", 'menu': "menu.html"})