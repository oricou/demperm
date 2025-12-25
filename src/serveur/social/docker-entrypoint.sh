#!/bin/bash
set -e

echo "🚀 Starting Django application..."

# Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL..."
while ! nc -z ${DB_HOST:-postgres} ${DB_PORT:-5432}; do
  sleep 0.1
done
echo "✅ PostgreSQL is ready!"

# Wait for Redis
echo "⏳ Waiting for Redis..."
while ! nc -z ${REDIS_HOST:-redis} ${REDIS_PORT:-6379}; do
  sleep 0.1
done
echo "✅ Redis is ready!"

# Navigate to api directory
cd /app/api

mkdir -p logs

# Merge conflicting migrations automatically
echo "🔀 Checking for migration conflicts..."
python manage.py makemigrations --merge --noinput || echo "No conflicts to merge"


# Run migrations
echo "📦 Running database migrations..."
python manage.py migrate --noinput

# Initialize domains
echo "🏛️ Initializing political domains..."
python manage.py init_domains || echo "Domains already initialized"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Application ready!"
echo "🌐 Starting server..."

# Execute the command passed to the container
exec "$@"