from Homepage.models import *
from django.contrib.auth.models import User
from django.shortcuts import render
from django.test import TestCase
from .forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.core.files import File
from sandslecture.settings import BASE_DIR

class HomePageTest(TestCase):

    def test_adding_new_model_Profile(self):
        password = 'newPassword'
        newUser = User.objects.create_superuser('newUser','newUser@email.com', password)
        newProfile = Profile()
        newProfile.user = newUser
        newProfile.save()
        self.assertEqual('newUser',newProfile.user.username)
        
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
        self.assertEqual(Count_object,'<ImageFieldFile: lecture_image/test_image_lec_SJw9IrQ.png>')
        self.assertEqual(field_value, 1)

    def test_upload_Model_Profile(self):
        
        model=Profile()
        localtion=BASE_DIR
        model.profilePicture = SimpleUploadedFile(name='test_image_profile.png', content=open(localtion+"/red.png", 'rb').read(), content_type='image/png')
        model.save()
        obj = Profile.objects.all().last()
        field_object = Profile._meta.get_field('profilePicture')
        field_value = field_object.value_from_object(obj)
        self.assertEqual(field_value,'<ImageFieldFile: images/test_image_profile.png>')

    def test_upload_Model_Lecture(self):
        model=Lecture()
        localtion=BASE_DIR
        model.image = SimpleUploadedFile(name='test_image_lec.png', content=open(localtion+"/red.png", 'rb').read(), content_type='image/png')
        model.save()
        obj = Lecture.objects.all().last()
        field_object = Lecture._meta.get_field('image')
        field_value = field_object.value_from_object(obj)
        self.assertEqual(field_value,1)

    def test_upload_forms_Lecture(self):
        c = Client()
        
        localtion=BASE_DIR
        response = c.post('/upload/', {'username':'Timmy','password':"2542" } ) 
        response = c.post('/upload/', {'title':'tim','description':"555" ,'image':SimpleUploadedFile('666.png', content=open(localtion+'/red.png', 'rb').read())} ) 
        CountLec=Lecture.objects.count()
        Count_object=Lecture_img.objects.count()
        #obj = Profile.objects.all().last()
        # field_object = Profile._meta.get_field('profilePicture')
        #field_value = field_object.value_from_object(obj)
       # self.assertTrue(Count_object.is_valid())
        self.assertEqual(CountLec,1)
        self.assertEqual(Count_object,1)
        self.assertEqual(response.status_code,200)
        #self.assertEqual(field_value, 1)

    def test_upload_Lecture(self):
        c=Client()
        localtion=BASE_DIR
        Tim=User.objects.create_user(username='tim',password='pass')
        ProfileTim=Profile.objects.create(user=Tim)
        #self.client.login(username='tim', password='pass')
        self.client.post('/accounts/login/', {'username':'tim','password':"pass" } ) 
        self.client.post('/upload/', {'submitbutton':'Submit','title':'tim','description':"555" ,'image':{SimpleUploadedFile('666_1.png', content=open(localtion+'/red.png', 'rb').read()),SimpleUploadedFile('666_1.png', content=open(localtion+'/red.png', 'rb').read())}} )
        self.assertEqual(Lecture.objects.count(),1)
        self.assertEqual(Lecture_img.objects.count(),2)
    def test_button_upload_Clear(self):
        c=Client()
        localtion=BASE_DIR
        Tim=User.objects.create_user(username='tim',password='pass')
        ProfileTim=Profile.objects.create(user=Tim)
        #self.client.login(username='tim', password='pass')
        self.client.post('/accounts/login/', {'username':'tim','password':"pass" } ) 
        response = self.client.post('/upload/', {'Clearbutton':'Clear','title':'tim','description':"555" ,'image':SimpleUploadedFile('666_1.png', content=open(localtion+'/red.png', 'rb').read())} )
        #self.assertContains( response, {"title" :""}, status_code=200 )
        self.assertEqual(response.content["title"],1)
        self.assertEqual(Lecture_img.objects.count(),1)
    
    def test_counting_saves(self):
        creator = User.objects.create_user(username = 'tim',password = 'pass')
        creatorProfile = Profile.objects.create(user = creator)
        userA = User.objects.create_user(username = 'tim',password = 'pass')
        userAProfile = Profile.objects.create(user = userA)
        userB = User.objects.create_user(username = 'tim',password = 'pass')
        userBProfile = Profile.objects.create(user = userB)
        noteObj = Lecture.objects.create(title = 'test', description = 'test',author = creatorProfile)
        noteObj.userSaved.add(userA)
        noteObj.save()
        self.assertEqual(Lecture.objects.userSaved.count(),1)
        noteObj.userSaved.add(userB)
        noteObj.save()
        self.assertEqual(Lecture.objects.userSaved.count(),2)
       