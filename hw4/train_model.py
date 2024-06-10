import logging
import pickle
from typing import Dict, List, Union

import mlflow
import pandas as pd
import pandera as pa
import typer
from rich.logging import RichHandler
from rich.traceback import install
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from typing_extensions import Annotated

# Sets up the logger to work with rich
logger = logging.getLogger(__name__)
logger.addHandler(RichHandler(rich_tracebacks=True, markup=True))
logger.setLevel("INFO")
# Setup rich to get nice tracebacks
install()


# Basic pandera validation schema for our data
schema = pa.DataFrameSchema(
    columns={
        "PULocationID": pa.Column(int, coerce=True),
        "DOLocationID": pa.Column(int, coerce=True),
        "duration": pa.Column(float, pa.Check.ge(0.0)),
    }
)


def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Check that the features we care about are present
    and obey some basic sanity checks

    Args:
        df (pd.DataFrame): Raw data

    Returns:
        pd.DataFrame: Validated data
    """
    try:
        validated_df = schema(df)
    except pa.errors.SchemaError as exc:
        logger.error(exc)

        exit(-1)
    return validated_df


def read_dataframe(filename: str) -> pd.DataFrame:
    """Read in the NYC Taxi input data.
    Ensures that the pick-up and drop-off locations
    are stored as strings.

    Args:
        filename (str): Name of file with data

    Returns:
        pd.DataFrame: The data in DataFrame form
    """
    df = pd.read_parquet(filename)

    df["duration"] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    validate_dataframe(df)

    categorical = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].astype(str)
    return df


def prepare_dictionaries(
    df: pd.DataFrame, categorical: List[str] = ["PULocationID", "DOLocationID"]
) -> List[Dict[str, Union[str, float]]]:
    """Perform feature engineering and prepare dicts containing the
    desired features

    Args:
        df (pd.DataFrame): Data

    Returns:
        List[Dict[str, Union[str, float]]]: List of dicts with the features,
                                            each item being a dict with records
    """
    dicts = df[categorical].to_dict(orient="records")
    return dicts


def main(
    tracking_uri: Annotated[
        str, typer.Option(help="The MLFlow tracking URI")
    ] = "http://localhost:5012",
    experiment_name: Annotated[
        str, typer.Option(help="The experiment name to use")
    ] = "nyc-taxi-analysis",
):
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    logger.info("Reading data")
    df_train = read_dataframe("./data/yellow_tripdata_2023-01.parquet")
    df_val = read_dataframe("./data/yellow_tripdata_2023-02.parquet")

    target = "duration"
    y_train = df_train[target].values
    y_val = df_val[target].values

    logger.info("Preprocessing data")
    dict_train = prepare_dictionaries(df_train)
    dict_val = prepare_dictionaries(df_val)

    # Run the training

    with mlflow.start_run():

        lr = LinearRegression()
        dv = DictVectorizer()
        X_train = dv.fit_transform(dict_train)
        X_val = dv.transform(dict_val)
        logger.info("Training model")
        lr.fit(X_train, y_train)

        y_pred = lr.predict(X_val)

        rmse = root_mean_squared_error(y_pred, y_val)

        mlflow.log_metric("rmse", rmse)
        mlflow.sklearn.log_model(lr, artifact_path="artifacts")
        name = "model.bin"
        logger.info(f"Serializing model to {name}")
        with open(name, "wb") as fw:
            pickle.dump([dv, lr], fw)
        logger.info("All done")


if __name__ == "__main__":
    typer.run(main)
