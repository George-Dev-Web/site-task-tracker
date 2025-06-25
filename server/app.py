from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import db, migrate
from models import *

# JWT instance
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configs
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"  # 🔐 change before deployment

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    # Blueprints
    from controllers.project_controller import project_bp
    from controllers.task_controller import task_bp
    from controllers.assignee_controller import assignee_bp
    from controllers.user_controller import user_bp
    from controllers.auth_controller import auth_bp

    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(assignee_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    return app
