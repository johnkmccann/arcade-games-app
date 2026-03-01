import os

# Environment configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/mydatabase'
    DEBUG = os.environ.get('DEBUG') or False
