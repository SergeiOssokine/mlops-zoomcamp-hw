#!/bin/bash

# Do all the necessary runs to answer questions for homework 3
# Note that in Q3 one is required to look to the UI and then
# interrupt to continue

# Function to print a nicer header
header() {
    echo $1
    printf '=%.0s' {1..80}
    echo
}

echo "Beginning HW 3 MLFLOW version"
echo "Only questions 4 onwards are answered"
# Use a custom port for convenience
MLFLOW_PORT=5012




# Q4
header "Question 4"
python -c "import pandas as pd; df=pd.read_parquet('./data/raw_data_2023-3.parquet');print(f'The number of rows of the processed data is {df.shape[0]}')"


# Q5
header "Question 5"
# Get the run_id from mlflow

run_id=$(curl -s -X POST "http://localhost:${MLFLOW_PORT}/api/2.0/mlflow/runs/search" -H "Content-Type: application/json" -d '{"experiment_ids":["1"],"max_results":1}' | jq -r '.runs[0].info.run_id')

echo "The run ID in mlflow is ${run_id}"

# Now get the model intercept. For this we have to load the model

python get_model_intercept.py --model-uri=${run_id}

# Q6
header "Question 6"
# Extract the model size info

msize=$(curl -s -X GET "http://localhost:${MLFLOW_PORT}/api/2.0/mlflow/runs/get?run_id=${run_id}" | jq -c '.run.data.tags | .[] | select(.key | contains("history")) .value | fromjson | .[0].model_size_bytes')
echo "The size of the model is ${msize} bytes"
