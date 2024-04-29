#!bin/bash

set -o allexport
source "env/development.env"
set +o allexport

python manage.py -db True

flask db upgrade

# use following commands for create migrations

# bash run_with_env.sh env/development.env flask db init
# bash run_with_env.sh env/development.env flask db migrate -m "intial"
# bash run_with_env.sh env/development.env flask db upgrade