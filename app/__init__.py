from flask import Flask
from flask_pymongo import PyMongo

def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SECRET_KEY'] = 'azerty'
    app.config["MONGO_URI"] = "mongodb+srv://abhipshabhatta:<@bheeps@123>@uberclone.qqr6qbm.mongodb.net/uber_clone_db?retryWrites=true&w=majority"

    mongo = PyMongo(app)

    # Register routes
    from .app import app as main_app
    app.register_blueprint(main_app)

    return app
