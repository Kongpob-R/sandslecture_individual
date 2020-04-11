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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form.is_valid())
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
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user) 
    return render(request,'change_password.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def help(request):
    return render(request, 'help.html')

def noteView(request, lecture_id):
    if request.method == 'POST':
        profileObject = Profile.objects.get(user = request.user)
        noteObject = Note.objects.get(id = int(request.POST.get('noteID')))
        if profileObject not in noteObject.userSaved.all():
            noteObject.userSaved.add(profileObject)
            noteObject.save()
        return HttpResponseRedirect("/" + request.POST.get('noteID'))
    else:
        noteObject = Note.objects.get(id = lecture_id)
        imageObjectList = noteObject.NoteImage.all()
        return render(request, 'notedetail.html', {'noteObject': noteObject, "imageObjectList": imageObjectList})

def profile(request, username):
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