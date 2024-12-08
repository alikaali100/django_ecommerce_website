import django
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')

def pytest_configure():
    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:'
                }
            },
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'core',
                'customers',
                'orders',
                'product',
            ],
            SECRET_KEY='dummy-key-for-tests'
        )
        django.setup()
