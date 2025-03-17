#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Print Base Directory (for debugging)
python manage.py shell -c "from django.conf import settings; print('BASE_DIR:', settings.BASE_DIR)"

# Manually create the staticfiles directory (Render might not create it automatically)
mkdir -p /opt/render/project/src/staticfiles
echo "Created staticfiles directory"

# Collect static files
python manage.py collectstatic --noinput
echo "Collected static files"

# Apply migrations
python manage.py migrate
echo "Applied migrations"
