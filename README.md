# Simple MLOps with Airflow, MLFlow, and Pycaret 

## 1. Introduction

A toy project to help me learn MLOps. What does it do?
* create_db: Create a simple MySQL database from a single data source (csv). This code is run in AWS EC2.
* training_pipeline: Extracts data from remote MySQL table (above), performs simple preprocessing, and trains baseline ML models. The training results, params, and datasets are recorded and stored using MLFlow for tracing back when needed.

## 2. How to run with Airflow

My Airflow DAG includes tasks:
* ```print_task``` and ```setup_config_task```: Print and save the ```execution_date```. Setup the config for data preprocessing and training.
* ```load_task```: Access to the remote MySQL and save the dataset in parquet.
* ```preprocess_task```: Perform data preprocessing and save the preprocessed data seperately.
* ```train_task```: Train classification task using Pycaret and track with MLFlow. Save the best-performed model for deployment.
* ```clean_task```: Clean the caches and tmp file.

For running ```training_pipeline``` with Airflow, do as follows:

**Step 1**: Go to ```training_pipeline```

```console
cd mlflow_pipeline
```

**Step 2**: Build and deploy docker image

```console
docker compose build && docker compose up
```

**Step 3**: Go inside the docker container

```console
docker ps
```

Copy the container id (or name) and run
```console
docker exec -it container_id bash
```
Where ```container_id``` is replaced by your container id.

**Step 4**: Set up Airflow inside docker container

```console
export AIRFLOW_HOME=$(pwd) && airflow db init
```
Where AIRFLOW_HOME is the environment variable for running airflow. Your AIRFLOW_HOME is set to be ```training_pipeline/```. You can check it by:

```console
echo $AIRFLOW_HOME
```

**Step 4**: Check existing dags and create Airflow user

The below command should return you the dag defined in ```dags/dag_training_bash```: 

```console
airflow dags list
```
Airflow requires you to create a simple account to access to the webserver UI:
```console
airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
```
You can check if your account is created successfully by running:
```console
airflow users list
```

**Step 5**: Running Airflow scheduler and websever
```console
airflow scheduler
```

Open another cmd tab, go inside your docker container and run:
```console
airflow webserver -p 8080
```
Go to ```http://localhost:8080/```. You can keep track your flow and run here. You can also trigger dag and check the running result.

Please refer to the Airflow doc [[source](https://airflow.apache.org/docs/apache-airflow/stable/index.html)] to read about the concepts and usages of Airflow.

## 3. How to run with MLFlow only

If you just want to run MLFlow instead of the wole Airflow dag,  do as follows:

**Step 1**: Go to ```training_pipeline```

```console
cd mlflow_pipeline
```

**Step 2**: Build docker image

```console
docker build -t mlflow-pipeline -f Dockerfile .
```

**Step 3**: Build MLFlow project

```console
 mlflow run . -P baseline_sample= <float> -P task=<string> -P target=<string> --experiment-name <name>
```

Where:
* ```baseline_sample``` is the percentage of the data will be used for running the baseline (default 0.1)
* ```task``` is 'classification' or 'regression'
* ```target``` is the name of target feature
* ```--experiment-name``` is the name of this experiment run

Example:

```console
mlflow run . -P baseline_sample=0.1 -P task='classification' -P target='click' --experiment-name pycaret_experiment
```

**Step 4**: Check the recorded results

Note: When running against a local tracking URI, MLflow mounts the host system’s tracking directory (e.g., a local mlruns directory) inside the container so that metrics, parameters, and artifacts logged during project execution are accessible afterwards [[source](https://mlflow.org/docs/latest/projects.html#:~:text=When%20running%20against%20a%20local%20tracking%20URI%2C%20MLflow%20mounts%20the%20host%20system%E2%80%99s%20tracking%20directory%20(e.g.%2C%20a%20local%20mlruns%20directory)%20inside%20the%20container%20so%20that%20metrics%2C%20parameters%2C%20and%20artifacts%20logged%20during%20project%20execution%20are%20accessible%20afterwards.)]. In our case, the mlruns folder will be mounted back to the local directory (and not in the Docker image).

Simply call ```mlflow ui``` in the command-line for accessing the tracking UI.

```console
mlflow ui
```

## 4. Limitation

This is a toy project for me to learn about Airflow and MLFlow at a basic level. I'm aware that industry deployment is more complicated and sophisticated than what shown in my repo. 

A data pipeline with ETL process should be built to handle data loading from MySQL. Also, more MLOps modules such as Feast and CI/CD tools can be used to improve the quality of this project. 

## 5. Reference

* MLOps Crash Course [[source](https://github.com/MLOpsVN/mlops-crash-course-code)]: Helpful and practical course on MLOps.

* Airflow doc [[source](https://airflow.apache.org/docs/apache-airflow/stable/index.html)] 

* MLFlow doc [[source](https://mlflow.org/docs/latest/projects.html#:~:text=When%20running%20against%20a%20local%20tracking%20URI%2C%20MLflow%20mounts%20the%20host%20system%E2%80%99s%20tracking%20directory%20(e.g.%2C%20a%20local%20mlruns%20directory)%20inside%20the%20container%20so%20that%20metrics%2C%20parameters%2C%20and%20artifacts%20logged%20during%20project%20execution%20are%20accessible%20afterwards.)]