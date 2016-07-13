from city.models import City
from django.contrib import auth


def city_processor(request):
    args = {'username': auth.get_user(request),
            'cities': City.objects.all()}
    if 'city' in request.COOKIES.keys():
        city_id = request.COOKIES.get('city', '')
        args['city'] = City.objects.get(id=city_id).city
    return args
