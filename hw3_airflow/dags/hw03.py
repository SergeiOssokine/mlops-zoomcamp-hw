import os
import pickle
import sys
from datetime import datetime

import h5py
import mlflow
import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from scipy.sparse import csr_matrix
from sklearn.linear_model import LinearRegression

dr = os.path.dirname(os.path.dirname(__file__))

sys.path.append(os.path.abspath(dr))

from includes.prepare_data import prepare_dataframe, prepare_training_data
from includes.utils import load_training_dataset, serialize_training_dataset


def load_data(ti=None, year=2023, month=3):
    df = prepare_dataframe()
    pth = f"data/raw_data_{year}-{month}.parquet"
    df.to_parquet(pth)
    ti.xcom_push(key="raw_data_path", value=pth)


def generate_training_data(ti=None):
    raw_data_path = ti.xcom_pull(key="raw_data_path", task_ids="load_data_task")
    X, y, dv = prepare_training_data(raw_data_path)
    # Dump the vectorizer
    vec_path = "models/dict_vectorizer.b"
    with open(vec_path, "wb") as f_out:
        pickle.dump(dv, f_out)
    ti.xcom_push(key="vec_path", value=vec_path)
    # Dump the training data
    data_path = "data/training_data.h5"

    serialize_training_dataset(X, y, data_path)
    ti.xcom_push(key="data_path", value=data_path)


def train_model(ti=None, experiment_name="nyc-taxi-analysis"):
    vec_path = ti.xcom_pull(key="vec_path", task_ids="generate_training_data_task")
    data_path = ti.xcom_pull(key="data_path", task_ids="generate_training_data_task")

    X, y = load_training_dataset(data_path)
    mlflow.set_tracking_uri("http://mlflow:5012")
    mlflow.set_experiment(experiment_name)
    mlflow.sklearn.autolog()
    with mlflow.start_run():
        lr = LinearRegression()
        lr.fit(X, y)
        print(f"The intercept for the fitted model is {lr.intercept_}")
        mlflow.log_artifact(vec_path, artifact_path="preprocessor")


# Define the DAG
with DAG(
    "hw03_dag",
    start_date=datetime(2024, 6, 3),
    default_args={
        "owner": "airflow",
    },
    schedule_interval="@daily",  # Adjust to your needs
    catchup=False,
) as dag:

    # Define the task to read the DataFrame
    load_data_task = PythonOperator(
        task_id="load_data_task",
        python_callable=load_data,
        provide_context=True,
    )

    # Define the task to perform the operation on the DataFrame
    generate_training_data_task = PythonOperator(
        task_id="generate_training_data_task",
        python_callable=generate_training_data,
        provide_context=True,
    )

    train_model_task = PythonOperator(
        task_id="train_model_task",
        python_callable=train_model,
        provide_context=True,
    )

    load_data_task >> generate_training_data_task >> train_model_task
