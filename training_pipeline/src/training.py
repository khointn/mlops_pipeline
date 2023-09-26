import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import yaml
import mlflow
import config
if os.path.isfile('tmp/tmp_config.yaml'):
    with open('tmp/tmp_config.yaml') as f:
        tmp_config = yaml.full_load(f)
        config.BASELINE_SAMPLE = tmp_config['BASELINE_SAMPLE']
        config.BASELINE_SAMPLE_LIMIT = tmp_config['BASELINE_SAMPLE_LIMIT']
        config.TARGET = tmp_config['TARGET']
        config.TASK = tmp_config['TASK']

if config.TASK == 'classification':
    from pycaret.classification import *
elif config.TASK == 'regression':
    from pycaret.regression import *

class Training:
    def __init__(self):
        # Load data
        self.df = pd.read_parquet(config.PREPARED_DATA_PATH)
        print("Shape of data: ", self.df.shape)

    def train_baseline(self):
        # Setup pycaret
        self.experiment = setup(data=self.df, 
                                target=config.TARGET, 
                                session_id=config.RANDOM_STATE, 
                                log_experiment=True, 
                                experiment_name='pycaret_experiment')
        # compare all models
        #compare_models(include=models().index.tolist(), n_select=2, parallel=FugueBackend(spark))
        self.best = compare_models()
        mlflow.log_param("data sample", config.BASELINE_SAMPLE)

    def save_model(self):
        if os.path.isfile('tmp/exec_date.yaml'):
            with open('tmp/exec_date.yaml') as f:
                exec_date = yaml.full_load(f)['EXEC_DATE']
            
            saved_model_path = f"{config.SAVED_MODEL_PATH}_{exec_date}"
            save_model(self.best, saved_model_path)
        
        else:
            save_model(self.best, config.SAVED_MODEL_PATH)

if __name__ == "__main__":
    baseline = Training()
    baseline.train_baseline()
    baseline.save_model()

        

