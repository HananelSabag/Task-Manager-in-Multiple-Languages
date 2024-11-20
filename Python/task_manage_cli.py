import json
import os
from datetime import datetime
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
TASKS_FILE = os.path.join(DATA_DIR, "DB_task_manager.json")
SIGNATURE = "TaskManager"
LANGUAGE = "Python-CLI"
AUTHOR = "Hananel Sabag"

class TaskManager:
    def __init__(self):
   
   
        if not os.path.exists(DATA_DIR):
          os.makedirs(DATA_DIR)

        self.tasks = self._load_or_init_tasks()

    def _load_or_init_tasks(self):
        if not os.path.exists(TASKS_FILE):
            initial_data = {
                "metadata": {
                    "signature": SIGNATURE,
                    "language": LANGUAGE,
                    "last_modified": datetime.now().isoformat(),
                    "author": AUTHOR
                },
                "open_tasks": [],
                "completed_tasks": [],
                "activity_history": []
            }
            self._save_tasks(initial_data)
            return initial_data

        try:
            with open(TASKS_FILE, 'r') as file:
                data = json.load(file)
                if self._validate_data(data):
                    return data
                raise ValueError("Invalid data structure")
        except:
            return self._load_or_init_tasks()

    def _validate_data(self, data):
        required_keys = {"metadata", "open_tasks", "completed_tasks", "activity_history"}
        if not all(key in data for key in required_keys):
            return False
        
        metadata_keys = {"signature", "language", "last_modified", "author"}
        if not all(key in data["metadata"] for key in metadata_keys):
            return False
            
        return True

    def _save_tasks(self, tasks):
        timestamp = datetime.now().isoformat()
        tasks["metadata"].update({
            "last_modified": timestamp,
            "language": LANGUAGE
        })
        
        tasks["activity_history"].append({
            "program": "Task Manager",
            "language": LANGUAGE,
            "timestamp": timestamp
        })
        
        with open(TASKS_FILE, 'w') as file:
            json.dump(tasks, file, indent=4)

    def show_menu(self):
        while True:
            print("\n=== Task Manager ===")
            print("1. List Tasks")
            print("2. Add Task")
            print("3. Mark Task as Done")
            print("4. Delete Task")
            print("5. Show Completed Tasks")
            print("6. Show Activity History")
            print("0. Exit")
            
            choice = input("\nEnter your choice (0-6): ")
            
            if choice == "1":
                self.list_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.mark_done()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.show_completed()
            elif choice == "6":
                self.show_activity_history()
            elif choice == "0":
                print(f"\nGoodbye! Made by {AUTHOR}")
                break
            else:
                print("\nInvalid choice. Please try again.")

    def list_tasks(self):
        print("\n=== ACTIVE TASKS ===\n")
        if not self.tasks["open_tasks"]:
            print("No active tasks.")
            return
            
        for i, task in enumerate(self.tasks["open_tasks"], 1):
            print(f"{i}. {task['name']} - Priority: {task['priority']} - Deadline: {task['deadline']}")

    def add_task(self):
        print("\n=== Add New Task ===\n")
        name = input("Enter task name: ").strip()
        if not name:
            print("Task name cannot be empty!")
            return

        print("\nPriority:")
        print("1. High")
        print("2. Medium")
        print("3. Low")
        priority_choice = input("Choose priority (1-3): ")
        
        priority_map = {"1": "high", "2": "medium", "3": "low"}
        priority = priority_map.get(priority_choice, "medium")

        while True:
            deadline = input("Enter deadline (DD-MM-YYYY): ")
            try:
                datetime.strptime(deadline, "%d-%m-%Y")
                break
            except ValueError:
                print("Invalid date format! Please use DD-MM-YYYY")

        new_task = {
            "name": name,
            "priority": priority,
            "deadline": deadline,
            "created_at": datetime.now().isoformat()
        }
        
        self.tasks["open_tasks"].append(new_task)
        self._save_tasks(self.tasks)
        print("\nTask added successfully!")

    def mark_done(self):
        if not self.tasks["open_tasks"]:
            print("\nNo tasks to mark as done!")
            return

        print("\n=== Mark Task as Done ===")
        self.list_tasks()
        
        try:
            choice = int(input("\nEnter task number to mark as done: "))
            if 1 <= choice <= len(self.tasks["open_tasks"]):
                completed_task = self.tasks["open_tasks"].pop(choice - 1)
                completed_task.update({
                    "completed_at": datetime.now().isoformat(),
                    "status": "completed"
                })
                self.tasks["completed_tasks"].append(completed_task)
                self._save_tasks(self.tasks)
                print(f"\nTask '{completed_task['name']}' marked as done!")
            else:
                print("\nInvalid task number!")
        except ValueError:
            print("\nPlease enter a valid number!")

    def delete_task(self):
        if not self.tasks["open_tasks"]:
            print("\nNo tasks to delete!")
            return

        print("\n=== Delete Task ===")
        self.list_tasks()
        
        try:
            choice = int(input("\nEnter task number to delete: "))
            if 1 <= choice <= len(self.tasks["open_tasks"]):
                deleted_task = self.tasks["open_tasks"].pop(choice - 1)
                self._save_tasks(self.tasks)
                print(f"\nTask '{deleted_task['name']}' deleted!")
            else:
                print("\nInvalid task number!")
        except ValueError:
            print("\nPlease enter a valid number!")

    def show_completed(self):
        print("\n=== COMPLETED TASKS ===\n")
        if not self.tasks["completed_tasks"]:
            print("No completed tasks.")
            return

        for i, task in enumerate(self.tasks["completed_tasks"], 1):
            completed_time = datetime.fromisoformat(task["completed_at"]).strftime("%Y-%m-%d %H:%M")
            print(f"{i}. {task['name']} - Priority: {task['priority']} - Completed: {completed_time}")

    def show_activity_history(self):
        print("\n=== ACTIVITY HISTORY ===\n")
        if not self.tasks["activity_history"]:
            print("No activity history.")
            return

        for i, entry in enumerate(self.tasks["activity_history"], 1):
            timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{i}. {timestamp} - {entry['program']} ({entry['language']})")

if __name__ == "__main__":
    try:
        app = TaskManager()
        app.show_menu()
    except KeyboardInterrupt:
        print(f"\nGoodbye! Made by {AUTHOR}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")