from flask import Blueprint, request, jsonify
from server.models.project import Project
from server.config import db

project_bp = Blueprint('projects', __name__, url_prefix="/projects")

@project_bp.route("", methods=["POST"])
def create_project():
    data = request.get_json()

    try:
        project = Project(
            user_id=data.get("user_id", 1),  # Placeholder user
            name=data["name"],
            location=data.get("location"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date")
        )

        db.session.add(project)
        db.session.commit()

        return jsonify(project.to_dict()), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
