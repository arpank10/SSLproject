from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from mywebsite.models import *
from django.forms import ModelForm
class SignUpForm(UserCreationForm):
    webmail = forms.EmailField()
    first_name=forms.CharField(max_length=500)
    second_name=forms.CharField(max_length=500)

    class Meta:
        model = User
        fields = ('username','first_name','second_name', 'webmail', 'password1', 'password2', )


class editform(ModelForm):
    class Meta:
        model = Profile
        fields = ('designation','education','research_interest','publications')

class studentform(ModelForm):
    class Meta:
        model=Students
        fields = ('name','details')
