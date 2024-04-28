#!/bin/bash

set -o allexport
source "env/development.env"
set +o allexport

flask db upgrade

python app.py
