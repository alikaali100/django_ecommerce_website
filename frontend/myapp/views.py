from django.shortcuts import render, redirect
import requests

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
        response = requests.get('http://localhost:8000/api/products/discounted/')
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

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Send the registration data to your backend API
        response = requests.post(f"{API_BASE_URL}/api/customers/register/", data={
            "username": username,
            "email": email,
            "password": password
        })

        if response.status_code == 201:
            # Redirect to login page after successful registration
            return redirect('/login/')
        else:
            # Handle error (show error message to user)
            context = {"error": "Registration failed, please try again."}
            return render(request, "register.html", context)

    return render(request, "register.html")
    
API_BASE_URL = "http://127.0.0.1:8000"  # Update to match your backend URL

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Call the backend login API
        response = requests.post(f"{API_BASE_URL}/api/customers/login/", data={"email": email, "password": password})

        if response.status_code == 200:
            # Redirect to home page after successful login
            return render(request, "login.html")
        else:
            # Handle error
            context = {"error": "Invalid email or password"}
            return render(request, "login.html", context)
    return render(request, "login.html")

from django.http import HttpResponse

def logout_view(request):
    try:
        # ارسال درخواست logout به API
        response = requests.post(
            f"{API_BASE_URL}/api/customers/logout/",
            cookies=request.COOKIES,  # ارسال کوکی‌ها برای احراز هویت
        )
        
        if response.status_code == 200:
            # پاک کردن کوکی‌ها در سمت کلاینت
            logout_response = redirect("login")  # ریدایرکت به صفحه لاگین
            logout_response.delete_cookie("access_token")  # پاک کردن کوکی access_token
            # در صورت نیاز کوکی‌های دیگر را نیز اینجا پاک کنید
            return logout_response
        else:
            # Handle unsuccessful logout response
            return HttpResponse("Logout failed. Please try again.", status=400)
    except Exception as e:
        # Handle network error
        print(f"Logout Error: {e}")
        return HttpResponse("An error occurred while logging out. Please try again later.", status=500)
