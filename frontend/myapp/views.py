from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.core.paginator import Paginator
import json

def products_view(request):
    try:
        response = requests.get('http://localhost:8000/api/products/')
        if response.status_code == 200:
            products = response.json()
        else:
            products = []
        category_response = requests.get('http://127.0.0.1:8000/api/categories/')
        if category_response.status_code == 200:
            categories = category_response.json()
        else:
            categories = []
    except requests.exceptions.RequestException as e:
        products = []
        categories = []
        print(f"Error fetching data: {e}")
        
    paginator = Paginator(products, 4)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'products.html', {
        'page_obj': page_obj,   
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

        response = requests.post(f"{API_BASE_URL}/api/customers/register/", data={
            "username": username,
            "email": email,
            "password": password
        })

        if response.status_code == 201:
            return redirect('/login/')
        else:
            context = {"error": "Registration failed, please try again."}
            return render(request, "register.html", context)

    return render(request, "register.html")
    
API_BASE_URL = "http://127.0.0.1:8000" 

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        response = requests.post(f"{API_BASE_URL}/api/customers/login/", data={"email": email, "password": password})

        if response.status_code == 200:
            return render(request, "login.html")
        else:
            # Handle error
            context = {"error": "Invalid email or password"}
            return render(request, "login.html", context)
    return render(request, "login.html")

from django.http import HttpResponse

def logout_view(request):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/customers/logout/",
            cookies=request.COOKIES, 
        )
        
        if response.status_code == 200:
            logout_response = redirect("login")  
            logout_response.delete_cookie("access_token")  
            return logout_response
        else:
            return HttpResponse("Logout failed. Please try again.", status=400)
    except Exception as e:
        # Handle network error
        print(f"Logout Error: {e}")
        return HttpResponse("An error occurred while logging out. Please try again later.", status=500)

from django.http import Http404
def product_detail_view(request, product_id):
    product_api_url = f"http://localhost:8000/api/products/{product_id}/"
    features_api_url = f"http://localhost:8000/api/product-features/"

    try:
        product_response = requests.get(product_api_url)
        product_response.raise_for_status()
        product = product_response.json()

        features_response = requests.get(features_api_url)
        features_response.raise_for_status()
        all_features = features_response.json()

        product_features = [feature for feature in all_features if feature['product'] == product_id]

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

    # اعمال صفحه‌بندی
    paginator = Paginator(products, 10)  # نمایش 10 محصول در هر صفحه
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products.html', {'page_obj': page_obj, 'query': query})


def cart_view(request):
    cart_items = []
    total_price = 0

    # بررسی وجود اکسس توکن
    token = request.COOKIES.get('access_token')

    if token:
        # اگر اکسس توکن وجود داشته باشد، اطلاعات سبد خرید را از API دریافت می‌کنیم
        api_url = "http://localhost:8000/api/cart/"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            cart_items = data.get('cart_items', [])
            total_price = data.get('total_price', 0)
        else:
            # اگر مشکلی در ارتباط با API وجود داشت
            cart_items = []
            total_price = 0
    else:
        # اگر اکسس توکن وجود نداشت، اطلاعات سبد خرید از کوکی خوانده می‌شود
        guest_cart_cookie = request.COOKIES.get('guest_cart')
        guest_cart = []

        if guest_cart_cookie:
            try:
                guest_cart = json.loads(guest_cart_cookie)
            except json.JSONDecodeError:
                guest_cart = []

        # آدرس API محصولات
        products_api_url = "http://localhost:8000/api/products/"
        products_response = requests.get(products_api_url)

        if products_response.status_code == 200:
            products_data = products_response.json()
            products_dict = {str(product["id"]): product for product in products_data}

            # پردازش اطلاعات سبد خرید از کوکی
            for item in guest_cart:
                product_id = str(item["product"])
                quantity = item["quantity"]

                if product_id in products_dict:
                    product = products_dict[product_id]
                    discounted_price = product.get("discounted_price", product["price"])
                    total_price += discounted_price * quantity
                    cart_items.append({
                        "product_id": product["id"],
                        "product_name": product["name"],
                        "product_price": product["price"],
                        "discounted_price": discounted_price,
                        "quantity": quantity,
                    })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })
