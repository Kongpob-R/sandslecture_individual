from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import *
from .models import Lecture,Profile,Lecture_img

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    return render(request, 'home.html')

def upload(request):
    
    if request.method == 'POST':
        me=0
        v=0
        LectureForms1=LectureForms(request.POST)
        Lecture_imgForms1 = Lecture_imgForms(request.POST,request.FILES)
        if LectureForms1.is_valid() and  Lecture_imgForms1.is_valid():
            Lec=LectureForms1.save(commit=False)
            #Lectitle=Lecture_imgForms1.cleaned_data.get(title)
            title_object=Lecture.objects.filter(title=LectureForms1.cleaned_data.get('title'),description=LectureForms1.cleaned_data.get('description'))
            #subject_object
            #description_object=Lecture.objects.filter(description=LectureForms1.cleaned_data.get('description'))
            #if title_object==description_object:
            for i in title_object:
                L=Lecture_img.objects.filter(LectureKey=i)
                v+=1

            #me=Lecture(title=LectureForms1.cleaned_data.get('title'),subject=LectureForms1.cleaned_data.get('subject'),description=LectureForms1.cleaned_data.get('description'))
            if v>0:
                
                #Saveimg=Lecture_img.objects.filter(LectureKey=me)
                Manyimg= L[0].LectureKey
                Lecture_img.objects.create(LectureKey=Manyimg,image=Lecture_imgForms1.cleaned_data.get('image')) 
               # Saveimg.LectureKey=me
               # Saveimg.save()
                Img_obj=Lecture_img.objects.all().filter(LectureKey=Manyimg)
               

            else:
                Lec=LectureForms1.save()
                Saveimg=Lecture_imgForms1.save(commit=False)
                Saveimg.LectureKey=Lec
                Saveimg.save()
            
                Img_obj=Lecture_img.objects.all().filter(LectureKey=Lec)
            

             
            return render(request, 'upload.html',{'form':Lecture_imgForms1 , 'Lecture':LectureForms1 , "Lecture_img":Img_obj , "title_object":title_object})
        

    else:
        Lecture_imgForms1=Lecture_imgForms()
        LectureForms1=LectureForms()
    return render(request, 'upload.html',{'form':Lecture_imgForms1 , 'Lecture':LectureForms1})

    '''Lecture=LectureForms()
    profileObj = Lecture_img.objects.get(id=1)
    if request.FILES:
        form=Lecture_imgForms(request.FILES)
        if form.is_valid():
            profileObj.image = form.cleaned_data.get('image')
            profileObj.save()
    else:
        form=Lecture_imgForms()

    return render(request, 'upload.html',{'form':form})'''

def lecture(request,lectue_id):
    pass

def profile(request, username):
    profileObj = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        form=Profileform(request.POST , request.FILES)
        if form.is_valid():
            profileObj.profilePicture = form.cleaned_data.get('profilePicture')
            profileObj.save()
            
            return HttpResponseRedirect("/profile/"+username)
    else:
        form=Profileform()
    return render(request,'profile.html',{'form': form, 'profile': profileObj})

