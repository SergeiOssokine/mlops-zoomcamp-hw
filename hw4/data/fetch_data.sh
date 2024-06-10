#!/bin/bash
# Fetch the NYC yellow cab trip data for Jan and Feb of 2023

for m in {1..2}
do
    wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-0${m}.parquet
done