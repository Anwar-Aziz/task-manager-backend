from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to Student Info API',
        'status': 'running'
    })

@app.route('/api/student')
def student_info():
    student_id = request.args.get('id', '12345')

    students = {
        '12345': {'id': '12345', 'name': 'Alice', 'age': 21, 'major': 'Computer Science'},
        '67890': {'id': '67890', 'name': 'Bob', 'age': 22, 'major': 'Mathematics'}
    }

    student = students.get(student_id)

    if student:
        return jsonify(student)
    else:
        return jsonify({'error': 'Student not found'}), 404

@app.route('/api/students/count')
def students_count():
    students = {
        '12345': {'id': '12345', 'name': 'Alice', 'age': 21, 'major': 'Computer Science'},
        '67890': {'id': '67890', 'name': 'Bob', 'age': 22, 'major': 'Mathematics'}
    }
    return jsonify({
        'count': len(students)
    })

# -----------------------------
# Run the app
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True, port=7000)
