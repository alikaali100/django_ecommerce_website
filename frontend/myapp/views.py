from django.shortcuts import render, redirect
import requests
from .forms import SignupForm, LoginForm

def products_view(request):
    try:
        response = requests.get('http://localhost:8000/api/products/')
        if response.status_code == 200:
            data = response.json()  
        else:
            data = []
    except requests.exceptions.RequestException as e:
        data = []  
        print(f"Error fetching products: {e}")

    return render(request, 'products.html', {'products': data})

def home_view(request):
    try:
        response = requests.get('http://localhost:8000/api/products/')
        if response.status_code == 200:
            data = response.json()  
        else:
            data = []
    except requests.exceptions.RequestException as e:
        data = []  
        print(f"Error fetching products: {e}")

    return render(request, 'home.html', {'products': data})

def contact_view(request):
    return render(request, 'contact.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')


