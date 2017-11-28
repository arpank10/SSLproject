from django.shortcuts import render
import mimetypes
import requests
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.encoding import smart_str

from mywebsite.forms import *
from mywebsite.forms import publicationform
from mywebsite.forms import researchform
from django.conf import settings
from wsgiref.util import FileWrapper
from django.contrib.auth.models import User
from mywebsite.models import *




@login_required
def home(request):
    user= request.user
    prof=Profile.objects.filter(user=user)[0]
    return render(request,'prof_detail.html', {'prof':prof})

def index(request):
    all_users=Profile.objects.all()
    return render(request, 'all_users.html' , {'all_users':all_users} )

def courses(request,person):
    user=User.objects.filter(username=person)[0]
    prof=Profile.objects.filter(user=user)[0]
    if request.method== 'POST':
        form = addCourse(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.prof = prof
            course.courseName = form.cleaned_data.get('courseName')
            course.startDate = form.cleaned_data.get('startDate')
            course.endDate = form.cleaned_data.get('endDate')
            course.current= form.cleaned_data.get('current')
            course.save()
            return redirect ( 'mywebsite:courses' , person=prof )
    else:
        form = addCourse()
    return render(request, 'courses.html' , {'prof': prof , 'form': form})


def courses_upload(request,course):
    course=Courses.objects.filter(courseName=course)[0]
    prof=course.prof
    if request.method== 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.course_name=course
            doc.save()
            return redirect ( 'mywebsite:courses_upload' , course=course )
    else:
        form = DocumentForm()
    return render(request, 'course_upload.html' , { 'prof':prof , 'courses': course , 'form': form })

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
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''

            if result['success']:
                form.save()
                messages.success(request, 'New comment added with success!')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
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
        elif 'addResearch' in request.POST:
            form2 = researchform(request.POST)
            if form2.is_valid():
                public = form2.save(commit=False)
                public.profile = prof
                public.research_interest_title = form2.cleaned_data.get('research_interest_title')
                public.research_interest_description= form2.cleaned_data.get('research_interest_description')
                public.save()
                return redirect ( 'mywebsite:detail' , person=prof )
        elif 'addStudent' in request.POST:
            form1 = studentform(request.POST)
            if form1.is_valid():
                stud = form1.save(commit=False)
                stud.supervisor = prof
                stud.name = form1.cleaned_data.get('name')
                stud.details = form1.cleaned_data.get
                stud.pic=form1.cleaned_data.get('pic')
                stud.url=form1.cleaned_data.get('url')
                stud.save()
                return redirect ( 'mywebsite:detail' , person=prof )
    else:
        form=publicationform()
        form1=studentform()
        form2=researchform()
    return render( request, 'prof_detail.html' , { 'form':form, 'prof':prof , 'form1':form1,'form2':form2  })

def updatedetails(request,whoami):
    prof=Profile.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        form = editform(request.POST,instance=prof)
        if form.is_valid():
            prof.designation = form.cleaned_data.get('designation')
            prof.webmail=form.cleaned_data.get('webmail')
            prof.first_name=form.cleaned_data.get('first_name')
            prof.bio=form.cleaned_data.get('bio')
            prof.second_name=form.cleaned_data.get('second_name')
            prof.phone_number = form.cleaned_data.get('phone_number')
            prof.fax_number = form.cleaned_data.get('fax_number')
            prof.department = form.cleaned_data.get('department')
            prof.save()
            return redirect( 'mywebsite:detail' , person = prof )

    else:
        form = editform(instance=prof)
    return render(request, 'edit_details.html' , {'form': form})
def p_edit(request,person,pub):
    prof=Profile.objects.filter(user=request.user)[0]
    public=Publica.objects.filter(profile=prof,id=pub)[0]
    if request.method == 'POST':
        form = publicationform(request.POST,instance=public)
        if form.is_valid():
            public.publication_title = form.cleaned_data.get('publication_title')
            public.collaborator = form.cleaned_data.get('collaborator')
            public.collaborator_email= form.cleaned_data.get('collaborator_email')
            public.save()
            return redirect( 'mywebsite:detail' , person = prof )

    else:
        form = publicationform(instance=public)
    return render(request, 'p_edit.html' , {'form': form})

def r_edit(request,person,res):
    prof=Profile.objects.filter(user=request.user)[0]
    public=Research.objects.filter(id=res,profile=prof)[0]
    if request.method == 'POST':
        form2 = researchform(request.POST,instance=public)
        if form2.is_valid():
            public.profile = prof
            public.research_interest_title = form2.cleaned_data.get('research_interest_title')
            public.research_interest_description= form2.cleaned_data.get('research_interest_description')
            public.save()
            return redirect ( 'mywebsite:detail' , person=prof )
    else:
        form2 = researchform(instance=public)
    return render(request, 'r_edit.html' , {'form': form2})

def s_edit(request,person,std):
    prof=Profile.objects.filter(user=request.user)[0]
    stud=Students.objects.filter(id=std,supervisor=prof)[0]
    if request.method == 'POST':
        form1 =studentform(request.POST,instance=stud)
        if form1.is_valid():
            stud.supervisor = prof
            stud.name = form1.cleaned_data.get('name')
            stud.details = form1.cleaned_data.get
            stud.pic=form1.cleaned_data.get('pic')
            stud.url=form1.cleaned_data.get('url')
            stud.save()
            return redirect ( 'mywebsite:detail' , person=prof )

    else:
        form1 = studentform(instance=stud)
    return render(request, 's_edit.html' , {'form': form1})

def s_del(request,person,std):
    prof=Profile.objects.filter(user=request.user)[0]
    stud=Students.objects.filter(id=std,supervisor=prof)[0]
    stud.delete()
    return redirect ( 'mywebsite:detail' , person=prof )


def r_del(request,person,res):
    prof=Profile.objects.filter(user=request.user)[0]
    public=Research.objects.filter(id=res,profile=prof)[0]
    public.delete()
    return redirect ( 'mywebsite:detail' , person=prof )

def p_del(request,person,pub):
    prof=Profile.objects.filter(user=request.user)[0]
    public=Publica.objects.filter(id=pub,profile=prof)[0]
    public.delete()
    return redirect ( 'mywebsite:detail' , person=prof )

def download_file(request,file_name):
    file_path = settings.MEDIA_ROOT +'/'+ file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response
