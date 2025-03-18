from data_tracker.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'ka-info-handler.com', 'ka-info-handler.onrender.com']
BASE_DIR = Path(__file__).resolve().parent.parent

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

# # Configure static files for production (for example, using AWS S3)

# Security settings for production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS

# # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
# Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
# and renames the files with unique names for each version to support long-term caching

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
