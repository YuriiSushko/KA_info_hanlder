from data_tracker.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'ka-info-handler.com', 'ka-info-handler.onrender.com']

# # Configure static files for production (for example, using AWS S3)
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# In production.py
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.NullStorage'


# Security settings for production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS
