# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from city.models import City


def choose_city(request, pk):
    city = City.objects.get(pk=pk)
    response = HttpResponseRedirect('/')
    response.set_cookie('city', city.id)
    return response
