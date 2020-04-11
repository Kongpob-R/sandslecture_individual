from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, blank = True, default = None, null = True)
    profilePicture = models.ImageField(upload_to = "profilePictures/", blank = True, default = None, null = True)
    def __str__(self):
        return self.user.username

class Note(models.Model):
    title = models.CharField(max_length = 200, null = True)
    subject = models.CharField(max_length = 200, null = True)
    description = models.CharField(max_length = 2000, null = True)
    author = models.ForeignKey(Profile, related_name = 'author', on_delete = models.CASCADE, blank = True, null = True)
    userSaved = models.ManyToManyField(Profile)
    def __str__(self):
        return self.title

class NoteImage(models.Model):
    noteKey = models.ForeignKey(Note, related_name = 'NoteImage', on_delete = models.CASCADE, blank = True, null = True)
    image = models.ImageField(upload_to = 'noteImages/', blank = True)
    def __str__(self):
        return self.image.name

    
