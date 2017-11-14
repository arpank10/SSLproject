from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from mywebsite.forms import SignUpForm
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
            #user.profile.webmail = form.cleaned_data.get('webmail')
            person.save()
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('mywebsite:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
