import pandas as pd
import time
import db_config
from sqlalchemy import create_engine, text

if __name__ == '__main__':
    time.sleep(20)

    try:
        engine = create_engine(db_config.SQLALCHEMY_DATABASE_URI)
        with engine.connect() as connection:
            print("You're connected to database:", engine.url.database)
            connection.execute(text('DROP TABLE IF EXISTS advertising;'))
            connection.close()

    except Exception as e:
        print("Error while connecting to MySQL", e)

    print("Create table and insert data")
    df = pd.read_csv(config.DATA_PATH)
    df = df.astype("str")
    df.to_sql("advertising", con = engine, if_exists = 'replace', index = False)
    print("Inserted successfully")