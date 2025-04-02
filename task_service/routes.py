from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task, db
from flask_cors import cross_origin

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
    try:
        data = request.get_json()
        print(data)  # Check the incoming data
        
        # Get the task description
        description = data['task']
        
        # Create a new task instance
        new_task = Task(description=description)
        
        # Add the task to the session
        db.session.add(new_task)
        
        # Commit the transaction to save the task
        db.session.commit()
        
        # Return the task details as JSON with a 201 status code
        return jsonify({
            "id": new_task.id, 
            "description": new_task.description
        }), 201
    
    except Exception as e:
        # If there's an error, rollback the session and print the error
        db.session.rollback()
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": "Failed to add task", "message": str(e)}), 500

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

@task_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200
