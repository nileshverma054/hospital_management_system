#!/bin/bash

set -o allexport
source "env/development.env"
set +o allexport

python run.py

