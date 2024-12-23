from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
TasksFile = 'tasks.txt'
tasks = []


def load_tasks():
    global tasks
    if os.path.exists(TasksFile):
        with open(TasksFile, 'r') as f:
            tasks = json.load(f)


def save_tasks():
    with open(TasksFile, 'w') as f:
        json.dump(tasks, f)


def generate_id():
    if tasks:
        return max(task['id'] for task in tasks) + 1
    return 1


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    priority = data.get('priority')
    task_id = generate_id()
    task = {
        'id': task_id,
        'title': title,
        'priority': priority,
        'isDone': False
    }
    tasks.append(task)
    save_tasks()
    return jsonify(task)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    global tasks
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break

    if task is None:
        return '', 404
    task['isDone'] = True
    save_tasks()
    return '', 200

load_tasks()

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
