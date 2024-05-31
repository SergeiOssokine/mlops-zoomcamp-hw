#!/bin/bash

# Do all the necessary runs to answer questions for homework 2
# Note that in Q3 one is required to look to the UI and then
# interrupt to continue

# Function to print a nicer header
header() {
    echo $1
    printf '=%.0s' {1..80}
    echo
}

echo "Beginning HW 2"

# Use a custom port for convenience
PORT=7766

# Q1
header "Question 1"
mlflow --version

echo "Fetching Geen Taxi NYC data for Jan-March 2023"
cd data
bash fetch_data.sh
cd ..

# Q2
header "Question 2"
echo "Preprocessing data"
preprocess_cmd="python preprocess_data.py --raw_data_path ./data --dest_path ./output"
echo $preprocess_cmd
$preprocess_cmd

nfiles=$(ls ./output | wc -l)
echo "There are ${nfiles} files created"

# Q3
header "Question 3"
echo "Training"
train_cmd="python train.py"
echo $train_cmd
$train_cmd

echo "Launching MLflow UI to check the logging"
echo "To continue, interrupt"
mlflow ui --port $PORT

echo "The value of the  \`min_samples_split\` parameter is 2"

# Q4
header "Question 4"
echo "Launching the tracking server locally (in the background)"

tracking_server_cmd="mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root artifacts --port ${PORT}"
echo ${tracking_server_cmd}
$tracking_server_cmd >server.log 2>&1 &
pid=$!
echo "PID is ${pid}"

# Q5
header "Question 5"
echo "Starting hyper-parameter tuning"
hpo_cmd="python hpo.py"
echo $hpo_cmd
$hpo_cmd
echo "Finished!"
echo "Retriving the best model RMSE"
curl -s -X POST "http://localhost:7766/api/2.0/mlflow/runs/search" -H "Content-Type: application/json" -d '{"experiment_ids":["1"], "max_results":1,"order_by":["metrics.rmse"]}' | jq '.runs| .[] | {run_id: .info.run_id, value: .data.metrics[0].value}'

# Q6

header "Question 6"
echo "Checking model performance on held-out test set"
register_cmd="python ./register_model.py"
echo ${register_cmd}
$register_cmd

echo "The top 5 results based on test RMSE were: "
curl -s -X POST "http://localhost:7766/api/2.0/mlflow/runs/search" -H "Content-Type: application/json" -d '{"experiment_ids":["2"], "max_results":5,"order_by":["metrics.test_rmse"]}' | jq '.runs| .[] | {run_id: .info.run_id, value: .data.metrics[] |  select(.key | contains("test_rmse")) .value}'

echo "Verifying that we registered the model with the best test RMSE  via REST API call"

# Get model info
echo "The best model info is"
bmodel=$(curl -s http://localhost:${PORT}/api/2.0/mlflow/registered-models/search | jq '.registered_models[0].latest_versions[0]')
jq <<<${bmodel}
BEST_RUN_ID=$(jq -r '.run_id' <<<${bmodel})

# # Get the test RMSE
echo "The test RMSE of the associated run is"
curl -s http://localhost:${PORT}/api/2.0/mlflow/runs/get?run_id=${BEST_RUN_ID} | jq '.run.data.metrics[] | select(.key | contains("test_rmse")) .value'

echo "All done, when ready interrupt to finish"
wait $pid
