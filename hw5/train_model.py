import logging

import joblib
import mlflow
import typer
from rich.logging import RichHandler
from rich.traceback import install
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from typing_extensions import Annotated
from utils import read_dataframe

# Sets up the logger to work with rich
logger = logging.getLogger(__name__)
logger.addHandler(RichHandler(rich_tracebacks=True, markup=True))
logger.setLevel("INFO")
# Setup rich to get nice tracebacks
install()


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
    df = read_dataframe("./data/green_tripdata_2022-01.parquet")
    train_data = df[:30000]
    val_data = df[30000:].reindex()
    target = "duration"
    y_train = train_data[target].values
    y_val = val_data[target].values

    # Run the training
    num_features = ["passenger_count", "trip_distance", "fare_amount", "total_amount"]
    cat_features = ["PULocationID", "DOLocationID"]
    with mlflow.start_run():

        lr = LinearRegression()

        logger.info("Training model")
        lr.fit(train_data[num_features + cat_features], y_train)

        y_pred = lr.predict(val_data[num_features + cat_features])

        rmse = root_mean_squared_error(y_pred, y_val)

        mlflow.log_metric("rmse", rmse)
        mlflow.sklearn.log_model(lr, artifact_path="artifacts")
        name = "models/lin_reg.bin"
        logger.info(f"Serializing model to {name}")
        with open(name, "wb") as fw:
            joblib.dump(lr, fw)

    # Serialize the validation dataset
    val_data_name = "data/reference.parquet"
    logger.info(f"Serializing reference data to {val_data_name}")

    val_data["prediction"] = y_pred
    val_data.to_parquet(val_data_name)
    logger.info("All done")


if __name__ == "__main__":
    typer.run(main)
