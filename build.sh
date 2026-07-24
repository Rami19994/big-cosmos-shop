#!/bin/bash
set -e

echo "--- Installing dependencies ---"
pip install -r requirements.txt

echo "--- Collecting static files ---"
python manage.py collectstatic --noinput

echo "--- Running database migrations ---"
python manage.py migrate --noinput

echo "--- Ensuring deployment superuser ---"
python manage.py ensure_superuser

echo "--- Build complete ---"
