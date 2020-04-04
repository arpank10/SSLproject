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
    url(r'^login/$', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page = 'mywebsite:login'), name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^(?P<person>[a-zA-Z0-9_]+)/courses$', core_views.courses , name='courses') ,
    url(r'^(?P<course>[a-zA-Z0-9_]+)/courses/upload$', core_views.courses_upload , name='courses_upload'),
    url(r'^details/(?P<person>[a-zA-Z0-9_]+)/(?P<pub>[a-zA-Z0-9_]+)/publication_edit$', core_views.p_edit , name='publica_edit') ,
    url(r'^details/(?P<person>[a-zA-Z0-9_]+)/(?P<std>[a-zA-Z0-9_]+)/student_edit$', core_views.s_edit , name='student_edit') ,
    url(r'^details/(?P<person>[a-zA-Z0-9_]+)/(?P<res>[a-zA-Z0-9_]+)/research_edit$', core_views.r_edit , name='research_edit') ,
    url(r'^details/(?P<person>[a-zA-Z0-9_]+)/(?P<pub>[a-zA-Z0-9_]+)/publication_delete$', core_views.p_del , name='publica_delete') ,
    url(r'^details/(?P<person>[a-zA-Z0-9_]+)/(?P<std>[a-zA-Z0-9_]+)/student_delete$', core_views.s_del , name='student_delete') ,
    url(r'^details/(?P<person>[a-zA-Z0-9_]+)/(?P<res>[a-zA-Z0-9_]+)/research_delete$', core_views.r_del , name='research_delete') ,
    url(r'^download/(?P<file_name>.+)$', core_views.download_file , name='download')

]
