from django.forms import ModelForm
from .models import *

# Create the form class.
class Profileform(ModelForm):
     class Meta:
        model = Profile
        fields = ['profilePicture']

class NoteForms(ModelForm):
   class Meta:
      model = Note
      fields = ['title','description']

class NoteImageForms(ModelForm):
      class Meta:
         model = NoteImage
         fields = ['image']