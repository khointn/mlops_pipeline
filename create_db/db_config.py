DB_HOST = "123.456.789.000" #Change here
DB_PORT = 3306
DB_USER = "username" #Change here
DB_PASSWORD = "password" #Change here
DB_NAME = "mldb"
SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"