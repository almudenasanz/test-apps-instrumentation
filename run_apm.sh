#!/bin/bash

# This script exports environment variables from .apm.env and then runs
# the Python application with the Elastic APM agent.

# Set the path to the .env file
ENV_FILE=".apm.env"

# Check if the .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Environment file not found at '$ENV_FILE'"
    exit 1
fi

# Export the environment variables from the file
# This command reads the file, ignores lines starting with #, and exports the variables.
export $(grep -v '^#' "$ENV_FILE" | xargs)

echo "Environment variables from '$ENV_FILE' have been exported."
echo "Starting the Flask APM application..."

# Run the application
python3 app_apm.py
