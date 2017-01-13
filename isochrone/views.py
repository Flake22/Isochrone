from django.shortcuts import render_to_response
import os

import isochrone_computation
import getter
import db_connection
import graphs_generator

def parse_query_results(res):

	#retrive population by age and sex
	m1 =int(round(res[3]))						#men 0-29
	m2 =int(round(res[4]))						#men 30-54
	m3 =int(round(res[5]))						#men >=55
	men = m1+m2+m3

	w1 =int(round(res[0]))-m1					#women 0-29
	w2 =int(round(res[1]))-m2					#women 30-54
	w3 =int(round(res[2]))-m3					#women >=55
	women = (w1+w2+w3)

	age_and_sex = [w1, w2, w3, m3, m2, m1, women, men]

	#retrive family composition
	family_composition=[int(round(res[6])),		#families with 1 component
						int(round(res[7])),		#families with 1 component
						int(round(res[8])),		#families with 1 component
						int(round(res[9])),		#families with 1 component
						int(round(res[10])),	#families with 1 component
						int(round(res[11]))]	#families with 1 component

	#retrive commuters
	commuters=[int(round(res[12])),				#within residence town
						int(round(res[13]))]		#outside residence town

	return age_and_sex, family_composition, commuters

def print_to_file(rel_path, html):
	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	abs_file_path = os.path.join(script_dir, rel_path)
	with open(abs_file_path, 'w+') as f:
		f.write(html)

def escape_html(html):
	return "{% autoescape off %}{{" + myhtml + "}}{% endautoescape %}"


# Check if GET parameters have valid values
def checkGetParams(latitude, longitude, duration, travelMode, angles, tolerance):
	
	validParams = True
	if latitude == None or latitude == "":
		validParams = False
	elif longitude == None or longitude == "":
		validParams = False
	elif duration == None or duration == "":
		validParams = False
	elif travelMode == None or travelMode == "":
		validParams = False
	elif angles == None or travelMode == "":
		validParams = False
	elif tolerance == None or tolerance == "":
		validParams = False

	return validParams


def index(request):
	key = getter.get_key()
	map_file = 'map.html'
	menu_file = 'menu.html'
	exception_report = None
	if request.method == "GET":
		try:
			#checks whether isochrone has been requested
			latitude = request.GET.get("latitude", None)
			longitude = request.GET.get("longitude", None)
			duration = request.GET.get("duration", None)
			travelMode = request.GET.get("travelMode", None)
			angles = request.GET.get("angles", None)
			tolerance = request.GET.get("tolerance", None)

			# Check GET parameters
			if checkGetParams(latitude, longitude, duration, travelMode, angles, tolerance):

				#get isochrone and its html versrion
				iso, map_html = isochrone_computation.compute_isochrone(latitude, longitude, duration, travelMode, angles, tolerance)
				
				#open connection with pgadming ad run query
				try:
					#connect to the db
				 	conn = db_connection.connect()
				 	records = db_connection.executeQuery(iso, conn)

				 	age_and_sex, family_composition, commuters = parse_query_results(records)

				 	#close connection
				 	conn.close()
				except Exception as eDB:
				 	print eDB
				
				graphs_html = graphs_generator.generate_graphs(age_and_sex, family_composition, commuters)

				#print html to file	
				try:
					print_to_file("templates/iso_map.html", map_html)
					
					print_to_file("templates/graphs.html", graphs_html)
					
					map_file = 'iso_map.html'
					menu_file = 'graphs.html'
				except Exception as eG:
					print eG

		except Exception as e:
			print e
			exception_report = e


	return render_to_response('isochrone/index.html', {'key' : key, 'map': map_file, 'main': "main.html", 'menu': menu_file, 'modal': "messageModal.html", 'exception': exception_report})