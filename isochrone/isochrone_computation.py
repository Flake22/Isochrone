from __future__ import division
from math import cos, sin, tan, sqrt, pi, radians, degrees, asin, atan2
import time
import datetime
import urlparse
import unicodedata
import urllib
import urllib2
import simplejson
import hmac
import base64
import unicodedata
import hashlib

import key_getter as key

def settings_sanity_check(latitude, longitude, dist, mode, angles, tolerance):
	try:
		# selected poin must have a float latitude and longitude
		if not (isinstance(latitude, float) & isinstance(longitude, float)):
			raise Exception('origin point must have a float latitude and longitude')

		#distance must be an int(minutes)
		if not isinstance(dist, int):
			raise Exception('distance must be an int')

		# travel_mode must be either 'driving' or 'walking'
		if mode not in ['driving', 'walking']:
			raise Exception("access_type must be either 'driving' or 'walking'.")

		#number_of_angles must be an integer
		if not isinstance(angles, int):
		   raise Exception('number_of_angles must be an int')

		#tolerance must be a float
		if not isinstance(tolerance, float):
		   raise Exception("tolerance must be a number")
	except Exception as e:
		print e

def select_destination(angle, radius, latitude, longitude):
	#sanity check
	if angle == '':
		raise Exception('angle cannot be blank.')
	if radius == '':
		raise Exception('radius cannot be blank.')

	#find the location on a sphere a distance 'radius' along a bearing 'angle' from origin
	#this uses haversines rather than simple Pythagorean distance in Euclidean space, being the Earth spherical
	r = 6378.388  # Radius of the Earth in chilometers
	bearing = radians(angle)  # Bearing in radians converted from angle in degrees
	lat1 = radians(latitude)
	lng1 = radians(longitude)
	lat2 = asin(sin(lat1) * cos(radius / r) + cos(lat1) * sin(radius / r) * cos(bearing))
	lng2 = lng1 + atan2(sin(bearing) * sin(radius / r) * cos(lat1), cos(radius / r) - sin(lat1) * sin(lat2))
	lat2 = degrees(lat2)
	lng2 = degrees(lng2)
	return [lat2, lng2]

def get_full_url(url):
	# Get the private_key used to sign the API request
	private_key = config.get('api', 'crypto_key')
	
	# We only need to sign the path+query part of the string
	url_to_sign = url.path + "?" + url.query
	
	# Decode the private key into its binary format
	decoded_key = base64.urlsafe_b64decode(private_key)
	
	# Create a signature using the private key and the URL-encoded
	#   string using HMAC SHA1. This signature will be binary.
	signature = hmac.new(decoded_key, url_to_sign, hashlib.sha1)
	
	# Encode the binary signature into base64 for use within a URL
	encoded_signature = base64.urlsafe_b64encode(signature.digest())
	original_url = url.scheme + '://' + url.netloc + url.path + '?' + url.query
	full_url = original_url + '&signature=' + encoded_signature

	return full_url

def build_url(destination, latitude, longitude, mode):
	origin = str(latitude)+','+str(longitude)

	#sanity check on destination field
	if destination == '':
		raise Exception('destination cannot be blank.')
	elif isinstance(destination, str):
		destination_str = destination.replace(' ', '+')
	elif isinstance(destination, list):
		destination_str = ''
		for element in destination:
			if isinstance(element, str):
				destination_str = '{0}|{1}'.format(destination_str, element.replace(' ', '+'))
			elif isinstance(element, list) and len(element) == 2:
				destination_str = '{0}|{1}'.format(destination_str, ','.join(map(str, element)))
			else:
				raise Exception('destination must be a list of lists [lat, lng] or a list of strings.')
		destination_str = destination_str.strip('|')
	else:
		raise Exception('destination must be a a list of lists [lat, lng] or a list of strings.')
	
	acc = key.get_key()

	#if using Google Maps for Business, the calculation will use current traffic conditions
	departure = datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1, 0, 0, 0)

	# Convert the URL string to a URL that can be parsed
	# The URL should already be URL-encoded
	full_url=''
	prefix = 'https://maps.googleapis.com/maps/api/distancematrix/json?mode='+mode+'&units=metric&avoid=tolls|highways|ferries|indoor'

	access_type=key.get_access_type()

	if access_type == 'personal':
		url = urlparse.urlparse('{0}&origins={1}&destinations={2}&key={3}'.format(prefix, origin, destination_str, acc))
		full_url = url.scheme + '://' + url.netloc + url.path + '?' + url.query

	if access_type == 'business':
		url = urlparse.urlparse('{0}&origins={1}&destinations={2}&departure_time={3}&client={4}'.format(prefix,
																										origin,
																										destination_str,
																										int(departure.total_seconds()),
																										acc))
		full_url = get_full_url(url)
	
	return full_url

