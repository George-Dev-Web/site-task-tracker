# app.py
from flask import Flask
from flask_cors import CORS
from server.config import db, migrate
from server.models import *

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from server.controllers.project_controller import project_bp
    app.register_blueprint(project_bp)

    return app
