from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path='store.env')  # specify file name

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')
    MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
    MYSQL_CURSORCLASS = 'DictCursor'