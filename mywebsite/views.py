from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from mywebsite.forms import SignUpForm
from mywebsite.forms import editform
from django.contrib.auth.models import User
from mywebsite.models import Profile


@login_required
def home(request):
    return render(request, 'home.html')


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
    return render(request,'prof_detail.html', {'prof':prof})


def updatedetails(request,whoami):
    user=User.objects.filter(username=whoami)[0]
    prof=Profile.objects.filter(user=user)[0]
    if request.method == 'POST':
        form = editform(request.POST)
        if form.is_valid():


            prof.designation = form.cleaned_data.get('designation')
            prof.education = form.cleaned_data.get('education')
            prof.research_interest = form.cleaned_data.get('research_interest')
            prof.publications = form.cleaned_data.get('publications')
            prof.save()
            return redirect( 'mywebsite:detail' , person = prof )

    else:
        form = editform()
    return render(request, 'editform.html' , {'form': form})
