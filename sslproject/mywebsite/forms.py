from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from mywebsite.models import *

class SignUpForm(UserCreationForm):
    webmail = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'webmail', 'password1', 'password2', )
