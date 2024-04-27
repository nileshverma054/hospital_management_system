#!/bin/bash

set -e

# Wait for the database to be available
until nmap hospital_management_system_mysql --send-eth --max-retries 10
do
  echo "Waiting for database connection..."
  sleep 3
done

# Run the app
python app.py