#!/usr/bin/bash
# file name: EDA_test.sh

# Activate Python virtual environment
source /home/ubuntu/venv/bin/activate
echo "Env activated"

# Run Python script with provided argument
/home/ubuntu/venv/bin/python /home/ubuntu/Project7008/code/EDA/EDA_test/EDA_test.py $1

echo "Execution complete"

# Deactivate Python virtual environment
deactivate
