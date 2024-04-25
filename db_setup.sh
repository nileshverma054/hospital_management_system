#!bin/bash

# This script will setup database

set -o allexport
source "env/development.env"
set +o allexport

export FLASK_APP="manage.py"

python manage.py

flask db init

flask db migrate -m "initial migration"

flask db upgrade
