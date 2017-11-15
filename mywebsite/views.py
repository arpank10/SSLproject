from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from mywebsite.forms import *
from mywebsite.forms import publicationform
from django.contrib.auth.models import User
from mywebsite.models import Profile


@login_required
def home(request):
    user= request.user
    prof=Profile.objects.filter(user=user)[0]
    return render(request,'prof_detail.html', {'prof':prof})

def index(request):
    all_users=Profile.objects.all()
    return render(request, 'all_users.html' , {'all_users':all_users} )

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            person=Profile.objects.filter(user=user)[0]

            user.save()
            raw_password = form.cleaned_data.get('password1')
            person.webmail=form.cleaned_data.get('webmail')
            person.first_name=form.cleaned_data.get('first_name')
            person.second_name=form.cleaned_data.get('second_name')
            #user.profile.webmail = form.cleaned_data.get('webmail')
            person.save()
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('mywebsite:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def showdetail(request, person):
    user=User.objects.filter(username=person)[0]
    prof=Profile.objects.filter(user=user)[0]
    if request.method== 'POST':
        if 'addPublication' in request.POST:
            form = publicationform(request.POST)
            if form.is_valid():
                public = form.save(commit=False)
                public.profile = prof
                public.publication_title = form.cleaned_data.get('publication_title')
                public.collaborator = form.cleaned_data.get('collaborator')
                public.collaborator= form.cleaned_data.get('collaborator_email')
                public.save()
                return redirect ( 'mywebsite:detail' , person=prof )
        elif 'addStudent' in request.POST:
            form1 = studentform(request.POST)
            if form1.is_valid():
                stud = form1.save(commit=False)
                stud.supervisor = prof
                stud.name = form1.cleaned_data.get('name')
                stud.details = form1.cleaned_data.get('details')
                stud.save()
                return redirect ( 'mywebsite:detail' , person=prof )
    else:
        form=publicationform()
        form1=studentform()
    return render( request, 'prof_detail.html' , { 'form':form, 'prof':prof , 'form1':form1 })

def updatedetails(request,whoami):
    prof=Profile.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        form = editform(request.POST,instance=prof)
        if form.is_valid():
            prof.designation = form.cleaned_data.get('designation')
            prof.webmail=form.cleaned_data.get('webmail')
            prof.first_name=form.cleaned_data.get('first_name')
            prof.second_name=form.cleaned_data.get('second_name')
            prof.phone_number = form.cleaned_data.get('phone_number')
            prof.fax_number = form.cleaned_data.get('fax_number')
            prof.department = form.cleaned_data.get('department')
            prof.save()
            return redirect( 'mywebsite:detail' , person = prof )

    else:
        form = editform(instance=prof)
    return render(request, 'edit_details.html' , {'form': form})
