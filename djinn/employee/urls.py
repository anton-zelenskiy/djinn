from django.conf.urls import url
from employee.views import employee_info, employee_view

urlpatterns = [
    url(r'^list/$', employee_view, name='employee'),
    url(r'^get/(?P<uid>\d+)/$', employee_info, name='get_employee'),
]
