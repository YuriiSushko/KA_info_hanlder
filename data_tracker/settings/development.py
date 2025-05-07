from data_tracker.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'katext.com']  # Add any other necessary hosts

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': env('POSTGRES_NAME'),
    #     'USER': env('POSTGRES_USER'),
    #     'PASSWORD': env('POSTGRES_PASSWORD_DEV'),
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_NAME'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD_PROD'),
        'HOST': env('POSGRES_HOST_EXTERNAL'),
        'PORT': '5432',
    },
    'mongo': {
        'ENGINE': 'djongo',
        'NAME': env('DB_NAME_DEV',  default='DEVELOPMENT'),
        'ENFORCE_SCHEMA': True,
        'CLIENT': {
            'host': env('DB_HOST'),
        }
    }
}

STATIC_URL = 'static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
