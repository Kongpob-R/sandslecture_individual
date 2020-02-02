from django.db import models
from django.conf import settings

# Create your models here.

class Lecture(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)
    image = models.ImageField(upload_to='lecture_image',blank=True)