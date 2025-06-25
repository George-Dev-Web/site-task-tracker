from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.assignee import Assignee
from config import db

assignee_bp = Blueprint("assignee_bp", __name__, url_prefix="/assignees")

@assignee_bp.route("", methods=["GET"])
def get_assignees():
    assignees = Assignee.query.all()
    return jsonify([a.to_dict() for a in assignees])

@assignee_bp.route("<int:id>", methods=["GET"])
def get_assignee(id):
    assignee = Assignee.query.get_or_404(id)
    return jsonify(assignee.to_dict())

@assignee_bp.route("", methods=["POST"])
@jwt_required()
def create_assignee():
    data = request.get_json()
    try:
        assignee = Assignee(name=data["name"], role=data["role"])
        db.session.add(assignee)
        db.session.commit()
        return jsonify(assignee.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@assignee_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_assignee(id):
    assignee = Assignee.query.get_or_404(id)
    data = request.get_json()
    try:
        assignee.name = data.get("name", assignee.name)
        assignee.role = data.get("role", assignee.role)
        db.session.commit()
        return jsonify(assignee.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@assignee_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_assignee(id):
    assignee = Assignee.query.get_or_404(id)
    try:
        db.session.delete(assignee)
        db.session.commit()
        return jsonify({"message": "Assignee deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
