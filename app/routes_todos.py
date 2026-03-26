from flask import Blueprint, request, jsonify

# Initialize the blueprint
todos_bp = Blueprint('todos', __name__)

todos = []

# Endpoint to add a todo
@todos_bp.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    new_todo = {'id': len(todos) + 1, 'task': data['task'], 'completed': False}
    todos.append(new_todo)
    return jsonify(new_todo), 201

# Endpoint to list todos
@todos_bp.route('/todos', methods=['GET'])
def list_todos():
    return jsonify(todos), 200

# Endpoint to complete a todo
@todos_bp.route('/todos/<int:todo_id>/complete', methods=['PUT'])
def complete_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if todo:
        todo['completed'] = True
        return jsonify(todo), 200
    return jsonify({'error': 'Todo not found'}), 404

# Endpoint to delete a todo
@todos_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return jsonify({'message': 'Todo deleted'}), 204
