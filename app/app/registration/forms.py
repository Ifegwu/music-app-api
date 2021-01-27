from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm 
from django import forms
from django.contrib.auth.models import User

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'your class',
        'placeholder': 'your placeholder',
        'type': 'email',
        'name': 'email'
    }))

    class Meta:
         model = User
         fields = ['email']

class UserPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetConfirmForm, self).__init__(*args, **kwargs)

    password1 = forms.EmailField(label='', widget=forms.PasswordInput(attrs={
        'class': 'your class',
        'placeholder': 'Password',
        'type': 'password',
        'name': 'password1'
    }))

    password2 = forms.EmailField(label='', widget=forms.PasswordInput(attrs={
        'class': 'your class',
        'placeholder': 'Password',
        'type': 'password',
        'name': 'password2'
    }))

    class Meta:
         model = User
         fields = ['password']