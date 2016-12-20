# from django.conf.urls import url
# from isochrone.views import index

# urlpatterns = [
#     url(r'isochrone/$', index),
# ]


from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from AppIsochrone import settings
from isochrone.views import index

admin.autodiscover()

urlpatterns = [
	url(r'isochrone/$', index)
]

urlpatterns += staticfiles_urlpatterns()