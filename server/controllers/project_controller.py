from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.project import Project
from config import db
from datetime import datetime

project_bp = Blueprint("project_bp", __name__, url_prefix="/projects")

@project_bp.route("", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    return jsonify([p.to_dict() for p in projects])

@project_bp.route("<int:id>", methods=["GET"])
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify(project.to_dict())

@project_bp.route("", methods=["POST"])
@jwt_required()
def create_project():
    data = request.get_json()
    user_id = get_jwt_identity()
    try:
        project = Project(
            user_id=user_id,
            name=data["name"],
            location=data.get("location"),
            start_date=datetime.strptime(data["start_date"], "%Y-%m-%d").date(),
            end_date=datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        )
        db.session.add(project)
        db.session.commit()
        return jsonify(project.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@project_bp.route("/<int:id>/tasks", methods=["GET"])
def get_project_tasks(id):
    project = Project.query.get_or_404(id)
    return jsonify([task.to_dict() for task in project.tasks])

@project_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_project(id):
    project = Project.query.get_or_404(id)
    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({"message": "Project deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@project_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.get_json()
    try:
        project.name = data.get("name", project.name)
        project.location = data.get("location", project.location)
        if data.get("start_date"):
            project.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        if data.get("end_date"):
            project.end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        db.session.commit()
        return jsonify(project.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