def normalize(url):
    # turn string into unicode
    if not isinstance(url,unicode):
        url = url.decode('utf8')

    # parse it
    parsed = urlparse.urlsplit(url)

    # divide the netloc further
    userpass,at,hostport = parsed.netloc.rpartition('@')
    user,colon1,pass_ = userpass.partition(':')
    host,colon2,port = hostport.partition(':')

    # encode each component
    scheme = parsed.scheme.encode('utf8')
    user = urllib.quote(user.encode('utf8'))
    colon1 = colon1.encode('utf8')
    pass_ = urllib.quote(pass_.encode('utf8'))
    at = at.encode('utf8')
    host = host.encode('idna')
    colon2 = colon2.encode('utf8')
    port = port.encode('utf8')
    path = '/'.join(  # could be encoded slashes!
        urllib.quote(urllib.unquote(pce).encode('utf8'),'')
        for pce in parsed.path.split('/')
    )
    query = urllib.quote(urllib.unquote(parsed.query).encode('utf8'),'=&?/')
    fragment = urllib.quote(urllib.unquote(parsed.fragment).encode('utf8'))

    # put it back together
    netloc = ''.join((user,colon1,pass_,at,host,colon2,port))
    return urlparse.urlunsplit((scheme,netloc,path,query,fragment))


def run_request(url):
	#send query to Google Maps to get the requested answer
	url = normalize(url)

	req = urllib2.Request(url)
	#print url
	opener = urllib2.build_opener()

	f = opener.open(req)
	d = simplejson.load(f)

	if not d['status'] == 'OK':
		raise Exception('Error. Google Maps API encoutered error: {}'.format(d['status']))

	return d

def parse_json(url=''):
	#Parse the json response from the API
	d = run_request(url)

	addresses = d['destination_addresses']

	i = 0
	durations = [0] * len(addresses)
	for row in d['rows'][0]['elements']:
		if not row['status'] == 'OK':
			raise Exception('Error. Google Maps API encountered error: {}'.format(row['status']))
			durations[i] = 9999
		else:
			if 'duration_in_traffic' in row:
				durations[i] = row['duration_in_traffic']['value'] / 60
			else:
				durations[i] = row['duration']['value'] / 60
		i += 1
	return [addresses, durations]

def geocode_address(address=''):
	# Convert origin to URL-compatible string
	if address == '':
		raise Exception('address cannot be blank.')
	elif isinstance(address, str) or isinstance(address, unicode):
		address_str = address.replace(' ', '+')
	else:
		raise Exception('address should be a string.')
   
	acc = key.get_key()

	#convert the URL string to a URL that can be parsed
	#the URL should already be URL-encoded
	prefix = 'https://maps.googleapis.com/maps/api/geocode/json'

	access_type = key.get_access_type()
	if access_type == 'personal':
		url = urlparse.urlparse('{0}?address={1}&key={2}'.format(prefix,
																 address_str,
																 acc))
		full_url = url.scheme + '://' + url.netloc + url.path + '?' + url.query
	if access_type == 'business':
		url = urlparse.urlparse('{0}?address={1}&client={2}'.format(prefix,
																	address_str,
																	acc))
		full_url= get_full_url(url)

	#request geocode from address
	d = run_request(full_url)
	
	geocode = [d['results'][0]['geometry']['location']['lat'],
			   d['results'][0]['geometry']['location']['lng']]
	return geocode

def get_bearing(destination, latitude, longitude):
	#sanity check
	if destination == '':
		raise Exception('destination cannot be blank')

	#calculate the bearing from origin to destination
	bearing = atan2(sin((destination[1] - longitude) * pi / 180) * cos(destination[0] * pi / 180),
					cos(latitude * pi / 180) * sin(destination[0] * pi / 180) -
					sin(latitude * pi / 180) * cos(destination[0] * pi / 180) * cos((destination[1] - longitude) * pi / 180))
	bearing = bearing * 180 / pi
	bearing = (bearing + 360) % 360
	return bearing

