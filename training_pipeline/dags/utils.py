import pendulum
import yaml
from airflow.operators.python import get_current_context

class DefaultConfig:
    DEFAULT_DAG_ARGS = {
        "owner": "khointn",
        "retries": 3,
        "retry_delay": pendulum.duration(seconds=20),
    }

    DEFAULT_DOCKER_OPERATOR_ARGS = {
        "image": f"/training_pipeline-training_pipeline:latest",
        "api_version": "auto",
        "auto_remove": "success",
    }

def print_and_save_execution_date():
  context = get_current_context()
  ds = str(context['execution_date'])
  print(f"The execution date of this flow is {ds}")
  exec_date = {}
  exec_date['EXEC_DATE'] = ds
  
  with open('tmp/exec_date.yaml', 'w') as f:
    yaml.dump(exec_date, f, default_flow_style=False)