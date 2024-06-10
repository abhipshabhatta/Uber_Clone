from flask import Flask
from flask_pymongo import PyMongo
from flask_session import Session
import redis
import logging

logging.basicConfig(level=logging.DEBUG)

def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SECRET_KEY'] = 'azerty'
    app.config["MONGO_URI"] = "mongodb+srv://abhipshabhatta:%40bheeps%40123@uberclone.qqr6qbm.mongodb.net/uber_clone_db?retryWrites=true&w=majority&ssl=true"

    # Redis configuration
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'uber_clone:'
    app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6380, db=0)

    # Initialize extensions
    mongo = PyMongo(app, tlsAllowInvalidCertificates=True)  # Allow invalid SSL certificates for debugging
    Session(app)  # Initialize session with Redis

    # Register routes
    from .app import app as main_app
    app.register_blueprint(main_app)

    return app