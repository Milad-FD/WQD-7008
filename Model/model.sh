#!/usr/bin/bash
# file name: model.sh

# Activate Python virtual environment
source /home/ubuntu/venv/bin/activate
echo "Env activated"

# Run Python script with provided argument
/home/ubuntu/venv/bin/python /home/ubuntu/Project7008/code/Model/model.py $1

echo "Execution complete"

# Deactivate Python virtual environment
deactivate
