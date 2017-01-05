# isocronut

For a location selected through a GUI, calculate an [isochrone (same time) contour](http://en.wikipedia.org/wiki/Isochrone_map) around it. For the computed isochrone retrive information regarding the population that lives there: age and sex of the population, family composition and the daily movemetns of those who live there.

### Use

In order to run this implementation, put this repository in a folder. From the terminal, cd to that folder and type

```python
python manage.py runserver
```

Then go to browser, and point it to [127.0.0.1:8000/isochone](127.0.0.1:8000/isochone). Click away on the map.

### Parameters

__origin__ : Google Maps parseable origination address, selected through the interface

__duration__ : Number of minutes (scalar) for the isochrone contour, selected through the interface

__number_of_vertexes__ : Number of points defining the isochrone (int), selected through the interface

__tolerance__ : Number of minutes (scalar) that a test point can be away from __duration__ to be considered acceptable, selected through the interface

__access_type__ : Either 'personal' or 'business' (str), specifying if you are using a personal or business API access for Google Maps.

  * If 'personal', you won't have access to traffic conditions. The format of the 'config.py' config file must be:

```
api_number=<your api number>
```

  * If 'business', you will be able to use current traffic conditions, which will tighten your contour distance. The format of the 'config.py' config file must be:

```
client_id=<your client id>
crypto_key=<your crypto key>
```

__credentials_for_database__ : list of credentials for accessing the database. The format of the 'config.py' config file must be:

```
dbname =<your db name>
user=<your username>
host=<your host name>
password=<your password>
```

### Returns

Isochrone and information on the population that lives within the isochrone

### Dependencies

This module makes use of the following Python modules that you must have installed.

* django
* \__future\__
* psycopg2
* pyproj
* math
* time
* datetime
* urlparse
* urllib
* urllib2
* simplejson
* hmac
* base64
* unicodedata
* hashlib
* os
* sys
