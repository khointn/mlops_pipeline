from utils import *
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator

with DAG(
    dag_id="bash_training",
    default_args=DefaultConfig.DEFAULT_DAG_ARGS,
    schedule="@once",
    start_date=pendulum.datetime(2023, 9, 26, tz="UTC"),
    catchup=False,
) as dag:
    
    print_task = PythonOperator(
        task_id='print_task',
        python_callable= print_and_save_execution_date,
    )
    
    setup_config_task = BashOperator(
        task_id="bash_setup_config_task",
        bash_command="cd $AIRFLOW_HOME && python src/setup_config.py --load_default_config=True"
    )

    load_task = BashOperator(
        task_id="bash_load_task",
        bash_command="cd $AIRFLOW_HOME && python src/data_preparation.py",
    )

    preprocess_task = BashOperator(
        task_id="bash_preprocess_task",
        bash_command="cd $AIRFLOW_HOME && python src/data_preprocess.py && python src/data_validation.py",
    )
    
    train_task = BashOperator(
        task_id="bash_train_task",
        bash_command="cd $AIRFLOW_HOME && python src/training.py",
    )

    clean_task = BashOperator(
        task_id="bash_clean_task",
        bash_command="cd $AIRFLOW_HOME && python src/clean.py",
    )

    print_task >> setup_config_task >> load_task >> preprocess_task >> train_task >> clean_task
