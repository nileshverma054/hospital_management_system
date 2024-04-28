#!/bin/bash

set -e

# This will wait unintil database is ready
python manage.py

echo "DB_MIGRATIONS is ${DB_MIGRATIONS}"
# Run database migrations only if DB_MIGRATIONS is set to True
if [[ "${DB_MIGRATIONS}" == "true" ]]; then
    echo "Running database migrations.."
    flask db upgrade
fi

# Run application
python app.py
