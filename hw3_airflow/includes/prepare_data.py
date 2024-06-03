import os
import pickle
from io import BytesIO
from typing import List

import pandas as pd
import requests
from sklearn.feature_extraction import DictVectorizer


def fetch_data(year=2023, month=3):
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"
    r = requests.get(url)
    if r.ok:
        df = pd.read_parquet(BytesIO(r.content))
    else:
        raise Exception(r.text)

    print(f"The number of rows in the original data is {df.shape[0]}")
    return df


def prepare_dataframe(year: int = 2023, month: int = 3):
    df = fetch_data(year, month)
    df["duration"] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].astype(str)
    print(f"The number of rows in the processed data is {df.shape[0]}")

    return df


def prepare_training_data(
    fname: str,
    dv: DictVectorizer = None,
    features: List[str] = ["PULocationID", "DOLocationID"],
    target: str = "duration",
):
    df = pd.read_parquet(fname)
    dicts = df[features].to_dict(orient="records")

    if dv is None:
        # Training data, fit and transform
        dv = DictVectorizer()
        X = dv.fit_transform(dicts)
    else:
        # Testing data, just transform
        X = dv.transform(dicts)
    y = df[target].values

    return X, y, dv
