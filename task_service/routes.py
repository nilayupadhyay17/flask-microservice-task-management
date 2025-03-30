from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task, db

task_bp = Blueprint("task", __name__)
# Fetch tasks route
@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = Task.query.all()
    tasks_list = [{"id": task.id, "description": task.description} for task in tasks]
    return jsonify(tasks_list)

# Add task route
@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    data = request.get_json()
    description = data['task']
    new_task = Task(description=description)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "description": new_task.description}), 201

# Delete task route
@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"message": "Task not found!"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully!"}), 200
