import psycopg2
import pyproj

def convert_points_to_UTM32N(iso):
	# Define coordinates stadards
	wgs84=pyproj.Proj("+init=EPSG:4326") # LatLon with WGS84 datum used by GPS units and Google Earth
	UTM32N=pyproj.Proj("+init=EPSG:32632") # LatLon used by the database

	s = ''
	count =0
	y_first =0
	x_first =0
	# Current coordinates that need to be converted (Trento)
	# Remember to reverse the logic of lat-long in x-y cartesian system (lat becomes y and long becomes x)
	for points in iso:
		y_curr = points[0]
		x_curr = points[1]

		


		# Conversion of the coordinates from wgs84 to UTM32N reference
		x_tar, y_tar = pyproj.transform(wgs84, UTM32N, x_curr, y_curr)

		if count==0:
			x_first=x_tar
			y_first=y_tar
		count=count+1
		s = ''.join([s, str(x_tar), ' ', str(y_tar), ','])
	s = ''.join([s, str(x_first), ' ', str(y_first), ','])
	return s[:len(s)-1]

def create_query(iso):
	#convert WGS84 coordinates into UTM32N
	polygon = convert_points_to_UTM32N(iso)
	print polygon
	query = "\n".join(["SELECT ",
						"SUM(ST_Area(ST_GeomFromText('POLYGON(("+polygon+"))')))/SUM(ST_Area(geom)),",
						"SUM(p.p14)+SUM(p.p15)+SUM(p.p16)+SUM(p.p17)+SUM(p.p18)+SUM(p.p19)+SUM(s.st3),",
						"SUM(p.p20)+SUM(p.p21)+SUM(p.p22)+SUM(p.p23)+SUM(p.p24)+SUM(s.st4),",
						"SUM(p.p25)+SUM(p.p26)+SUM(p.p27)+SUM(p.p28)+SUM(p.p29)+SUM(s.st5),",
						"SUM(p.p30)+SUM(p.p31)+SUM(p.p32)+SUM(p.p33)+SUM(p.p34)+SUM(p.p35)+SUM(s.st6),",
						"SUM(p.p36)+SUM(p.p37)+SUM(p.p38)+SUM(p.p39)+SUM(p.p40)+SUM(s.st7),",
						"SUM(p.p41)+SUM(p.p42)+SUM(p.p43)+SUM(p.p44)+SUM(p.p45)+SUM(s.st8),",
						"SUM(f.pf3),",
						"SUM(f.pf4),",
						"SUM(f.pf5),",
						"SUM(f.pf6),",
						"SUM(f.pf7),",
						"SUM(f.pf8),",
						"SUM(p.p137),",
						"SUM(p.p138)",
						"FROM spatial_ref NATURAL JOIN ",
						"famiglie AS f NATURAL JOIN ",
						"popolazione_residente AS p NATURAL JOIN ",
						"stranieri_residenti AS s WHERE ST_Intersects(geom, ST_GeomFromText('POLYGON(("+polygon+"))'))"])
	print "Query"
	return query

def connect():
	connection = psycopg2.connect("dbname='sezioni2011_nazionale' user='postgres' host='localhost' password='toor'")
	return connection

def executeQuery(iso, connection):
	query = create_query(iso)
	cursor = connection.cursor()
	cursor.execute(query)
	records = cursor.fetchall()
	return records[0]

def disconnect(connection):
	connection.close()