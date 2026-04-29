#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations if database is configured
if [[ $POSTGRES_DB ]]; then
  python manage.py migrate --noinput
fi
