from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import *

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
    return render(request, 'upload.html')

def lecture(request,lectue_id):
    pass

def profile(request):
    if request.method == 'POST':
        form=Profileform(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            
            
            return render(request,'test_profile.html',{'form_44':object_img})
    else:
        form=Profileform()
    return render(request,'test_profile.html',{'form':form})

