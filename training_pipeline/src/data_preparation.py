import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from sqlalchemy import create_engine

'''
Read raw dataset
Handle null (default = drop) and duplicate (default = drop)
Return parquet dataset
'''

def data_preparation():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    print("Create engine successfully")
    df = pd.read_sql('SELECT * from advertising;', con=engine)
    df.to_parquet(config.DATA_PATH, index = False)
    print("Extract data from MySQL successfully")

if __name__ == "__main__":
    data_preparation()
    