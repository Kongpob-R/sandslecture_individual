from django.contrib import admin
from .models import Note, Profile, NoteImage

# Register your models here.
admin.site.register(Note)
admin.site.register(Profile)
admin.site.register(NoteImage)