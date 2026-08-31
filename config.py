import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///our_forever.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRIVATE_PASSWORD = os.getenv("PRIVATE_PASSWORD", "PoonamBikash@123")

