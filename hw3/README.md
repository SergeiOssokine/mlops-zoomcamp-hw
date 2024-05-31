This folder contains scripts to solve homework for week 3 of the [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) for the 2024 cohort.
For the actual questions, look [here](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/cohorts/2024/03-orchestration/homework.md)

You will need both `docker` and `docker-compose` to do this. Don't forget to [add yourself](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user) to the `docker` group so that you don't have to run things with `sudo`.

**NOTE: the instructions here are only for running homework and only on the `localhost`. These are explicitly NOT secure for anything else.**

To launch both `mage` and `mlflow` with all the pipelines and everything ready, simply do

```bash
./scripts/start.sh
```

This will launch `docker-compose` in detached mode. When you are done with everything want to stop it, do `docker-compose down`.

Once you have launched things, `mage` is available at `localhost:6789` and `mflow` at `localhost:5012`. You can now answer all the questions just by using the UI.

Alternatively, you can simply run the following script (note that it may take a while since it has to wait for pipeline runs to finish).


```bash
bash run_homework.sh
```
