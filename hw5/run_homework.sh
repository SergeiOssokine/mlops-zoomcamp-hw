#!/bin/bash

# Do all the necessary runs to answer questions for homework 4
# Note that you must have followed the README.md to train the model
# and to build the container!


# Function to print a nicer header
header() {
    echo $1
    printf '=%.0s' {1..80}
    echo
}

echo "Beginning HW 5"


# Q1
header "Question 1"

python -c "import pandas as pd;df=pd.read_parquet('data/green_tripdata_2024-03.parquet');print(f'The number of rows is {df.shape[0]}')"


# Q2
header "Question 2"
echo "We use the ColumnSummaryMetric for the prediction as our extra metric. See monitor_data.py"


# Q3
header "Question 3"
echo "Running the monitoring script for March 2024"
python montior_data.py --data-file ./data/green_tripdata_2024-03.parquet --ref-data-file ./data/reference.parquet

# Q4
header "Question 4"
echo "The new dashboard is inside project_folder/dashboards"




