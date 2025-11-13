from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# ===== In-memory "database" =====
tasks = []
categories = []
task_id_counter = 1
category_id_counter = 1


# ===== Helper Functions =====
def find_task(task_id):
    return next((t for t in tasks if t["id"] == task_id), None)

def find_category(cat_id):
    return next((c for c in categories if c["id"] == cat_id), None)

def parse_date(date_str):
    """Parse date in YYYY-MM-DD format; return datetime or None"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


# ====== PART 1: CATEGORY MANAGEMENT ======

@app.route('/api/categories', methods=['POST'])
def create_category():
    global category_id_counter
    data = request.get_json()

    if not data or 'name' not in data or not data['name'].strip():
        return jsonify({'error': 'Category name is required'}), 400

    new_cat = {
        'id': category_id_counter,
        'name': data['name'].strip()
    }
    categories.append(new_cat)
    category_id_counter += 1
    return jsonify(new_cat), 201


@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': categories, 'count': len(categories)}), 200


# ====== PART 1 + PART 2: TASK MANAGEMENT ======

@app.route('/api/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400
    if 'title' not in data or not data['title'].strip():
        return jsonify({'error': 'Title is required'}), 400

    # Optional fields
    category_id = data.get('category_id')
    due_date_str = data.get('due_date')
    priority = data.get('priority', 'medium').lower()

    # Validate category
    if category_id is not None and not find_category(category_id):
        return jsonify({'error': 'Invalid category_id'}), 400

    # Validate due date format
    due_date = None
    if due_date_str:
        due_date = parse_date(due_date_str)
        if not due_date:
            return jsonify({'error': 'Invalid due_date format (expected YYYY-MM-DD)'}), 400

    # Validate priority
    if priority not in ['low', 'medium', 'high']:
        return jsonify({'error': 'Priority must be low, medium, or high'}), 400

    new_task = {
        'id': task_id_counter,
        'title': data['title'].strip(),
        'description': data.get('description', ''),
        'completed': False,
        'category_id': category_id,
        'due_date': due_date_str,
        'priority': priority
    }

    tasks.append(new_task)
    task_id_counter += 1
    return jsonify(new_task), 201


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    category_id = request.args.get('category_id', type=int)
    filtered_tasks = tasks

    # Filter by category if provided
    if category_id is not None:
        filtered_tasks = [t for t in tasks if t['category_id'] == category_id]

    return jsonify({'tasks': filtered_tasks, 'count': len(filtered_tasks)}), 200


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task), 200


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = find_task(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'title' in data:
        if not data['title'].strip():
            return jsonify({'error': 'Title cannot be empty'}), 400
        task['title'] = data['title'].strip()

    if 'description' in data:
        task['description'] = data['description']

    if 'completed' in data:
        task['completed'] = bool(data['completed'])

    if 'category_id' in data:
        if not find_category(data['category_id']):
            return jsonify({'error': 'Invalid category_id'}), 400
        task['category_id'] = data['category_id']

    if 'due_date' in data:
        due_date = parse_date(data['due_date'])
        if not due_date:
            return jsonify({'error': 'Invalid due_date format (expected YYYY-MM-DD)'}), 400
        task['due_date'] = data['due_date']

    if 'priority' in data:
        priority = data['priority'].lower()
        if priority not in ['low', 'medium', 'high']:
            return jsonify({'error': 'Priority must be low, medium, or high'}), 400
        task['priority'] = priority

    return jsonify(task), 200


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = find_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': f'Task {task_id} deleted successfully'}), 200


# ====== PART 2: OVERDUE TASKS ======

@app.route('/api/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    today = datetime.now()
    overdue = []
    for t in tasks:
        if t['due_date'] and not t['completed']:
            due_date = parse_date(t['due_date'])
            if due_date and due_date < today:
                overdue.append(t)
    return jsonify({'overdue_tasks': overdue, 'count': len(overdue)}), 200


# ====== PART 3: STATISTICS ======

@app.route('/api/tasks/stats', methods=['GET'])
def get_stats():
    total = len(tasks)
    completed = sum(t['completed'] for t in tasks)
    pending = total - completed

    today = datetime.now()
    overdue = sum(
        1 for t in tasks
        if not t['completed'] and t['due_date'] and parse_date(t['due_date']) and parse_date(t['due_date']) < today
    )

    stats = {
        'total_tasks': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue
    }
    return jsonify(stats), 200


# ===== Run Server =====
if __name__ == '__main__':
    app.run(debug=True, port=5000)
