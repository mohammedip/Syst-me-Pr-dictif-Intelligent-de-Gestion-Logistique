#!/bin/bash

# Initialize the database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --firstname Zakaria \
    --lastname Zakaria \
    --role Admin \
    --email zakaria@example.com \
    --password Mimo20032016

# Start Airflow standalone
exec airflow standalone