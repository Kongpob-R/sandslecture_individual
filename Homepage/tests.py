from Homepage.models import Lecture
from django.contrib.auth.models import User
from django.shortcuts import render
from django.test import TestCase
from .forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.core.files import File
from sandslecture.settings import BASE_DIR

class HomePageTest(TestCase):

    def test_saving_and_retrieving_lecture_title(self):
        firstLecture = Lecture()
        firstLecture.title = 'The first (ever) lecture title'
        firstLecture.save()

        secondLecture = Lecture()
        secondLecture.title = 'lecture title the second'
        secondLecture.save()

        lectures = Lecture.objects.all()
        self.assertEqual(lectures.count(), 2)

        firstLecture = lectures[0]
        secondLecture = lectures[1]
        self.assertEqual(firstLecture.title, 'The first (ever) lecture title')
        self.assertEqual(secondLecture.title, 'lecture title the second')

    def test_saving_lecture_id_auto_increment_start_at_1(self):
        firstLecture = Lecture()
        firstLecture.title = 'The first (ever) lecture title'
        firstLecture.save()

        secondLecture = Lecture()
        secondLecture.title = 'lecture title the second'
        secondLecture.save()

        lectures = Lecture.objects.all()
        self.assertEqual(lectures.count(), 2)

        firstLecture = lectures[0]
        secondLecture = lectures[1]
        self.assertEqual(firstLecture.id, 1)
        self.assertEqual(secondLecture.id, 2)

    def test_upload_forms_Profile(self):
        c = Client()
        form=Profileform()
        localtion=BASE_DIR
        response = c.post('/profile/<str:username>/', {'profilePicture':SimpleUploadedFile('666.png', content=open(localtion+'/red.png', 'rb').read())} ) 
        Count_object=Profile.objects.count()
        obj = Profile.objects.all().last()
        field_object = Profile._meta.get_field('profilePicture')
        field_value = field_object.value_from_object(obj)
        self.assertEqual(Count_object, 1)
        self.assertEqual(field_value, 1)

    def test_upload_Model_Profile(self):
        
        model=Profile()
        localtion=BASE_DIR
        model.profilePicture = SimpleUploadedFile(name='test_image_profile.png', content=open(localtion+"/red.png", 'rb').read(), content_type='image/png')
        model.save()
        obj = Profile.objects.all().last()
        field_object = Profile._meta.get_field('profilePicture')
        field_value = field_object.value_from_object(obj)
        self.assertEqual(field_value,1)

    def test_upload_Model_Lecture(self):
        model=Lecture()
        localtion=BASE_DIR
        model.image = SimpleUploadedFile(name='test_image_lec.png', content=open(localtion+"/red.png", 'rb').read(), content_type='image/png')
        model.save()
        obj = Lecture.objects.all().last()
        field_object = Lecture._meta.get_field('image')
        field_value = field_object.value_from_object(obj)
        self.assertEqual(field_value,1)
