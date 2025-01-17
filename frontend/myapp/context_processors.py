import requests
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

def user_info_processor(request):
    access_token = request.COOKIES.get('access_token')
    
    if not access_token:
        if not request.user or isinstance(request.user, AnonymousUser):
            return {'user_info': None}
        return {'user_info': None}
    
    user_info_url = f"{settings.BACKEND_URL}/api/customers/me/"
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(user_info_url, headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                'user_info': {
                    'username': user_data.get('username'),
                }
            }
        else:
            print(f"API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error fetching user info: {e}")
    
    return {'user_info': None}
