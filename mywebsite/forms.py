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
        fields = ('username','first_name','second_name', 'webmail', 'password1', 'password2')

class editform(ModelForm):
    class Meta:
        model=Profile
        fields = ('designation','first_name','second_name', 'webmail','phone_number','fax_number', 'department','bio')

class studentform(ModelForm):
    class Meta:
        model=Students
        fields = ('name','details')
        fields = ('name','details','pic','url')

class publicationform(ModelForm):
    class Meta:
        model=Publica
        fields=('publication_title','collaborator','collaborator_email')

class researchform(ModelForm):
    class Meta:
        model=Research
        fields=('research_interest_title','research_interest_description')


class addCourse(ModelForm):
    class Meta:
        model=Courses
        fields=('courseName', 'startDate' , 'endDate' , 'current' )


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
