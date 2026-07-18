#!/bin/bash

# 1. Activate the Conda environment
# Using the standard conda activation initialization logic
source $(conda info --base)/etc/profile.d/conda.sh
conda activate quantium_env

# 2. Execute the test suite using pytest
pytest test_app.py

# 3. Capture the exit status code of pytest
TEST_STATUS=$?

# 4. Return exit code 0 if all tests passed, or 1 if something went wrong
if [ $TEST_STATUS -eq 0 ]; then
    echo "Tests passed successfully!"
    exit 0
else
    echo "Tests failed. Please check the test suite outputs."
    exit 1
fi