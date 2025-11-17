from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# MySQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passw0rd@localhost:3308/app_db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# PART 1: Categories
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    tasks = db.relationship("Task", backref="category", lazy=True)


# PART 2: Tasks with Due Dates
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)

    # Category relation
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    # Due date
    due_date = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Create all tables
with app.app_context():
    db.create_all()


# CATEGORY ENDPOINTS
@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Category name is required'}), 400

    # Prevent duplicates
    if Category.query.filter_by(name=name).first():
        return jsonify({'error': 'Category already exists'}), 409

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Category created', 'id': category.id}), 201


@app.route('/api/categories', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    return jsonify([
        {'id': c.id, 'name': c.name} for c in categories
    ])


# TASK ENDPOINTS
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    category_id = data.get('category_id')
    due_date_str = data.get('due_date')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    # Validate due date
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Validate category
    if category_id:
        if not Category.query.get(category_id):
            return jsonify({'error': 'Category not found'}), 404

    task = Task(title=title, description=description, category_id=category_id, due_date=due_date)
    db.session.add(task)
    db.session.commit()

    return jsonify({'message': 'Task created', 'id': task.id}), 201


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    category_id = request.args.get('category')

    if category_id:
        tasks = Task.query.filter_by(category_id=category_id).all()
    else:
        tasks = Task.query.all()

    return jsonify([
        {
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'completed': t.completed,
            'category_id': t.category_id,
            'due_date': t.due_date.strftime('%Y-%m-%d') if t.due_date else None,
            'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for t in tasks
    ])


@app.route('/api/tasks/overdue', methods=['GET'])
def overdue_tasks():
    now = datetime.utcnow()
    tasks = Task.query.filter(Task.due_date != None, Task.due_date < now, Task.completed == False).all()

    return jsonify([
        {
            'id': t.id,
            'title': t.title,
            'due_date': t.due_date.strftime('%Y-%m-%d'),
        }
        for t in tasks
    ])


# PART 3: STATS ENDPOINT
@app.route('/api/tasks/stats', methods=['GET'])
def task_stats():
    total = Task.query.count()
    completed = Task.query.filter_by(completed=True).count()
    pending = Task.query.filter_by(completed=False).count()

    now = datetime.utcnow()
    overdue = Task.query.filter(Task.due_date != None, Task.due_date < now, Task.completed == False).count()

    return jsonify({
        'total_tasks': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue
    })


# Run the app
if __name__ == '__main__':
    app.run(debug=True,port=6000)
