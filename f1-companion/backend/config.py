import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_USER = os.getenv("POSTGRES_USER", "username")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME = os.getenv("POSTGRES_DB", "f1companion")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OPENF1_API_URL = "https://api.openf1.org/v1"

    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 60

