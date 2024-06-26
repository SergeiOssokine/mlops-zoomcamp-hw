import os

import pandas as pd
import pytest
from batch import prepare_data

S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")

from datetime import datetime


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


@pytest.fixture
def df_input():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),  # <1 minute
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),  # >1 hour
    ]

    columns = [
        "PULocationID",
        "DOLocationID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]
    df = pd.DataFrame(data, columns=columns)
    return df


def write_to_s3(df_input, year=2024, month=1):
    input_file = f"s3://nyc-duration/test_input_{year:04d}-{month:02d}.parquet"
    options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}
    df_input.to_parquet(
        input_file,
        engine="pyarrow",
        compression=None,
        index=False,
        storage_options=options,
    )


def test_read_from_s3(df_input):
    write_to_s3(df_input)
