from data_tracker.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'ka-info-handler.com', 'ka-info-handler.onrender.com']
BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(BASE_DIR)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# # Configure static files for production (for example, using AWS S3)
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# Security settings for production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS

STATIC_URL = '/static/'

# Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
# and renames the files with unique names for each version to support long-term caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
