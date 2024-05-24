#!/bin/bash
echo "Beggining HW 2"

# Q1
mlflow --version

echo "Fetching Geen Taxi NYC data for Jan-March 2023"
cd data
bash fetch_data.sh
cd ..

# Q2
echo "Preprocessing data"
preprocess_cmd="python preprocess_data.py --raw_data_path ./data --dest_path ./output"
echo $preprocess_cmd
$($preprocess_cmd)

nfiles=$(ls ./output | wc -l)
echo "There are ${nfiles} files created"

# Q3
echo "Training"
train_cmd="python train.py"
echo $train_cmd
$($train_cmd)

echo "Launching MLflow UI to check the logging"
echo "To continue, interrupt"
mlflow ui --port 7766

echo "The value of the  \`min_samples_split\` parameter is 2"

# Q4
echo "Launching the tracking server locally (in the background)"

tracking_server_cmd="mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root artifacts --port 7766"
echo ${tracking_server_cmd}
$($tracking_server_cmd > server.log 2>&1 &)


# Q5
echo "Starting hyper-parameter tuning"
hpo_cmd="python ./hpo.py"
echo ${hpo_cmd}
$($hpo_cmd)

echo "The best RMSE on validation set is 5.335"

# Q6

echo "Registering the best model"

register_cmd="python ./register_model.py"
echo ${register_cmd}
$($register_cmd)

fg