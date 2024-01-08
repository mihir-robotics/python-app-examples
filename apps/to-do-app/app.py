from flask import Flask, jsonify, request, send_from_directory
import json

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def styles():
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def scripts():
    return send_from_directory('.', 'script.js')

@app.route('/load-tasks', methods=['GET'])
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            tasks = file.read()
        return tasks, 200
    except FileNotFoundError:
        return jsonify({"error": "Tasks file not found"}), 404

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        try:
            with open('tasks.json', 'r') as file:
                tasks = file.read()
            return tasks, 200
        except FileNotFoundError:
            return jsonify({"error": "Tasks file not found"}), 404
    elif request.method == 'POST':
        data = request.get_json()
        if data:
            operation = data.get('operation')
            if operation == 'add':
                task = data.get('task')
                if task:
                    try:
                        with open('tasks.json', 'r') as file:
                            tasks = json.load(file)
                        tasks.append(task)
                        with open('tasks.json', 'w') as file:
                            json.dump(tasks, file, indent=4)
                        return jsonify({"message": "Task added successfully"}), 200
                    except FileNotFoundError:
                        return jsonify({"error": "Tasks file not found"}), 404
                else:
                    return jsonify({"error": "Task value is empty"}), 400
            # Implement edit and delete operations similarly
            # ...
            else:
                return jsonify({"error": "Invalid operation"}), 400
        else:
            return jsonify({"error": "No data received"}), 400

if __name__ == '__main__':
    app.run(debug=True)
