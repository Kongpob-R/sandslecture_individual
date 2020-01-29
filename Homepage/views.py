from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, 'home.html')
def upload(request):
    return render(request, 'upload.html')

