from django import forms
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.template.context_processors import csrf

from .forms import UserProfileForm, PhoneForm, SkypeForm, EmailForm
from django.contrib.auth.decorators import login_required


User = get_user_model()


@login_required(login_url='/auth/login/')
def settings_view(request):
    args = {}

    user = User.objects.get(id=request.user.id)

    args['phone_form'] = PhoneForm()
    args['skype_form'] = SkypeForm()
    args['email_form'] = EmailForm()

    args['form'] = UserProfileForm(initial={
        'first_name': user.first_name, 'last_name': user.last_name,
        'birth_date': user.birth_date, 'city': user.city
        })
    args['phone'] = user.phone
    args['skype'] = user.skype
    args['email'] = user.email

    args.update(csrf(request))

    if request.POST:
        form = UserProfileForm(request.POST)
        if form.is_valid():
            data = {'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'birth_date': form.cleaned_data['birth_date'],
                    'city': form.cleaned_data['city']
                    }
            User.objects.filter(id=request.user.id).update(**data)
            return redirect('/')
        else:
            args['form'] = UserProfileForm()
            return render(request, 'settings.html', args)
    return render(request, 'settings.html', args)


def phone_update(request):
    args = {}
    if request.POST:
        phone = request.POST.get('phone', '')
        user = User.objects.get(id=request.user.id)
        if user.phone == phone:
            args['error'] = 'Данный номер сейчас используется в вашей анкете. Введите другой номер.'
            args['status'] = 0
            return JsonResponse(args)
        else:
            args['status'] = 1
            data = {'phone': phone}
            User.objects.filter(id=request.user.id).update(**data)
    return JsonResponse(args)


def skype_update(request):
    args = {}
    if request.POST:
        skype = request.POST.get('skype', '')
        user = User.objects.get(id=request.user.id)
        if user.skype == skype:
            args['error'] = 'Данный аккаун сейчас используется в вашей анкете. Введите другой аккаунт.'
            args['status'] = 0
            return JsonResponse(args)
        else:
            args['status'] = 1
            data = {'skype': skype}
            User.objects.filter(id=request.user.id).update(**data)
    return JsonResponse(args)


def email_update(request):
    args = {}
    if request.POST:
        try:
            email = request.POST.get('email', '')
            validate_email(email)
            user = User.objects.get(id=request.user.id)
            if user.email == email:
                args['error'] = 'Данный email сейчас используется в вашей анкете. Введите другой email.'
                args['status'] = 0
                return JsonResponse(args)
            else:
                args['status'] = 1
                data = {'email': email}
                User.objects.filter(id=request.user.id).update(**data)
        except forms.ValidationError:
            args['error'] = 'Неверный адрес электронной почты.'
            args['status'] = 0
            return JsonResponse(args)
    return JsonResponse(args)
