# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Define the path to the JSON file within the current directory
TASKS_FILE = os.path.join(os.getcwd(), "apps\\to-do-app\\tasks.json")

# Function to load tasks from JSON file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

# Function to save tasks to JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Route to display tasks
@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form.get('task')
    tasks = load_tasks()
    tasks.append({'task': new_task, 'done': False})
    save_tasks(tasks)
    return redirect(url_for('index'))

# Route to update task status (mark as done/not done)
@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    tasks = load_tasks()
    tasks[task_id]['done'] = not tasks[task_id]['done']
    save_tasks(tasks)
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    tasks = load_tasks()
    del tasks[task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

# API endpoint to get tasks in JSON format
@app.route('/api/tasks')
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(debug=True)
