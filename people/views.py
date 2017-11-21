from django.shortcuts import render
import mimetypes

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.encoding import smart_str
from mywebsite.forms import *
from mywebsite.forms import publicationform
from django.conf import settings
from wsgiref.util import FileWrapper
from django.contrib.auth.models import User
from mywebsite.models import *


# Create your views here.
def home_people(request,person):
    user=User.objects.filter(username=person)[0]
    prof=Profile.objects.filter(user=user)[0]
    return render(request,'base_p.html', {'prof':prof})

def home_publications(request,person):
        user=User.objects.filter(username=person)[0]
        prof=Profile.objects.filter(user=user)[0]
        return render(request , 'publications.html', {'prof':prof})

def home_students(request,person):
        user=User.objects.filter(username=person)[0]
        prof=Profile.objects.filter(user=user)[0]
        return render(request , 'students.html', {'prof':prof})

def home_courses(request,person):
    user=User.objects.filter(username=person)[0]
    prof=Profile.objects.filter(user=user)[0]
    return render(request , 'courses1.html', {'prof':prof})

def home_research(request,person):
    user=User.objects.filter(username=person)[0]
    prof=Profile.objects.filter(user=user)[0]
    return render(request, 'research.html', {'prof':prof})
