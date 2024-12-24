from django.shortcuts import render, redirect
import requests
from .forms import SignupForm, LoginForm

def products_view(request):
    try:
        # درخواست به API برای دریافت محصولات
        response = requests.get('http://localhost:8000/api/products/')
        if response.status_code == 200:
            data = response.json()  # تبدیل پاسخ به JSON
        else:
            data = []
    except requests.exceptions.RequestException as e:
        data = []  # در صورت بروز خطا، لیست محصولات خالی باشد
        print(f"Error fetching products: {e}")

    # ارسال داده‌ها به قالب
    return render(request, 'products.html', {'products': data})



BACKEND_SIGNUP_URL = "http://localhost:8000/api/signup/"

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            response = requests.post(BACKEND_SIGNUP_URL, json=data)
            if response.status_code == 201:
                return redirect("login")  # Redirect to login page
            form.add_error(None, "Signup failed. Try again.")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})

BACKEND_LOGIN_URL = "http://localhost:8000/api/login/"

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            response = requests.post(BACKEND_LOGIN_URL, json=data)
            if response.status_code == 200:
                tokens = response.json()
                request.session["access_token"] = tokens["access"]
                request.session["refresh_token"] = tokens["refresh"]
                return redirect("home")  # Redirect to home page
            form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})
