from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse

def products_view(request):
    try:
        # دریافت محصولات
        response = requests.get('http://localhost:8000/api/products/')
        if response.status_code == 200:
            products = response.json()
        else:
            products = []
        
        # دریافت دسته‌بندی‌ها
        category_response = requests.get('http://127.0.0.1:8000/api/categories/')
        if category_response.status_code == 200:
            categories = category_response.json()
        else:
            categories = []
    except requests.exceptions.RequestException as e:
        products = []
        categories = []
        print(f"Error fetching data: {e}")

    return render(request, 'products.html', {
        'products': products,
        'categories': categories
    })


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

from django.http import Http404
def product_detail_view(request, product_id):
    # API URLs
    product_api_url = f"http://localhost:8000/api/products/{product_id}/"
    features_api_url = f"http://localhost:8000/api/product-features/"

    try:
        # Fetch product details
        product_response = requests.get(product_api_url)
        product_response.raise_for_status()
        product = product_response.json()

        # Fetch all features
        features_response = requests.get(features_api_url)
        features_response.raise_for_status()
        all_features = features_response.json()

        # Filter features for the current product
        product_features = [feature for feature in all_features if feature['product'] == product_id]

        # Add features to product dictionary
        product['features'] = product_features

    except requests.exceptions.RequestException:
        raise Http404("Product or features not found")

    return render(request, 'product_detail.html', {'product': product})

def search_products_view(request):
    query = request.GET.get('q', '')  
    try:
        response = requests.get(f'http://localhost:8000/api/products/?search={query}')
        if response.status_code == 200:
            products = response.json()
        else:
            products = []
    except requests.exceptions.RequestException as e:
        products = []
        print(f"Error fetching search results: {e}")

    return render(request, 'products.html', {'products': products})


def cart_view(request):
    # URL API
    api_url = "http://localhost:8000/api/cart/"

    # گرفتن توکن از کوکی
    token = request.COOKIES.get('access_token')

    # تنظیم هدر درخواست
    headers = {
        "Authorization": f"Bearer {token}"
    } if token else {}

    # ارسال درخواست GET به API
    response = requests.get(api_url, headers=headers)

    # تبدیل پاسخ به JSON
    if response.status_code == 200:
        data = response.json()
    else:
        data = {"cart_items": [], "total_price": 0.0}

    # ارسال داده‌ها به قالب
    return render(request, 'cart.html', {
        'cart_items': data.get('cart_items', []),
        'total_price': data.get('total_price', 0.0),
    })
def remove_from_cart_view(request):
    if request.method == "POST":
        # دریافت اطلاعات محصول
        product_id = request.POST.get('product_id')
        
        # آدرس API
        api_url = "http://localhost:8000/api/cart/remove/"
        
        # گرفتن توکن از کوکی
        token = request.COOKIES.get('access_token')
        
        # تنظیم هدر درخواست
        headers = {
            "Authorization": f"Bearer {token}"
        } if token else {}

        # داده‌هایی که باید به API ارسال شود
        data = {
            "product": product_id
        }

        # ارسال درخواست DELETE به API
        response = requests.delete(api_url, json=data, headers=headers)

        # مدیریت پاسخ
        if response.status_code == 200:
            # موفقیت‌آمیز: بازگشت به سبد خرید
            return redirect('cart')
        else:
            # خطا: نمایش پیام مناسب
            return redirect('cart', {"error_message": "خطا در حذف محصول."})
        
def checkout_view(request):
    return render(request,'checkout.html')

def userpanel_view(request):
    api_url = "http://localhost:8000/api/cart/orders/"
    token = request.COOKIES.get('access_token')
    headers = {
        "Authorization": f"Bearer {token}"
    } if token else {}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        user_orders = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders: {e}")
        user_orders = []

    # Transform data for rendering if needed
    formatted_orders = [
        {
            'id': order['id'],
            'date': order['created_at'],
            'total': order['total_amount'],
            'status': order['status'],
        }
        for order in user_orders
    ]

    context = {
        'user_info': {
            'name': 'نام کاربر',  # Replace with real data
            'email': 'ایمیل کاربر',
            'phone': 'شماره تلفن کاربر',
        },
        'user_orders': formatted_orders,
    }

    return render(request, 'user_panel.html', context)
