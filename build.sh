#!/usr/bin/env bash

set -euo pipefail

# Install Python dependencies
python -m pip install -r requirements.txt

# Collect CSS and other static assets
python manage.py collectstatic --noinput

# Apply Django database migrations
python manage.py migrate --noinput

# Populate the catalogue only if the database is empty
python manage.py shell -c "from django.core.management import call_command; from perfumes.models import Perfume; call_command('import_perfumes') if not Perfume.objects.exists() else print('Catalogue already populated')"