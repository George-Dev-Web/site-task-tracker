from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.task import Task
from models.project import Project
from models.assignee import Assignee
from config import db

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@task_bp.route("<int:id>", methods=["GET"])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())

@task_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    data = request.get_json()
    try:
        task = Task(
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status", "pending"),
            project_id=data["project_id"]
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@task_bp.route("/<int:task_id>/assignees", methods=["POST"])
@jwt_required()
def assign_assignee(task_id):
    data = request.get_json()
    try:
        task = Task.query.get(task_id)
        assignee = Assignee.query.get(data["assignee_id"])
        if not task or not assignee:
            return jsonify({"error": "Task or Assignee not found"}), 404

        db.session.execute(
            f"""
            INSERT INTO task_assignees (task_id, assignee_id, hours_spent)
            VALUES ({task.id}, {assignee.id}, {data.get("hours_spent", 0)})
            """
        )
        db.session.commit()
        return jsonify({"message": "Assignee added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@task_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@task_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    try:
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.status = data.get("status", task.status)
        db.session.commit()
        return jsonify(task.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400