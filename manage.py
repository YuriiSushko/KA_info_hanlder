#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ

def main():
    """Run administrative tasks."""
    # Set the default settings module to 'development' for local development
    env = environ.Env()
    environ.Env.read_env(os.path.join(os.path.dirname(__file__), '.env'))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', env('DJANGO_SETTINGS_MODULE'))
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
    if len(sys.argv) > 1 and sys.argv[1] in ['makemigrations', 'migrate', 'createsuperuser', 'import_items', 'help']:
        execute_from_command_line(sys.argv)
    else:
        port = os.environ.get('PORT', '8000')  # Use '8000' as default if PORT is not set
        execute_from_command_line(['manage.py', 'runserver', f'0.0.0.0:{port}'])
        

if __name__ == '__main__':
    main()
