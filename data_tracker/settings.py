import os

# Get the settings module from the environment variable
settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'data_tracker.settings.development')

try:
    if settings_module == 'data_tracker.settings.development':
        from data_tracker.settings.development import *  # Import development settings
    elif settings_module == 'data_tracker.settings.production':
        from data_tracker.settings.production import *  # Import production settings
except ImportError as e:
    raise ImportError(f"Settings module {settings_module} could not be imported") from e
