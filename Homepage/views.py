from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import *
from .models import Lecture,Profile,Lecture_img

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            newUser = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            Profile.objects.create(user = newUser)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    return render(request, 'home.html')

def upload(request):
    r=1
    
    if request.user.is_authenticated==True:
        Profile_Lec=Profile.objects.filter(user=request.user)
        if request.method == 'POST' and request.FILES:
            me=0
            v=0
            LectureForms1=LectureForms(request.POST)
            Lecture_imgForms1 = Lecture_imgForms(request.POST,request.FILES)
            if LectureForms1.is_valid() and  Lecture_imgForms1.is_valid():
                
                #Lectitle=Lecture_imgForms1.cleaned_data.get(title)
                found_object=Lecture.objects.filter(title=LectureForms1.cleaned_data.get('title'),description=LectureForms1.cleaned_data.get('description'))
                #subject_object
                #description_object=Lecture.objects.filter(description=LectureForms1.cleaned_data.get('description'))
                #if title_object==description_object:
                for i in found_object:
                    L=Lecture_img.objects.filter(LectureKey=i)
                    v+=1

                #me=Lecture(title=LectureForms1.cleaned_data.get('title'),subject=LectureForms1.cleaned_data.get('subject'),description=LectureForms1.cleaned_data.get('description'))
                if v>0:
                    
                    #Saveimg=Lecture_img.objects.filter(LectureKey=me)
                    Lec=LectureForms1.save(commit=False)
                    Lec.author=Profile_Lec[0]
                    
                    Manyimg= L[0].LectureKey
                    Lecture_img.objects.create(LectureKey=Manyimg,image=Lecture_imgForms1.cleaned_data.get('image')) 
                # Saveimg.LectureKey=me
                # Saveimg.save()
                    Img_obj=Lecture_img.objects.all().filter(LectureKey=Manyimg)
                

                else:
                    Lec=LectureForms1.save(commit=False)
                    Lec.author=Profile_Lec[0]
                    Lec.save()
                    Saveimg=Lecture_imgForms1.save(commit=False)
                    Saveimg.LectureKey=Lec
                    Saveimg.save()
                
                    Img_obj=Lecture_img.objects.all().filter(LectureKey=Lec)
                

                
            return render(request, 'upload.html',{'form':Lecture_imgForms1 , 'Lecture':LectureForms1 , "Lecture_img":Img_obj , "title_object":found_object , "r":request.FILES})
            
            '''elif not request.FILES:
            LectureForms1=LectureForms(request.POST)
            Lecture_imgForms1 = Lecture_imgForms(request.POST,request.FILES)
            if Lecture.objects.filter()
            return render(request, 'upload.html',{'form':'Lecture_imgForms1' , 'Lecture':LectureForms1,"r":r})'''

        else:
            Lecture_imgForms1=Lecture_imgForms()
            LectureForms1=LectureForms()
        return render(request, 'upload.html',{'form':Lecture_imgForms1 , 'Lecture':LectureForms1,"r":request.FILES})

def lecture(request,lectue_id):
    pass

def profile(request, username):
    userObj = User.objects.get(username = username)
    profileObj = Profile.objects.get(user = userObj)
    if request.method == 'POST':
        form=Profileform(request.POST , request.FILES)
        if form.is_valid():
            profileObj.profilePicture = form.cleaned_data.get('profilePicture')
            profileObj.save()
            
            return HttpResponseRedirect("/profile/"+username)
    else:
        form=Profileform()
    return render(request,'profile.html',{'form': form, 'profile': profileObj})

