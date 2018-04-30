from flasgger import Swagger
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load the confguration
app.config.from_object('config')

# Swagger(app)
db = SQLAlchemy(app)

from app import server, models
