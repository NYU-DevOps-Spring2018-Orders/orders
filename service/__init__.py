
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Create app and db
    app = Flask(__name__)

    db.init_app(app)

    from api.items import items
    from api.orders import orders
    # Register blueprints
    app.register_blueprint(items)
    app.register_blueprint(orders)

    # We'll just use SQLite here so we don't need an external database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/development.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'itsasecret'
    app.config['LOGGING_LEVEL'] = logging.INFO

    return app
