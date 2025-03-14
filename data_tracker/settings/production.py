from data_tracker.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'katext.com','katext.onrender.com'] 

# Configure static files for production (for example, using AWS S3)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Security settings for production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS
