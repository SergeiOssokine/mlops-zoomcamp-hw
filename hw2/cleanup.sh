#!/bin/bash
# Clean up everything created by run_homework.sh
rm artifacts -rf
rm mlruns -rf
rm output -rf
rm mlflow.db
rm server.log

cd data
rm *parquet*
cd ..
