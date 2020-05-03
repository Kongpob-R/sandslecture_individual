from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import *
from .models import Note, Profile, NoteImage
from django.forms import modelformset_factory
from django.http import Http404
from django.db.models import Count
from django.contrib import messages

class NoteWithThumbnail:
    def __init__(self, note, thumbnail):
        self.note = note
        self.thumbnail = thumbnail

# Create your views here.
def signup(request):
    # inheritance user authentication from build-in django.auth
    # when user is signing up with UserCreationForm a User object will be created
    # this method will create Profile object with one-to-one relationship to that User object
    # So, that we can store more information in Profile object than User object, such as profile picture
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            newUser = form.save()
            Profile.objects.create(user = newUser)
            username = form.cleaned_data.get('username')
            rawPassword = form.cleaned_data.get('password1')
            signInUserObject = authenticate(username=username, password=rawPassword)
            login(request, signInUserObject)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    # fetching out the note with match keyword in title or description and return with rearchresult.html
    # else if no keyword were given it will fetch out latestNote and popularNote
    matchNote = []
    latestNote = []
    popularNote = []
    if request.GET.get('word'):
        keyword = request.GET.get('word').lower()
        for note in Note.objects.all():
            if keyword in note.title.lower() or keyword in note.description.lower():
                matchNote.append(NoteWithThumbnail(note, note.NoteImage.all()[0]))
        return render(request, 'searchresult.html', {'matchNote':matchNote})
    else:
        for note in Note.objects.all().order_by('-id')[:8][::-1]:
            latestNote.append(NoteWithThumbnail(note, note.NoteImage.all()[0]))
        
        for note in Note.objects.annotate(count = Count('userSaved')).order_by('count')[:8][::-1]:
            popularNote.append(NoteWithThumbnail(note, note.NoteImage.all()[0]))

        return render(request, 'home.html',{'latestNote': latestNote, 'popularNote': popularNote})

def upload(request):
    # handler for an upload content, create Note object for given title, description and author
    # create NoteImage object for each images in the content
    if Profile.objects.filter(user=request.user):
        profileObject = Profile.objects.get(user=request.user)
        if request.method == 'POST':
            NoteForm = NoteForms(request.POST)
            if NoteForm.is_valid():
                NoteForm = NoteForm.save(commit=False)
                NoteForm.author = profileObject
                NoteForm.save()

                for imageFile in request.FILES.getlist('image'):
                    photo = NoteImage.objects.create(noteKey=NoteForm, image=imageFile)
                    photo.save()

                # redirect to homepage
                return redirect('/')

            else:
                error="Please choose your file"

        else:
            NoteForm = NoteForms()
            error=""
        return render(request, 'upload.html', {'NoteForm': NoteForm, "Error": error})
    else:
        raise Http404("Profile does not found")

def changePassword(request):
    # handle the password changing
    # username and password are in User object from django.auth and django are provide a method to edit it already.
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changePassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user) 
    return render(request,'change_password.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def help(request):
    return render(request, 'help.html')

def noteView(request, noteID):
    # 'noteID' in the prameter come from url's interger field
    # path(note/<int:noteID>/) whatever in there will be in noteID

    # deleting and saving note will send the same post request here, logic bellow will be choose what to do
    if request.method == 'POST':
        profileObject = Profile.objects.get(user = request.user)
        noteObject = Note.objects.get(id = int(request.POST.get('noteID')))

    # delete the note, when user are login as note's author
        if profileObject == noteObject.author:
            noteObject.delete()
            return HttpResponseRedirect("/")

    # save the note, when user login as any others that not note's author
    # that user's Profile object will be add to many-to-many of that note's userSaved
        elif profileObject not in noteObject.userSaved.all():
            noteObject.userSaved.add(profileObject)
            noteObject.save()
        return HttpResponseRedirect("/note/" + request.POST.get('noteID'))

    # handle the request noteID and fetch the Note object with that ID and also all the NoteImage object related to that Note object
    else:
        noteObject = Note.objects.get(id = noteID)
        imageObjectList = noteObject.NoteImage.all()
        return render(request, 'notedetail.html', {'noteObject': noteObject, "imageObjectList": imageObjectList})
    # notedetail page contain a button that will change it self to
    # save button, 
    # delete button, when user login as note's author
    # login link text, when user are not login

def profile(request, username):
    # handle the request of user when a profile picture was uploaded and update Profile object with that picture
    # else if user wasn't decide to upload this method will return infomation about that Profile object and Note and NoteImage objects related
    # with that Profile object
    userObject = User.objects.get(username = username)
    profileObject = Profile.objects.get(user = userObject)
    if request.method == 'POST':
        form = Profileform(request.POST, request.FILES)
        if form.is_valid():
            profileObject.profilePicture = form.cleaned_data.get('profilePicture')
            profileObject.save()
            
            return HttpResponseRedirect("/profile/"+username)
    else:
        form = Profileform()
        myNote = []
        savedNote = []
        totalSaves = 0
        for note in profileObject.author.all():
            myNote.append(NoteWithThumbnail(note, note.NoteImage.all()[0]))
            totalSaves += note.userSaved.count()
        for note in Note.objects.all():
            if profileObject in note.userSaved.all():
                savedNote.append(NoteWithThumbnail(note, note.NoteImage.all()[0]))
    return render(request,'profile.html', {'form': form, 'profile': profileObject, 'myNote': myNote, 'savedNote': savedNote, 'totalSaves': totalSaves})