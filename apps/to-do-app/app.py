'''
To-Do Web App using Flask

Dependencies:
- Flask: Web framework for creating the application

Usage:
- Run this script with Python to start the Flask server.
- Access the To-Do app through a web browser at http://127.0.0.1:5000/

File Structure:
- app.py: Main Flask application file
- templates/index.html: HTML template for rendering the To-Do list
- static/styles.css: CSS Styles for Webpage
- tasks.json: JSON file to store the tasks
'''
# Imports
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Define the path to the JSON file within the current directory
TASKS_FILE = os.path.join(os.getcwd(), "apps\\to-do-app\\tasks.json")

# Function to load tasks from JSON file
def load_tasks():
    '''
    Load tasks from tasks.json file or create an empty list if the file doesn't exist.

    Returns:
    - tasks (list): List of tasks loaded from the JSON file or an empty list if the file is not found.
    '''
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

# Function to save tasks to JSON file
def save_tasks(tasks):
    '''
    Save tasks to tasks.json file.

    Args:
    - tasks (list): List of tasks to be saved to the JSON file.
    '''
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Route to display tasks
@app.route('/')
def index():
    '''
    Route to display the To-Do list.

    Renders:
    - index.html: HTML template displaying the current tasks.
    '''
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    '''
    Route to add a new task.

    Retrieves a new task from the form, appends it to the task list, and redirects to the main page.
    '''
    new_task = request.form.get('task')
    tasks = load_tasks()
    tasks.append({'task': new_task, 'done': False})
    save_tasks(tasks)
    return redirect(url_for('index'))

# Route to update task status (mark as done/not done)
@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    '''
    Route to update a task's status (mark as done/not done).

    Changes the status of the specified task and redirects to the main page.
    '''
    tasks = load_tasks()
    tasks[task_id]['done'] = not tasks[task_id]['done']
    save_tasks(tasks)
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    '''
    Route to delete a task.

    Deletes the specified task from the list and redirects to the main page.
    '''
    tasks = load_tasks()
    del tasks[task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

# API endpoint to get tasks in JSON format
@app.route('/api/tasks')
def get_tasks():
    '''
    API endpoint to get tasks in JSON format.

    Returns:
    - tasks (JSON): JSON data containing the list of tasks.
    '''
    tasks = load_tasks()
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) # Expose this app to the Network
