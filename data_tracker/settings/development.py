from data_tracker.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'katext.com']  # Add any other necessary hosts

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': env('DB_NAME',  default='Text'),  # Use environment variable for DB name, with default 'katext'
        'ENFORCE_SCHEMA': True,  # Ensures schema enforcement on MongoDB
        'CLIENT': {
            'host': env('DB_HOST'),  # Use environment variable for MongoDB connection string
        }
    }
}
