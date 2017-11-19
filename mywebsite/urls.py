from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import  include
from django.contrib.auth import views as auth_views
from mywebsite import views as core_views
app_name = 'mywebsite'


urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^(?P<person>[a-zA-Z0-9_]+)$', core_views.showdetail , name='detail'),
    url(r'^update/(?P<whoami>[a-zA-Z0-9_]+)$', core_views.updatedetails , name='update'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'mywebsite:login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^(?P<person>[a-zA-Z0-9_]+)/courses$', core_views.courses , name='courses') ,
    url(r'^(?P<course>[a-zA-Z0-9_]+)/courses/upload$', core_views.courses_upload , name='courses_upload'),
    url(r'^download/(?P<file_name>.+)$', core_views.download_file , name='download')

]