# def sync_cart(request):
#     if not request.user.is_authenticated:
#         return JsonResponse({'error': 'User not authenticated'}, status=401)

#     # گرفتن توکن از هدر درخواست
#     token = request.headers.get('Authorization', None)
#     if not token:
#         return JsonResponse({'error': 'Access token is required'}, status=400)

#     # خواندن کوکی
#     guest_cart_cookie = request.COOKIES.get('guest_cart', '[]')
#     guest_cart = json.loads(guest_cart_cookie)

#     # دریافت کارت از API
#     try:
#         response = requests.get(
#             "http://localhost:8000/api/cart/",
#             headers={'Authorization': token}
#         )
#         if response.status_code != 200:
#             return JsonResponse({'error': 'Failed to fetch cart from API'}, status=response.status_code)

#         user_cart = response.json()
#         user_cart_dict = {str(item['product']): item['quantity'] for item in user_cart}

#         # حالت 1: اقلامی که فقط در کوکی هستند
#         for item in guest_cart:
#             product_id = str(item['product'])
#             quantity = item['quantity']
#             if product_id not in user_cart_dict:
#                 # اضافه کردن به دیتابیس
#                 data = {
#                     'product': product_id,
#                     'quantity': quantity
#                 }
#                 add_response = requests.post(
#                     "http://localhost:8000/api/cart/add/",
#                     headers={'Authorization': token, 'Content-Type': 'application/json'},
#                     data=json.dumps(data)
#                 )
#                 if add_response.status_code != 200:
#                     return JsonResponse({'error': 'Failed to add item to database'}, status=add_response.status_code)

#         # حالت 2: اقلامی که فقط در دیتابیس هستند
#         for product_id, quantity in user_cart_dict.items():
#             if not any(item['product'] == int(product_id) for item in guest_cart):
#                 # اضافه کردن به کوکی
#                 guest_cart.append({'product': int(product_id), 'quantity': quantity})

#         # حالت 3: اقلامی که در هر دو هستند ولی تعداد متفاوت است
#         for item in guest_cart:
#             product_id = str(item['product'])
#             quantity = item['quantity']
#             if product_id in user_cart_dict and user_cart_dict[product_id] != quantity:
#                 # به‌روزرسانی تعداد در دیتابیس
#                 data = {
#                     'product': product_id,
#                     'quantity': quantity
#                 }
#                 update_response = requests.post(
#                     "http://localhost:8000/api/cart/add/",
#                     headers={'Authorization': token, 'Content-Type': 'application/json'},
#                     data=json.dumps(data)
#                 )
#                 if update_response.status_code != 200:
#                     return JsonResponse({'error': 'Failed to update item in database'}, status=update_response.status_code)

#         # به‌روزرسانی کوکی
#         response = JsonResponse({'success': 'Cart synchronized successfully'})
#         response.set_cookie('guest_cart', json.dumps(guest_cart), max_age=7 * 24 * 60 * 60)
#         return response

#     except requests.RequestException as e:
#         return JsonResponse({'error': f'Network error: {str(e)}'}, status=500)
    
def remove_from_cart_view(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        api_url = "http://localhost:8000/api/cart/remove/"

        token = request.COOKIES.get('access_token')
        headers = {
            "Authorization": f"Bearer {token}"
        } if token else {}

        data = {
            "product": product_id
        }
        response = requests.delete(api_url, json=data, headers=headers)

        if response.status_code == 200:
            return redirect('cart')
        else:
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
        response.raise_for_status()  
        user_orders = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders: {e}")
        user_orders = []

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
        'user_orders': formatted_orders,
    }

    return render(request, 'user_panel.html', context)
