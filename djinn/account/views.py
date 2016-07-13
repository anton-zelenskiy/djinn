from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from django.contrib import auth
from .forms import LoginForm, UserCreationForm


def login(request):
    args = {}
    args.update(csrf(request))
    args['form'] = LoginForm()
    if request.POST:
        auth_form = LoginForm(request.POST)
        if auth_form.is_valid():
            auth_user = auth.authenticate(email=auth_form.cleaned_data['email'],
                                          password=auth_form.cleaned_data['password'])
            if auth_user is not None:
                if auth_user.is_active:
                    auth.login(request, auth_user)
                    return redirect('/')
                else:
                    args['form'] = auth_form
                    return render_to_response('login.html', args)
            else:
                args['form'] = auth_form
                return render_to_response('login.html', args)
        else:
            args['form'] = auth_form

    return render_to_response('login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(email=newuser_form.cleaned_data['email'],
                                        password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html', args)
