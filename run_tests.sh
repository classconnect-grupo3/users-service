#!/bin/bash
set -e  # Exit immediately if a command exits with non-zero status

# Ensure we clean up containers even if script is interrupted
function cleanup {
  echo "Cleaning up containers..."
  docker-compose -f docker-compose.test.yml down -v
}

# Register the cleanup function to be called on the EXIT signal
trap cleanup EXIT

# Run the tests
echo "Starting test containers..."
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from app-test

# The cleanup function will be called automatically when the script exits 