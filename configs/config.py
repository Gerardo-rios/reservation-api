import os

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv('DB_HOST', 'mysql-service')
DB_PORT = os.getenv("DB_PORT", 3306)
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = "mysql+pymysql"

DB_URI = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Secret key for JWT
SECRET_KEY = os.getenv("SECRET_KEY")

# CORS
FRONTEND_DOMAIN = os.getenv("FRONT_END_DOMAIN", "*")