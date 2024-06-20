#!/bin/bash
# Fetch the NYC yellow cab trip data for Jan and Feb of 2023

# For training
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-01.parquet

# For "live" performance
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2024-03.parquet
