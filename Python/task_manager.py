import json
import os

# File to store tasks
TASKS_FILE = "tasks.json"

# Initialize tasks
def initialize_tasks():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as file:
            json.dump([], file)

def load_tasks():
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task():
    name = input("Enter task name: ")
    while True:
        priority = input("Enter task priority (High/Medium/Low): ").lower()
        if priority in ["high", "medium", "low"]:
            break
        else:
            print("Invalid priority. Please enter High, Medium, or Low.")

    tasks = load_tasks()
    tasks.append({"name": name, "status": "pending", "priority": priority})
    save_tasks(tasks)
    print(f"Task '{name}' with priority '{priority}' added successfully.")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['name']} - {task['status']} - Priority: {task['priority']}")

def update_task():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    list_tasks()
    try:
        task_num = int(input("Enter task number to update: "))
        if 1 <= task_num <= len(tasks):
            new_status = input("Enter new status (pending/completed): ").lower()
            if new_status in ["pending", "completed"]:
                tasks[task_num - 1]["status"] = new_status
            else:
                print("Invalid status. Status not updated.")

            new_priority = input("Enter new priority (High/Medium/Low): ").lower()
            if new_priority in ["high", "medium", "low"]:
                tasks[task_num - 1]["priority"] = new_priority
            else:
                print("Invalid priority. Priority not updated.")

            save_tasks(tasks)
            print(f"Task {task_num} updated successfully.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def delete_task():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    list_tasks()
    try:
        task_num = int(input("Enter task number to delete: "))
        if 1 <= task_num <= len(tasks):
            tasks.pop(task_num - 1)
            save_tasks(tasks)
            print(f"Task {task_num} deleted successfully.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def main():
    initialize_tasks()
    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            update_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
