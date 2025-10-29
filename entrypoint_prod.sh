#!/bin/bash
# Entrypoint script for production
# This script runs migrations and starts the server

set -e

echo "🚀 Starting production deployment..."

# Wait for database to be ready using Python
echo "⏳ Waiting for database..."
python << END
import psycopg2
import sys
import time

max_attempts = 30
for attempt in range(max_attempts):
    try:
        conn = psycopg2.connect(
            dbname='ehit_db',
            user='ehit_user',
            password='ehit_password',
            host='db',
            port='5432'
        )
        conn.close()
        print("✅ Database is ready!")
        sys.exit(0)
    except psycopg2.OperationalError:
        if attempt < max_attempts - 1:
            print("⏳ Database not ready, waiting 2 seconds...")
            time.sleep(2)
        else:
            print("❌ Timeout waiting for database after 30 attempts")
            sys.exit(1)

sys.exit(1)
END

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

