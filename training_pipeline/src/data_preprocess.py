import pandas as pd
import os
import sys
import yaml
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

if os.path.isfile('tmp/tmp_config.yaml'):
    with open('tmp/tmp_config.yaml') as f:
        tmp_config = yaml.full_load(f)
        config.BASELINE_SAMPLE = tmp_config['BASELINE_SAMPLE']
        config.BASELINE_SAMPLE_LIMIT = tmp_config['BASELINE_SAMPLE_LIMIT']
        config.TARGET = tmp_config['TARGET']
        config.TASK = tmp_config['TASK']

'''
Perform preprocessing
If feature is numerical, then perform min-max scaling
If feature is categorical, then perform ordinal encoder
'''

class Preprocessing:

    def __init__(self):
        # Read data & drop
        self.df = pd.read_parquet(config.DATA_PATH)
        self.drop()
        # Preprocess the baseline sample
        self.df_train = self.sampling()
        self.preprocess()
        del self.df
        # Save data
        self.df_train.info()
        self.df_train.to_parquet(config.PREPARED_DATA_PATH, index = False)

    # Maximum 50k
    def sampling(self):
        if config.BASELINE_SAMPLE > 1:
            print("Running pycaret baseline models with number of sample: ", config.BASELINE_SAMPLE)
            df_train = self.df.sample(n = min(int(config.BASELINE_SAMPLE), config.BASELINE_SAMPLE_LIMIT), axis = 0)
        else:
            print("Running pycaret baseline models with number of sample: ", len(self.df)*config.BASELINE_SAMPLE)
            df_train = self.df.sample(n = min(int(len(self.df)*config.BASELINE_SAMPLE), config.BASELINE_SAMPLE_LIMIT), axis = 0)
        return df_train

    def drop(self, cols = config.DROP_COLS, null_handling_strategy = 'drop', duplicate_handling_strategy = 'drop'):
        # Drop null
        if null_handling_strategy == 'drop':
            self.df = self.df.dropna(how = 'any')
        elif null_handling_strategy == 'keep':
            pass

        # Drop duplicate
        if duplicate_handling_strategy == 'drop':
            self.df = self.df.drop_duplicates()
        elif duplicate_handling_strategy == 'keep':
            pass

        # Drop columns
        if cols != []:
            self.df = self.df.drop(columns = cols)

    def preprocess(self):

        if config.CATEGORICAL_FEATURES != []:
            from sklearn.preprocessing import OrdinalEncoder
            encoder = OrdinalEncoder()
            encoder.fit(self.df[config.CATEGORICAL_FEATURES])
            self.df_train[config.CATEGORICAL_FEATURES] = encoder.transform(self.df_train[config.CATEGORICAL_FEATURES])

        if config.NUMERICAL_FEATURES != []:
            from sklearn.preprocessing import MinMaxScaler
            encoder = MinMaxScaler()
            encoder.fit(self.df[config.NUMERICAL_FEATURES])
            self.df_train[config.NUMERICAL_FEATURES] = encoder.transform(self.df_train[config.NUMERICAL_FEATURES])

if __name__ == "__main__":
    Preprocessing()
    
