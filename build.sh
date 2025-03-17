#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt
python manage.py shell -c "from django.conf import settings; print('BASE_DIR:', settings.BASE_DIR)"

mkdir -p /opt/render/project/src/data_tracker/staticfiles/

# Convert static asset files
# python manage.py collectstatic --noinput

# Apply any outstanding database migrations
python manage.py migrate