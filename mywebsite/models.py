

# Create your models here.

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    webmail=models.EmailField(null=True,blank=True)
    first_name=models.CharField(max_length=500,blank=True)
    second_name=models.CharField(max_length=500,blank=True)
    education = models.TextField(max_length=1500, blank=True)
    designation = models.TextField(max_length=1500, blank=True)
    research_interest=models.TextField(max_length=1500, blank=True)
    publications = models.TextField(max_length=1500, blank=True)


    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Students(models.Model):
    supervisor=models.ForeignKey(Profile, on_delete=models.CASCADE)
    name=models.CharField(max_length=100,blank=True)
    details=models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name
