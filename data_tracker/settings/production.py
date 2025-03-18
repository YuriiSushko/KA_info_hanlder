from data_tracker.settings.base import *
import environ

# Read the .env file for environment variables
env = environ.Env()
environ.Env.read_env()

DEBUG = True
ALLOWED_HOSTS = ['ka-info-hanlder.onrender.com']
BASE_DIR = Path(__file__).resolve().parent.parent

# Template settings for production (since you're only using templates in the 'courses' app)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # The template backend to use
        'DIRS': [],  # No global templates folder
        'APP_DIRS': True,  # Enable app-level templates searching
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

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

# Security settings for production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS
