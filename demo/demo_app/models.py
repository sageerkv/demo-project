from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Projects(models.Model):
    project_img = models.ImageField(upload_to='service')
    project_img_1 = models.ImageField(upload_to='service')
    project_title = models.CharField(max_length=255)
    project_text = models.CharField(max_length=255)
    project_link = models.URLField()

class Services(models.Model):
    service_img = models.ImageField(upload_to='service')
    service_img_1 = models.ImageField(upload_to='service')
    service_title = models.CharField(max_length=255)
    service_text = models.CharField(max_length=255)
    service_link = models.URLField()

class Contact(models.Model):
    c_name = models.CharField(max_length=255)
    c_email = models.EmailField()
    c_subject = models.CharField(max_length=300)
    c_text_area = models.TextField()