import logging
from app.vcap import get_database_uri

SQLALCHEMY_DATABASE_URI = get_database_uri()
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'secret-for-dev-only'
LOGGING_LEVEL = logging.INFO