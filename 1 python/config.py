import os
from pathlib import Path
from dotenv import load_dotenv

# параметры подключения к бд
load_dotenv()
db_params = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}