import psycopg2
import pyproj
import key_getter

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
	query = "\n".join(["WITH abraham_simpson AS (",
						"SELECT sez2011, (ST_Area(ST_Intersection(ST_MakeValid(ST_GeomFromText('POLYGON(("+polygon+"))')), geom))/ST_Area(geom)) AS prop",
						"FROM spatial_ref WHERE ST_Intersects(geom, ST_MakeValid(ST_GeomFromText('POLYGON(("+polygon+"))'))))",
						"SELECT",
						"SUM((p.p14+p.p15+p.p16+p.p17+p.p18+p.p19+s.st3)*prop),",
						"SUM((p.p20+p.p21+p.p22+p.p23+p.p24+s.st4)*prop),",
						"SUM((p.p25+p.p26+p.p27+p.p28+p.p29+s.st5)*prop),",
						"SUM((p.p30+p.p31+p.p32+p.p33+p.p34+p.p35+s.st6)*prop),",
						"SUM((p.p36+p.p37+p.p38+p.p39+p.p40+s.st7)*prop),",
						"SUM((p.p41+p.p42+p.p43+p.p44+p.p45+s.st8)*prop),",
						"SUM((f.pf3)*prop),",
						"SUM((f.pf4)*prop),",
						"SUM((f.pf5)*prop),",
						"SUM((f.pf6)*prop),",
						"SUM((f.pf7)*prop),",
						"SUM((f.pf8)*prop),",
						"SUM((p.p137)*prop),",
						"SUM((p.p138)*prop)",
						"FROM abraham_simpson NATURAL JOIN ",
						"famiglie AS f NATURAL JOIN ",
						"popolazione_residente AS p NATURAL JOIN ",
						"stranieri_residenti AS s"])
	print "Query"
	print query
	return query

def connect():
	c = "dbname='"+key_getter.get_dbname()+"' user='"+key_getter.get_user()+"' host='"+key_getter.get_host()+"' password='"+key_getter.get_password()+"'"
	connection = psycopg2.connect(c)
	#connection = psycopg2.connect("dbname='sezioni2011_nazionale' user='postgres' host='localhost' password='toor'")
	return connection

def executeQuery(iso, connection):
	query = create_query(iso)
	cursor = connection.cursor()
	cursor.execute(query)
	records = cursor.fetchall()
	return records[0]

def disconnect(connection):
	connection.close()