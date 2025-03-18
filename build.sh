#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Build script started"
source .venv/bin/activate
echo "Using venv"

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

mkdir -p /opt/render/project/src/data_tracker/staticfiles/
echo "✅ Created staticfiles directory"

chmod -R 777 /opt/render/project/src/data_tracker/staticfiles/
echo "✅ Granted permissions to staticfiles directory"

# Debug: Check for existing static files
echo "Contents of static directory:"
ls /opt/render/project/src/data_tracker/static/

# Run collectstatic and check for errors
echo "Running collectstatic..."
python manage.py collectstatic --noinput || { echo "❌ collectstatic failed"; exit 1; }
echo "✅ Collected static files"

# Apply database migrations
python manage.py migrate || { echo "❌ Migrations failed"; exit 1; }
echo "✅ Migrations applied"
