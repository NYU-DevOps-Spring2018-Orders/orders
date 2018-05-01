from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the Flask app
app = Flask(__name__)

# Load Config
app.config.from_object('config')
print('Database URI {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))
app.config['SQLALCHEMY_POOL_RECYCLE'] = 599
# Initialize SQLAlchemy
db = SQLAlchemy(app)

from app import server, models
