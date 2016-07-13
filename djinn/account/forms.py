from django import forms
from django.contrib.auth import get_user_model
from django.contrib import auth
from .models import ExtUser
from django.forms.widgets import PasswordInput


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), label='Email')
    password1 = forms.CharField(
        required=True,
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}), label='Пароль')
    password2 = forms.CharField(
        required=True,
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        label='Повторите пароль')

    class Meta:
        model = ExtUser
        fields = ['email', 'password1', 'password2']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), label='Email')
    password = forms.CharField(
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}), label='Пароль')

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = auth.authenticate(email=email,
                                     password=password)
            if user is None:
                raise forms.ValidationError('Неверный email или пароль.')
        return self.cleaned_data

    class Meta:
        fields = ['email', 'password']
