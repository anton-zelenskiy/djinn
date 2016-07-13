from django.conf.urls import url
from .views import choose_city

urlpatterns = [
    url(r'^choose_city/(?P<pk>\d+)$', choose_city, name='choose_city'),
]
