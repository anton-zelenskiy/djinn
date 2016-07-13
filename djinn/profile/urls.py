from django.conf.urls import url
from .views import settings_view, phone_update, skype_update, email_update

urlpatterns = [
    url(r'^settings/$', settings_view, name='profile'),
    url(r'^phone_update/$', phone_update, name='phone_update'),
    url(r'^skype_update/$', skype_update, name='skype_update'),
    url(r'^email_update/$', email_update, name='email_update')
]
