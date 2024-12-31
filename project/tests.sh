#!/bin/bash

# Fail the script on the first error
set -e

# Install the dependencies
echo "Installing dependencies..."
pip install -r ./project/requirements.txt

# Run all test cases
echo "Running tests..."
pytest ./project/test_ETL.py

echo "All tests passed!"