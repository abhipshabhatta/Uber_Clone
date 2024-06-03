from flask import Flask
from flask_pymongo import PyMongo

def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SECRET_KEY'] = 'azerty'
    app.config["MONGO_URI"] = "mongodb://localhost:27017/uber_user"

    mongo = PyMongo(app)

    # Register routes
    from .route import configure_routes
    configure_routes(app)

    return app
