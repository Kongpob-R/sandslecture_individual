from django.forms import ModelForm
from .models import *

# Create the form class.
class Profileform(ModelForm):
     class Meta:
        model = Profile
        fields = ['profilePicture']
