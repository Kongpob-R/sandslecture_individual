from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    # store User object of django auth
    # store profile picture
    user = models.OneToOneField(User, on_delete = models.CASCADE, blank = True, default = None, null = True)
    profilePicture = models.ImageField(upload_to = "profilePictures/", blank = True, default = None, null = True)
    def __str__(self):
        return self.user.username

class Note(models.Model):
    # store title and description of the note
    # store author with many-to-one to Profile object
    # store userSaved with many-to-many with Profile object
    title = models.CharField(max_length = 200, null = True)
    subject = models.CharField(max_length = 200, null = True)
    description = models.CharField(max_length = 2000, null = True)
    author = models.ForeignKey(Profile, related_name = 'author', on_delete = models.CASCADE, blank = True, null = True)
    userSaved = models.ManyToManyField(Profile, related_name = 'noteSaved')
    def __str__(self):
        return self.title

class NoteImage(models.Model):
    # store noteKey as many-to-one to Note object
    # each NoteImage object contain 1 images
    noteKey = models.ForeignKey(Note, related_name = 'NoteImage', on_delete = models.CASCADE, blank = True, null = True)
    image = models.ImageField(upload_to = 'noteImages/', blank = True)
    def __str__(self):
        return self.image.name

# related_name is use for trace back for easier calling
# normally:
# noteA.author.all() will return 1 Profile object of author of noteA
# trace back:
# userA.author.all() will return all Note objects that have userA as author
# noteA.NoteImage.all() will return all NoteImage objects that have noteA as noteKey
