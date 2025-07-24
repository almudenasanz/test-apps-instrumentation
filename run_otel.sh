#!/bin/bash

# This script exports environment variables from .otel.env and then runs
# the OpenTelemetry-instrumented Python application.

# Set the path to the .env file
ENV_FILE=".otel.env"

# Check if the .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Environment file not found at '$ENV_FILE'"
    exit 1
fi

# Export the environment variables from the file
# This command reads the file, ignores lines starting with #, and exports the variables.
export $(grep -v '^#' "$ENV_FILE" | xargs)

echo "Environment variables from '$ENV_FILE' have been exported."
echo "Starting the OpenTelemetry application..."

# Run the application with OpenTelemetry instrumentation
opentelemetry-instrument python3 app_otel.py
