from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route('/api/tasks', methods=['POST'])
def create_task():
    # Get JSON data from request body
    data = request.get_json()
    # Access the data
    title = data.get('title')
    description = data.get('description')
    # Process and return response
    return jsonify({
        'message': 'Task created successfully',
        'task': {
            'title': title,
            'description': description
        }
    }), 201 # 201 = Created

# At the top of app.py, after imports
tasks = [] # Global list to store tasks

task_id_counter = 1 # To generate unique IDs
@app.route('/api/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()
    new_task = {
        'id': task_id_counter,
        'title': data.get('title'),
        'description': data.get('description'),
        'completed': False
    }
    tasks.append(new_task)
    task_id_counter += 1
    return jsonify(new_task), 201

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        'tasks': tasks,
        'count': len(tasks)
    }), 200

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        'tasks': tasks,
        'count': len(tasks)
    }), 200

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Find task with matching ID
    task = next((t for t in tasks if t[’id’] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task), 200

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Find task with matching ID
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task), 200

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
 # Find the task
 # Update title, description, or completed status
 # Return updated task
 pass
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
 # Find and remove the task
 # Ret

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
 # Find the task
 # Update title, description, or completed status
 # Return updated task
 pass

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
 # Find and remove the task
 # Return success message
 pass

@app.route('/api/tasks', methods=['POST'])
def create_task():
 data = request.get_json()
 # Validation
 if not data:
    return jsonify({'error': 'No data provided'}), 400
 if 'title' not in data or not data['title'].strip():
    return jsonify({'error': 'Title is required'}), 400
 if len(data['title']) > 100:
    return jsonify({'error': 'Title too long'}), 400
 # Create task...
 # Rest of the code

@app.route('/api/tasks', methods=['POST'])
def create_task():
 data = request.get_json()
 # Validation
 if not data:
    return jsonify({'error': 'No data provided'}), 400
 if 'title' not in data or not data['title'].strip():
    return jsonify({'error': 'Title is required'}), 400
 if len(data['title']) > 100:
    return jsonify({'error': 'Title too long'}), 400
 # Create task...
 # Rest of the code

@app.route('/api/tasks', methods=['POST'])
def create_task():
 data = request.get_json()
 # Validation
 if not data:
    return jsonify({'error': 'No data provided'}), 400
 if 'title' not in data or not data['title'].strip():
    return jsonify({'error': 'Title is required'}), 400
 if len(data['title']) > 100:
    return jsonify({'error': 'Title too long'}), 400
 # Create task...
 # Rest of the code