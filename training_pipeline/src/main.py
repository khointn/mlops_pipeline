import argparse
import os
import sys
import time
#from data_preparation import data_preparation
from data_preparation import data_preparation
from data_preprocess import Preprocessing
from data_validation import Validation
from training import Training
from clean import clean
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

if __name__ == "__main__":

    # Request arguments from user
    parser = argparse.ArgumentParser(description='ML pipeline with pycaret and mlflow.')
    parser.add_argument(
        '--baseline_sample',
        type=float,
        nargs='?',
        help='Data samples used for baseline with pycaret. If bigger than 1, then will be treated as number of sample. If smaller than 1, then will be treated as fraction.',
        default=50000,
    )
    parser.add_argument(
        '--baseline_sample_limit',
        type=float,
        nargs='?',
        help='Default: 50.000',
        default=50000,
    )
    parser.add_argument(
        '--data_path',
        type=str,
        nargs='?',
        help='Path to the training data.',
        default=config.DATA_PATH,
    )
    parser.add_argument(
        '--task',
        type=str,
        nargs='?',
        help='Task to be performed: classification or regression (default: classification).',
        default=config.TASK,
    )
    parser.add_argument(
        '--target',
        type=str,
        nargs='?',
        help='Target variable name (your y-array).',
        default=config.TARGET,
    )

    args = parser.parse_args()
    config.BASELINE_SAMPLE = args.baseline_sample
    config.BASELINE_SAMPLE_LIMIT = args.baseline_sample_limit
    config.DATA_PATH = args.data_path if args.data_path != '' else config.DATA_PATH
    config.TASK = args.task
    config.TARGET = args.target

    # data preparation
    data_preparation()
    # data preprocess
    Preprocessing()
    # data validation
    Validation()
    baseline = Training()
    baseline.train_baseline()
    baseline.save_model()
    # clean
    time.sleep(20)
    clean(remove_tmp = False)

