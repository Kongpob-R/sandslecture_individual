from Homepage.models import *
from django.contrib.auth.models import User
from django.shortcuts import render
from django.test import TestCase
from .forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.core.files import File
from sandslecture.settings import BASE_DIR
import os
from pathlib import Path
import glob

class HomePageTest(TestCase):

    def test_adding_new_model_Profile(self):
        # create Profile object with one-to-one to User object
        password = 'newPassword'
        newUser = User.objects.create_user('newUser', password)
        newProfile = Profile()
        newProfile.user = newUser
        newProfile.save()

        # and test that those 2 object are relate
        self.assertEqual('newUser',newProfile.user.username)

    def test_saving_note_id_auto_increment_starting_at_1(self):
        # create 2 Note objects with different title
        firstNote = Note()
        firstNote.title = 'The first (ever) lecture title'
        firstNote.save()

        secondNote = Note()
        secondNote.title = 'lecture title the second'
        secondNote.save()

        # test that exactly 2 Note objects were created
        notes = Note.objects.all()
        self.assertEqual(notes.count(), 2)

        # test that the generated id for firstNote and secondNote are 1 and 2 respectivly
        firstNote = notes[0]
        secondNote = notes[1]
        self.assertEqual(firstNote.id, 1)
        self.assertEqual(secondNote.id, 2)

    def test_uploading_Profile_picture(self):
        # create a User object and Profile object
        client = Client()
        form = Profileform()
        location = BASE_DIR
        Tim = User.objects.create_user(username = 'Timmy', password = '2542')
        TimProfileObject = Profile.objects.create(user = Tim)

        # create a post request to upload a profile picture
        response = client.post('/profile/'+ str(TimProfileObject) +'/', {'profilePicture': SimpleUploadedFile('666.png', content = open(location+'/red.png', 'rb').read())} ) 
        
        # test that the upload image are in the Profile object
        profileObject = Profile.objects.filter(id = 1)[0]
        self.assertNotEquals(profileObject.profilePicture, "<ImageFieldFile: None>")

    def test_uploading_Note_with_single_image(self):
        # create a User object and Profile object
        client = Client()
        location = BASE_DIR
        Tim = User.objects.create_user(username = 'Timmy', password='2542')
        TimProfileObject = Profile.objects.create(user = Tim)

        # post request to login with a created Profile object
        self.client.post('/accounts/login/', {'username': 'Timmy', 'password': "2542"}) 

        # post request to upload new Note
        # So, 1 Note object and 1 NoteImage object will be create
        self.client.post('/upload/', {'title': 'tim', 'description': "555", 'image': SimpleUploadedFile('666.png', content=open(location+'/red.png', 'rb').read())} ) 
        
        # test a total number of Note object and NoteImage object
        totalNoteCount = Note.objects.count()
        totalUploadedImages = NoteImage.objects.count()
        self.assertEqual(totalNoteCount, 1)
        self.assertEqual(totalUploadedImages, 1)

    def test_upload_Note_with_multiple_images(self):
        # create a User object and Profile object
        client = Client()
        location = BASE_DIR
        Tim = User.objects.create_user(username = 'tim', password = 'pass')
        TimProfileObject = Profile.objects.create(user = Tim)

        # post request to login with a created Profile object
        self.client.post('/accounts/login/', {'username': 'tim', 'password': "pass" } ) 

        # upload content to create 1 Note object and 2 NoteImage object
        self.client.post('/upload/', {'submitbutton': 'Submit', 'title': 'tim', 'description': "555" , 
        'image': {
        SimpleUploadedFile('666_1.png', content = open(location + '/red.png', 'rb').read()), 
        SimpleUploadedFile('666_1.png', content = open(location + '/red.png', 'rb').read())
        }})

        # test a total number of Note object and NoteImage objects
        totalNoteCount = Note.objects.count()
        totalUploadedImages = NoteImage.objects.count()
        self.assertEqual(totalNoteCount, 1)
        self.assertEqual(totalUploadedImages, 2)

    def test_search_Note(self):
        # create User and Profile object to be an author for a testCreatedNote's Note object
        creator = User.objects.create_user(username = 'tim01', password = 'pass')
        creatorProfileObject = Profile.objects.create(user = creator)
        testCreatedNote = Note.objects.create(title = 'test', description = 'test', author = creatorProfileObject)
        testCreatedNoteImage = NoteImage.objects.create(noteKey = testCreatedNote, image = SimpleUploadedFile('666_1.png', content = open(BASE_DIR + '/red.png', 'rb').read()))

        # test the response status code and content is containing keyword
        response = self.client.get('/', {'word': 'test'})
        self.assertEqual(response.status_code,200)
        decodedResponse = response.content.decode()
        self.assertIn('test', decodedResponse)

    def test_change_password(self):
        # create a User object and Profile object with first password
        creator = User.objects.create_user(username = 'tim01', password = 'pass')
        creatorProfileObject = Profile.objects.create(user = creator)

        # login and change the via a post request this lead the a method with django-built-in command to change a password
        self.client.login(username = 'tim01', password = 'pass')
        self.client.post('/change-password/', {"old_password": 'pass', "new_password1": "time25422542", "new_password2": "time25422542"})
        self.client.logout()
        
        # test response status after post login with new password
        newPasswordLoginResponse = self.client.post('/accounts/login/', {'username': 'tim01', 'password': "time25422542" }, follow = True) 
        self.assertEqual(newPasswordLoginResponse.status_code, 200)
        self.assertIn("tim01", newPasswordLoginResponse.content.decode())

    def test_Note_show_up_on_homepage(self):
        # create a User object and Profile object
        location = BASE_DIR
        Tim = User.objects.create_user(username = 'Timmy', password = '2542')
        TimProfileObject = Profile.objects.create(user = Tim)

        # post request to login and create new Note object with one image
        self.client.post('/accounts/login/', {'username': 'Timmy', 'password': "2542"}) 
        self.client.post('/upload/', {'title': 'tim', 'description': "555", 'image': SimpleUploadedFile('666.png', content = open(location + '/red.png', 'rb').read())}) 

        # post request to login and create new Note object with one image
        decodedHomepageResponse = self.client.get('/').content.decode()
        self.assertIn('666.png', decodedHomepageResponse)
        self.assertIn('tim', decodedHomepageResponse)

    def test_Note_show_on_Profile(self):
        # create a User object and Profile object
        location = BASE_DIR
        Tim = User.objects.create_user(username = 'Timmy', password = '2542')
        TimProfileObject = Profile.objects.create(user = Tim)

        # post request to login and create new Note object with one image
        self.client.post('/accounts/login/', {'username': 'Timmy', 'password': "2542"}) 
        self.client.post('/upload/', {'title': 'tim', 'description': "555", 'image': SimpleUploadedFile('666.png', content = open(location + '/red.png', 'rb').read())}) 

        # test the profile page response with Note object content in the page
        decodedProfilePageResponse = Client().post('/profile/Timmy/', follow = True).content.decode()
        self.assertIn('666.png', decodedProfilePageResponse)
        self.assertIn('tim', decodedProfilePageResponse)

    def test_deleting_note_via_post_request(self):
        # create userA's User object and Profile object
        # then, create a Note object with userA as an author
        username = 'userA'
        password = 'userApassword'
        userA = User.objects.create_user(username = username, password = password)
        userAProfileObject = Profile.objects.create(user = userA)
        testCreatedNote = Note.objects.create(title = 'test', description = 'test', author = userAProfileObject)

        # make a post request to login and delete the note
        self.client.post('/accounts/login/', {'username': username, 'password': password } ) 
        response = self.client.post('/note/' + str(testCreatedNote.id) + '/', {'noteID': str(testCreatedNote.id) })

        # test note was deleted
        self.assertNotIn(testCreatedNote, Note.objects.all())

    def test_login_state_effect_button_type_in_noteView_page(self):
        # create userA User and Profile object and a note with userA as author
        usernameA = 'userA'
        passwordA = 'userApassword'
        userA = User.objects.create_user(username = usernameA, password = passwordA)
        userAProfileObject = Profile.objects.create(user = userA)
        testCreatedNote = Note.objects.create(title = 'test', description = 'test', author = userAProfileObject)

        # create userB User and Profile object
        usernameB = 'userB'
        passwordB = 'userBpassword'
        userB = User.objects.create_user(username = usernameB, password = passwordB)
        userBProfileObject = Profile.objects.create(user = userB)

        # test button type in the page when login as anonymous user
        response = self.client.get('/note/' + str(testCreatedNote.id) + '/').content.decode()
        self.assertIn('please login to save notes', response)

        # test button type in the page when login as note's author user
        self.client.post('/accounts/login/', {'username': usernameA, 'password': passwordA } )
        response = self.client.get('/note/' + str(testCreatedNote.id) + '/').content.decode()
        self.assertIn('Delete Note', response)
        self.client.post('/accounts/logout/')

        # test button type in the page when login as another user that isn't note's author
        self.client.post('/accounts/login/', {'username': usernameB, 'password': passwordB } )
        response = self.client.get('/note/' + str(testCreatedNote.id) + '/').content.decode()
        self.assertIn('Save Note', response)
        self.client.post('/accounts/logout/')

    def tearDown(self):
        # clear the Images directory after finish all the test
        for directory in glob.glob(BASE_DIR+'/sandslecture/media/*'):
            directory = Path(directory)
            for file in directory.glob('666*.png'):
                os.remove(file)

        
        


       