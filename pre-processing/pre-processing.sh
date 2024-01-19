#!/usr/bin/bash
# file name: pre-processing.sh

# Activate Python virtual environment
source /home/ubuntu/venv/bin/activate
echo "Env activated"
#echo $1

# Run Python script with provided argument
/home/ubuntu/venv/bin/python /home/ubuntu/Project7008/code/pre-processing/pre-processing.py $1

echo "Execution complete"

# Deactivate Python virtual environment
deactivate