def sort_points(iso, latitude, longitude):
	#put the isochrone points in a proper order
	if iso == '':
		raise Exception('iso cannot be blank.')

	bearings = []
	for row in iso:
		bearings.append(get_bearing(row, latitude, longitude))

	points = zip(bearings, iso)
	sorted_points = sorted(points)
	sorted_iso = [point[1] for point in sorted_points]
	return sorted_iso

def get_isochrone(latitude, longitude, duration, mode, angles, tolerance):
	# Make a radius list, one element for each angle,
	#   whose elements will update until the isochrone is found
	if mode=='walking':
		c_min = 0.05
		c_max = 0.15
	if mode=='driving':
		c_min = 0.5
		c_max = 2

	rad1 = [duration * c_min] * angles  #This will give us a 3km/h or 30km/h speed for 'walking' and 'driving' respectively
	phi1 = [i * (360 / angles) for i in range(angles)]
	data0 = [0] * angles
	rad0 = [0] * angles
	rmin = [0] * angles
	rmax = [c_max * duration] * angles  #This will give us a 9km/h or 120km/h speed for 'walking' and 'driving' respectively
	iso = [[0, 0]] * angles

	# Counter to ensure we're not getting out of hand
	j = 0

	#Perform a binary search on radius along each bearing until the duration returned from
	#the API is within a tolerance of the isochrone duration.
	while sum([a - b for a, b in zip(rad0, rad1)]) != 0:
		rad2 = [0] * angles
		for i in range(angles):
			iso[i] = select_destination(phi1[i], rad1[i], latitude, longitude)
			time.sleep(0.1)
		url = build_url(iso, latitude, longitude, mode)
		data = parse_json(url)
		for i in range(angles):
			if (data[1][i] < (duration - tolerance)) & (data0[i] != data[0][i]):
				rad2[i] = (rmax[i] + rad1[i]) / 2
				rmin[i] = rad1[i]
			elif (data[1][i] > (duration + tolerance)) & (data0[i] != data[0][i]):
				rad2[i] = (rmin[i] + rad1[i]) / 2
				rmax[i] = rad1[i]
			else:
				rad2[i] = rad1[i]
			data0[i] = data[0][i]
		rad0 = rad1
		rad1 = rad2
		j += 1
		if j > 30:
			raise Exception("The operation took too much time.")

	for i in range(angles):
		iso[i] = geocode_address(data[0][i])
		time.sleep(0.1)

	iso = sort_points(iso, latitude, longitude)
	return iso

def generate_isochrone_map(iso, latitude, longitude):

	htmltext = """
	<script>
	function initMap() {{
	var mapOptions = {{
	zoom: 14,
	center: new google.maps.LatLng({0},{1})
	}};

	var map = new google.maps.Map(document.getElementById('map'), mapOptions);

	var marker = new google.maps.Marker({{
	position: new google.maps.LatLng({0},{1}),
	map: map
	}});

	var isochrone;

	var isochroneCoords = [
	""".format(latitude, longitude)

	for i in iso:
		htmltext += 'new google.maps.LatLng({},{}), \n'.format(i[0], i[1])

	htmltext += """
	];

	isochrone = new google.maps.Polygon({
	paths: isochroneCoords,
	strokeColor: '#000',
	strokeOpacity: 0.5,
	strokeWeight: 1,
	fillColor: '#000',
	fillOpacity: 0.25
	});

	isochrone.setMap(map);

	}

	google.maps.event.addDomListener(window, 'load', initMap);
	</script>
	"""
	#print htmltext
	return htmltext

def compute_isochrone(latitude, longitude, duration, mode, angles, tolerance):
	#check whether input settings are valid
	try:
		latitude = float(latitude)
		longitude = float(longitude)
		duration = int(duration)
		angles = int(angles)
		tolerance = float(tolerance)
	except Exception as e:
		raise

	settings_sanity_check(latitude, longitude, duration, mode, angles, tolerance)

	#compute isochrone
	iso = get_isochrone(latitude, longitude, duration, mode, angles, tolerance)
	htmltext = generate_isochrone_map(iso, latitude, longitude)
	return iso, htmltext
