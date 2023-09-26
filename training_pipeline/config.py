#Tmp config
TASK = 'classification'
BASELINE_SAMPLE = 50000
BASELINE_SAMPLE_LIMIT = 50000
TARGET = 'click'

#Const path
DATA_PATH = './data/advertising.parquet'
PREPARED_DATA_PATH = './data/prepared_data.parquet'
SAVED_MODEL_PATH = './models/model'
CATEGORICAL_FEATURES = ['hour', 'C1', 'banner_pos', 'site_id', 'site_domain', 'site_category', 'app_id', 'app_domain', 'app_category', 'device_id', 'device_ip', 'device_model', 'device_type', 'device_conn_type', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21']
NUMERICAL_FEATURES = []
DROP_COLS = ['id']
TEST_SIZE = 0.2
RANDOM_STATE = 42

#DATABASE
DB_HOST = "123.456.789.000" #Change here
DB_PORT = 3306
DB_USER = "username" #Change here
DB_PASSWORD = "password" #Change here
DB_NAME = "mldb"
SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"