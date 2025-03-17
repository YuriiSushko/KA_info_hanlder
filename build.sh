#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Debug: Print Base Directory
python manage.py shell -c "from django.conf import settings; print('BASE_DIR:', settings.BASE_DIR)"

# Debug: Create staticfiles directory explicitly
mkdir -p /opt/render/project/src/staticfiles
echo "✅ Created staticfiles directory"

# Run collectstatic and check for errors
echo "Running collectstatic..."
python manage.py collectstatic --noinput || { echo "❌ collectstatic failed"; exit 1; }
echo "✅ Collected static files"

# Apply database migrations
python manage.py migrate || { echo "❌ Migrations failed"; exit 1; }
echo "✅ Migrations applied"
