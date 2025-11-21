from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database"
tasks = []
task_id_counter = 1


# CREATE task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    global task_id_counter

    data = request.get_json()

    # Validation
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    if 'title' not in data or not data['title'].strip():
        return jsonify({'error': 'Title is required'}), 400
    if len(data['title']) > 100:
        return jsonify({'error': 'Title too long'}), 400

    #Create task
    new_task = {
        'id': task_id_counter,
        'title': data.get('title'),
        'description': data.get('description', ''),
        'completed': False
    }
    tasks.append(new_task)
    task_id_counter += 1

    return jsonify(new_task), 201


# READ all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        'tasks': tasks,
        'count': len(tasks)
    }), 200


# READ single task
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task), 200


# UPDATE task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = next((t for t in tasks if t['id'] == task_id), None)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Update fields if provided
    if 'title' in data:
        if not data['title'].strip():
            return jsonify({'error': 'Title cannot be empty'}), 400
        task['title'] = data['title']

    if 'description' in data:
        task['description'] = data['description']

    if 'completed' in data:
        task['completed'] = bool(data['completed'])

    return jsonify(task), 200


# DELETE task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': f'Task {task_id} deleted successfully'}), 200


# Run app
if __name__ == '__main__':
    app.run(debug=True,port=5000)
