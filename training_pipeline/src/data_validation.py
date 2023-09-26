import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
import yaml

if os.path.isfile('tmp/tmp_config.yaml'):
    with open('tmp/tmp_config.yaml') as f:
        tmp_config = yaml.full_load(f)
        config.BASELINE_SAMPLE = tmp_config['BASELINE_SAMPLE']
        config.BASELINE_SAMPLE_LIMIT = tmp_config['BASELINE_SAMPLE_LIMIT']
        config.TARGET = tmp_config['TARGET']
        config.TASK = tmp_config['TASK']

class Validation:
    def __init__(self):
        self.raw_df = pd.read_parquet(config.DATA_PATH)
        self.preprocessed_df = pd.read_parquet(config.PREPARED_DATA_PATH)
        self.check_null_duplicate()
        self.data_validation()
        self.target_distribution()

    def check_null_duplicate(self):
        print("Null check:")
        if self.preprocessed_df.isnull().values.any():
            raise Exception('Data contains null values')
        else:
            print("No null values found!")

        print("Duplicate check:")
        if self.preprocessed_df.duplicated().any():
            print('Warning: Data contains duplicates')
        else:
            print("No duplicates found!")

    def data_validation(self):
        print("Features before preprocessing:", list(self.raw_df.columns))
        print("Features after preprocessing:", list(self.preprocessed_df.columns))
        print("Shape before preprocessing:", self.raw_df.shape)
        print("Shape after preprocessing:", self.preprocessed_df.shape)
    
    def target_distribution(self):
        print("Target distribution:", self.preprocessed_df[config.TARGET].value_counts(normalize=True))
        if self.preprocessed_df[config.TARGET].value_counts(normalize=True).max() > 0.7:
            print('Warning: Target distribution may be imbalanced. You may want to perform some imbalance-handling strategies.')

if __name__ == "__main__":
    Validation()

