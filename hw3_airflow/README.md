This is a simple version of the same pipeline as in hw3. You will have to install `Airflow`. We follow almost exactly the approach from [the Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/cohorts/2022/week_3_data_warehouse/airflow) from a couple of years ago. You can find the `Dockerfile` and `docker-compose` file here. You will also need to create your own `.env` file, as shown [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2022/week_3_data_warehouse/airflow/.env_example).
After that, you should be able to run

```{bash}
docker build .
```
To get everything running do
```{bash}
docker compose up -d

```

Now you should have `Airflow` running on `localhost:8080` and `MLflow` on `localhost:5012`.

To answer the questions, simply execute the `hw03_dag`.
