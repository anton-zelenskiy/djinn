from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model


User = get_user_model()


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.initial['city'] = '1'
        self.fields['city'].empty_label = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birth_date', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'фамилия'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'city': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'first_name': "Имя",
            'last_name': "Фамилия",
            'city': "Город",
            'birth_date': "Дата рождения",
        }


class PhoneForm(ModelForm):
    class Meta:
        model = User
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control',
                                            'pattern': '+7 ([0-9]{3}) [0-9]{3}-[0-9]{2}-[0-9]{2}',
                                            'placeholder': '+7 (999) 999-9999'})
        }
        labels = {'phone': "Телефон"}


class SkypeForm(ModelForm):
    class Meta:
        model = User
        fields = ['skype']
        widgets = {
            'skype': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {'skype': "Skype"}


class EmailForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {'email': "Email адрес"}
