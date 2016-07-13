from django.http import JsonResponse
from django.shortcuts import render_to_response, render
from django.template.context_processors import csrf
from django.template.defaulttags import register
from .models import Employee
from category.models import Category, Subcategory
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import get_user_model


User = get_user_model()


@ensure_csrf_cookie
def employee_view(request):
    args = {'categories': Category.objects.all(), 'subcategory': Subcategory.objects.all()}

    response = {}
    if request.POST:
        users = None
        status = request.POST.get('status')  # load all employee list on load {% url 'employee' %} page
        if status == 'all':
            users = Employee.objects.all()
        else:
            if 'cat_id' not in request.POST:
                sub_id = request.POST.get('sub_id')
                current_sub = Subcategory.objects.get(id=sub_id)
                response['url'] = current_sub.subcategory
                users = Employee.objects.filter(subcategory=sub_id)
            if 'sub_id' not in request.POST:
                cat_id = request.POST.get('cat_id')
                current_cat = Category.objects.get(id=cat_id)
                response['url'] = current_cat.category
                users = Employee.objects.filter(category=cat_id)

        employee_list = []
        for i in users:
            user_profile = User.objects.get(id=i.user_id)
            employee_data = {"description": i.description,
                             'first_name': user_profile.first_name,
                             'last_name': user_profile.last_name,
                             'age': user_profile.get_age_and_postfix,
                             'id': i.id,
                             }
            employee_list.append(employee_data)
        response['users'] = employee_list

        return JsonResponse(response)

    return render(request, 'employee.html', args)


def employee_info(request, uid=1):
    args = {}
    employee_data = Employee.objects.get(id=uid)
    args['employee_data'] = employee_data
    args['user_profile_data'] = User.objects.get(id=employee_data.user_id)

    return render(request, 'employee_info.html', args)


# filter: get all employee subcategories for employee category
@register.filter
def in_category(item, category):
    return item.filter(category=category)
