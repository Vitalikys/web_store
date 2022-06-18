from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def login(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'index.html')

def logout(request):
    return render(request, 'index.html')