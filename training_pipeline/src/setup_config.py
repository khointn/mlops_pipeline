import argparse
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
import yaml

def setup_config():
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

    parser.add_argument(
        '--load_default_config',
        type=str,
        nargs='?',
        help='Set to True if load default config (default: False)',
        default='False',
    )

    args = parser.parse_args()

    if args.load_default_config == 'False':
        tmp_config = {}
        tmp_config['BASELINE_SAMPLE'] = args.baseline_sample
        tmp_config['BASELINE_SAMPLE_LIMIT'] = args.baseline_sample_limit
        tmp_config['TASK'] = args.task
        tmp_config['TARGET'] = args.target

        with open('tmp/tmp_config.yaml', 'w') as f:
            yaml.dump(tmp_config, f, default_flow_style=False)
    
    else:
        pass

if __name__ == "__main__":
    setup_config()