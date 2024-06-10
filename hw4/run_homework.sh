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

echo "Beginning HW 4"


# Q1
header "Question 1"
echo "Running the starter notebook, please wait"
jupyter nbconvert  --log-level 50 --execute --stdout --to markdown --no-input starter.ipynb   | grep 'deviation' 



# Q2
header "Question 2"
fsize=$(du -h predictions/prediction_2023_3.parquet | cut -f 1)
echo "The size of the prediction file for March 2023 is ${fsize}"

# Q3
header "Question 3"
echo "To convert notebook to a script you can run nbconvert --to script starter.ipynb"

# Q4
header "Question 4"
hash=$(cat Pipfile.lock | jq '.default."scikit-learn".hashes[0]')
echo "The hash for the first dependency of scikit-learn is ${hash}"

# Q5
header "Question 5"
echo "Running our own model in local environment"
echo "Stats for predictions for April 2023"

cmd="python predict.py --year 2023 --month 4"
echo $cmd
$cmd

# Q5
header "Question 6"
echo "Running the provided model in a Docker container"
echo "Stats for predictions for May 2023"
cmd="sudo docker run --rm hw4_predict:latest --year 2023 --month 5"
echo $cmd
$cmd
