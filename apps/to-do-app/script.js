// Functions for handling tasks
window.addEventListener('DOMContentLoaded', (event) => {
    loadTasks(); // Call the function to load tasks when the page loads
});

function loadTasks() {
    fetch('/load-tasks', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(tasks => {
        console.log('Tasks loaded:', tasks);
        // Update your UI to display the tasks (tasks is an array of tasks)
        displayTasks(tasks);
    })
    .catch(error => {
        console.error('Error loading tasks:', error);
    });
}

function displayTasks(tasks) {
    const taskOutput = document.getElementById('taskOutput');
    taskOutput.value = tasks.join('\n');
}

function addTask() {
    const taskInput = document.getElementById('taskInput');
    const task = taskInput.value.trim();
  
    if (task !== '') {
      const data = {
        operation: 'add', // Set the operation for adding a task
        task: task
      };
  
      fetch('/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(result => {
        console.log(result); // Log the response from the server
        loadTasks(); // Reload tasks after adding a new task
      })
      .catch(error => {
        console.error('Error:', error);
      });
  
      taskInput.value = '';
    }
}

function editTask() {
    // Implement edit task functionality based on your requirements
    // Call appropriate Flask route to handle editing
}

function deleteTask() {
    // Implement delete task functionality based on your requirements
    // Call appropriate Flask route to handle deletion
}
