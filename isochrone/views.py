from django.shortcuts import render_to_response
from django.http import HttpResponse
import isochrone_computation
import key_getter

def index(request):
	key = key_getter.get_key()
	if request.method == "GET":
		try:
			latitude = request.GET["latitude"]
			longitude = request.GET["longitude"]
			duration = request.GET["duration"]
			travelMode = request.GET["travelMode"]
			angles = request.GET["angles"]
			tolerance = request.GET["tolerance"]

			iso, htmltext = isochrone_computation.compute_isochrone(latitude, longitude, duration, travelMode, angles, tolerance)
			#call postgress

			print htmltext
			print iso

			return HttpResponse("Hello world")
			#return render_to_response('isochrone/index.html', {'key' : key, 'map': "map.html", 'main': "main.html"})
		except Exception:
			pass
	return render_to_response('isochrone/index.html', {'key' : key, 'map': "map.html", 'main': "main.html", 'menu': "menu.html"})