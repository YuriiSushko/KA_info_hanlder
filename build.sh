#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Build script started"

export DISABLE_COLLECTSTATIC=1

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# mkdir -p /opt/render/project/src/data_tracker/staticfiles/
# echo "✅ Created staticfiles directory"

# chmod -R 777 /opt/render/project/src/data_tracker/staticfiles/
# echo "✅ Granted permissions to staticfiles directory"

# # source .venv/bin/activate
# # echo "Using venv"

# # Debug: Check for existing static files
# echo "Contents of static directory:"
# ls /opt/render/project/src/data_tracker/staticfiles/

# # Run collectstatic and check for errors
# echo "Running collectstatic..."
# python manage.py collectstatic --noinput --verbosity 2 || { echo "❌ collectstatic failed"; exit 1; }
# echo "✅ Collected static files"

# # Apply database migrations
# echo "🚀 Applying migratrions"
# python manage.py migrate || { echo "❌ Migrations failed"; exit 1; }
# echo "✅ Migrations applied"
# Skip collectstatic if DISABLE_COLLECTSTATIC is set
if [ "$DISABLE_COLLECTSTATIC" != "1" ]; then
  echo "Running collectstatic..."
  python manage.py collectstatic --noinput --verbosity 2 || { echo "❌ collectstatic failed"; exit 1; }
  echo "✅ Collected static files"
else
  echo "Skipping collectstatic due to DISABLE_COLLECTSTATIC=1"
fi


echo "✅ Finished"