#!/bin/bash
# Entrypoint script for production
# This script runs migrations and starts the server

set -e

echo "🚀 Starting production deployment..."

# Wait for database to be ready
echo "⏳ Waiting for database..."
until python manage.py dbshell -c "SELECT 1" > /dev/null 2>&1; do
  echo "⏳ Database not ready, waiting 2 seconds..."
  sleep 2
done

echo "✅ Database is ready!"

# Run migrations
echo "🔄 Running migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Setup complete! Starting server..."

# Start Gunicorn
exec gunicorn ehit_backend.wsgi:application \
    --bind 0.0.0.0:3030 \
    --workers 3 \
    --timeout 30 \
    --access-logfile - \
    --error-logfile -

