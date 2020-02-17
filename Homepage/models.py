from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        default=None,
        null=True
    )
    profilePicture = models.ImageField(upload_to="images/", blank=True, default=None, null=True)
    def __str__(self):
        return self.user.username

class Lecture(models.Model):
    title = models.CharField(max_length=200,null=True)
    subject = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=2000,null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,blank=True,null=True)
    #image = models.ImageField(upload_to='lecture_image',blank=True)
class Lecture_img(models.Model):
    LectureKey = models.ForeignKey(Lecture, on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(upload_to='lecture_image',blank=True)
    
