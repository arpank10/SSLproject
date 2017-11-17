from requests import request, HTTPError
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from mywebsite.models import Profile


def save_profile_picture(backend, user, response, details, *args, **kwargs):
    url = None
    profile = Profile.objects.filter(user = user).first()
    if backend.name == 'facebook':
        #url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        #response = request('GET', url, params={'type': 'large'})
        #response.raise_for_status()
        #m.save('{0}_social.jpg'.format(profile.first_name),
                                 #  ContentFile(response.content))
        #profile.fbprofile_photo.save('{0}_social.jpg'.format(profile.first_name),
                                   #ContentFile(response.content))
        profile.fbprofile_photo  = 'http://graph.facebook.com/{0}/picture?type=large'.format(response['id'])
    profile.save()
