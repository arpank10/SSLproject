

# Create your models here.

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    DEP_CHOICES = (
        ('CSE','CSE'),
        ('ECE', 'ECE'),
        ('EEE','EEE'),
        ('DOD','DOD'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    webmail=models.EmailField(null=True,blank=True)
    first_name=models.CharField(max_length=500,blank=True)
    second_name=models.CharField(max_length=500,blank=True)
    phone_number = PhoneNumberField(blank=True)
    fax_number = PhoneNumberField(blank=True)
    department = models.CharField(max_length=4, choices=DEP_CHOICES, default='cse')
    designation = models.TextField(max_length=500, blank=True)
    fbprofile_photo = models.URLField( blank=True)

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

class Publica(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publication_title=models.TextField(max_length=1500,blank=True)
    collaborator=models.CharField(max_length=500,blank=True)
    collaborator_email=models.EmailField(null=True,blank=True)

    def __str__(self):
        return self.publication_title

class Courses(models.Model):
    prof= models.ForeignKey(Profile, on_delete=models.CASCADE)
    courseName= models.CharField(max_length=10)
    startDate= models.DateField(blank=True,null=True)
    endDate = models.DateField(blank=True,null=True)
    current = models.BooleanField(default=False)

    def __str__(self):
        return self.courseName


class Document(models.Model):
    course_name= models.ForeignKey(Courses, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField()
    uploaded_at = models.DateTimeField(default=timezone.now)
