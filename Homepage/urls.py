from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html')
def login(request):
    return render(request, 'login.html')