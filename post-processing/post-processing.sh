#!/usr/bin/bash
# file name: post-processing.sh

# Activate Python virtual environment
source /home/ubuntu/venv/bin/activate
echo "Env activated"

# Run Python script with provided argument
/home/ubuntu/venv/bin/python /home/ubuntu/Project7008/code/post-processing/post-processing.py $1

echo "Execution complete"

# Deactivate Python virtual environment
deactivate
