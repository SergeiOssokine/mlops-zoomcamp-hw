This folder contains scripts to solve homework for week 4 of the [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) for the 2024 cohort.
For the actual questions, look [here](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/cohorts/2024/04-deployment/homework.md)

## Getting started
Before doing anything we need to set up the environment, which will make our lives easier later. You can do this just by running `pipenv install`. This will use the info in `Pipfile` and `Pipfile.lock` to install everything you need. Then launch the env via `pipenv shell`.


We need a saved model from Homework 1 in order to do this homework. Since we didn't actually save the model to disk in HW1, we recreate the training process here. First fetch the data via

```
cd data && bash fetch_data.sh && cd ../
```

To train the model we still use `mlflow` for logging. Then run the training script via (assuming you have the tracking sever running on `localhost:5012`)

```
python train_model.py
```

This will generate `model_hw1.bin` and log the experiment. We can use this model for most of the rest of the questions.

To convert our `starter.ipynb` notebooker to a Python script we use `nbconvert` with `--to script`. By default this will create a python file that contains the (commented) prompt tags, like `# In[3]`. To get rid of those, we use `--no-prompt`. We also don't want empty lines or line magics in the output (since the latter won't work). To get rid of those we can use some regexp magic. In the end the full command is

```{bash}
jupyter nbconvert  --to script   --no-prompt --RegexRemovePreprocessor.patterns="['\s*\Z','.*?water*']" starter.ipynb
```

