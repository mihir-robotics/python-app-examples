# backend script, only contains functions

import json

# Read JSON file
def readJSON(filename="tasks.json"):
    try:
        with open(filename, 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []  # Create an empty list if the file doesn't exist
    return tasks

# Write to JSON
def writeJSON(tasks, filename="tasks.json"):
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)
        

def displayList(arg):
    for i in range(len(arg)):
            print(str(i+1)+". "+arg[i])


def operateOnList(tasks, operation):

    validOperations = ['add', 'delete', 'update']
    if operation not in validOperations:
        raise ValueError

    if operation == 'add':
        addTask = input("Give task to be added: ")
        tasks.append(addTask)

    elif operation == 'delete':    
        displayList(tasks)
        delIndex = int(input("Give task no. to be deleted: "))
        try:
            delIndex -= 1
            if 0 <= delIndex < len(tasks):
                del tasks[delIndex]
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")
            
    elif operation == 'update':
        displayList(tasks)
        updateIndex = int(input("Give task no. to be updated: "))
        try:
            updateIndex -= 1
            if 0 <= updateIndex < len(tasks):
                update = input("Write the updated task here: ")
                tasks[updateIndex] = update
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")

    return tasks

def getTasks(toDoList):
    if toDoList:
        displayList(toDoList)

    print("You can make changes to this list using 'add', 'update' or 'delete' commands!")
    userOperation = input("-> ")
    
    try:
        toDoList = operateOnList(toDoList, userOperation)
        writeJSON(toDoList)
    except Exception as e:
        print("Oops, it seems something went wrong!" + str(e))

