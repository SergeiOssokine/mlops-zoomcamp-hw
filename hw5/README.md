This folder contains scripts to solve homework for week 5 of the [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) for the 2024 cohort.
For the actual questions, look [here](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/cohorts/2024/05-monitoring/homework.md)

## Getting started

### Set up the env
Before doing anything we need to set up the environment, which will make our lives easier later.  There are many ways to do this with the provided `requirements.txt`. A very _fast_ way is the following.


Install [`uv`](https://github.com/astral-sh/uv) which is an extremely fast package manager:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Now create a virtual environment and activate it
```bash
uv venv .hw5_env
source .hw5_env/bin/activate
```
Finally install dependencies

```bash
uv pip install -r requirements.txt
```

### Get the model ready
We need a model from the videos in order to do this homework. For completness we have a script that reproduces it. First fetch the data via

```
cd data && bash fetch_data.sh && cd ../
```

To train the model we still use `mlflow` for logging. Launch the `MLflow` server 
```bash
PORT=5012
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root artifacts --port ${PORT}
```

Then run the training script 

```bash
python train_model.py
```

This will generate `models/lin_reg.bin`, log the experiment and create reference data we will need in `data/reference.parquet`. 

### Build the docker image
To actually store and visualize the monitoring data we will need a `PostgreSQL` and `Grafana` servers running. For this we have a `docker-compose` file. Do

```{bash}
docker compose up -d --build
```

You will need to set the environmental variable `HW5_PASS` so that all the scripts can connect to the database (of course you can change it easily in `docker-compose.yml`):

```bash
export HW5_PASS="mlops4thewin"
```

Now to answer HW questions, one can just run 

```bash
bash run_homework.sh
```

You can inspect the database by pointing your browser to `localhost:8080`:

- System: PostgreSQL
- Username: postgres
- Password: mlops4thewin
- Database: test

The `Grafana` dashboard can be accessed at `localhost:3000`, with default username and password (`admin` for both).