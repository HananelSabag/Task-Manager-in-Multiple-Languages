import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
TASKS_FILE = os.path.join(DATA_DIR, "DB_task_manager.json")
SIGNATURE = "TaskManager"
LANGUAGE = "Python-GUI"
AUTHOR = "Hananel Sabag"

class TaskManagerApp:
    def __init__(self, root):

        if not os.path.exists(DATA_DIR):
               os.makedirs(DATA_DIR)

        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x700")
        self.tasks = self._load_or_init_tasks()
        self._setup_gui()

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

    def _setup_gui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="Task Manager",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Task List with Scrollbar
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_list = tk.Listbox(
            list_frame, 
            width=60, 
            height=20,
            yscrollcommand=scrollbar.set
        )
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_list.yview)

        # Buttons Frame
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=5)

        buttons = [
            ("Add Task", self.add_task_dialog),
            ("Mark Done", self.mark_done),
            ("Delete", self.delete_task),
            ("Show Completed", self.show_completed),
            ("Show History", self.show_activity_history)
        ]

        for text, command in buttons:
            tk.Button(
                buttons_frame, 
                text=text, 
                command=command, 
                width=15
            ).pack(side=tk.LEFT, padx=5)

        # Footer
        footer = tk.Label(
            self.root,
            text=f"Made by {AUTHOR}",
            font=("Arial", 10),
            fg="gray"
        )
        footer.pack(side=tk.BOTTOM, pady=10)

        self.refresh_list()

    def refresh_list(self):
        self.task_list.delete(0, tk.END)
        self.task_list.insert(tk.END, "=== ACTIVE TASKS ===")
        self.task_list.insert(tk.END, "")
        
        for i, task in enumerate(self.tasks["open_tasks"], 1):
            self.task_list.insert(tk.END, 
                f"{i}. {task['name']} - Priority: {task['priority']} - Deadline: {task['deadline']}")

    def add_task_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Task")
        dialog.geometry("300x500")
        dialog.grab_set()
        dialog.transient(self.root)

        content_frame = tk.Frame(dialog)
        content_frame.pack(expand=True, fill='both', padx=20, pady=10)

        tk.Label(content_frame, text="Task Name:").pack(pady=5)
        name_entry = tk.Entry(content_frame, width=30)
        name_entry.pack(pady=5)

        tk.Label(content_frame, text="Priority:").pack(pady=5)
        priority_var = tk.StringVar(value="medium")
        for priority in ["high", "medium", "low"]:
            tk.Radiobutton(
                content_frame,
                text=priority.title(),
                value=priority,
                variable=priority_var
            ).pack()

        tk.Label(content_frame, text="Deadline:").pack(pady=5)
        today = datetime.now().date()
        cal = Calendar(content_frame, mindate=today, date_pattern='dd-mm-yyyy')
        cal.pack(pady=5)

        button_frame = tk.Frame(dialog)
        button_frame.pack(side=tk.BOTTOM, pady=15)

        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Task name is required!")
                return

            new_task = {
                "name": name,
                "priority": priority_var.get(),
                "deadline": cal.get_date(),
                "created_at": datetime.now().isoformat()
            }
            
            self.tasks["open_tasks"].append(new_task)
            self._save_tasks(self.tasks)
            self.refresh_list()
            dialog.destroy()
            messagebox.showinfo("Success", "Task added successfully!")

        tk.Button(
            button_frame, 
            text="Save Task", 
            command=save, 
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, 
            text="Cancel", 
            command=dialog.destroy, 
            width=15
        ).pack(side=tk.LEFT, padx=5)

    def mark_done(self):
        selection = self.task_list.curselection()
        if not selection or selection[0] <= 1:
            messagebox.showwarning("Warning", "Please select a task")
            return

        task_idx = selection[0] - 2
        completed_task = self.tasks["open_tasks"].pop(task_idx)
        completed_task.update({
            "completed_at": datetime.now().isoformat(),
            "status": "completed"
        })
        
        self.tasks["completed_tasks"].append(completed_task)
        self._save_tasks(self.tasks)
        self.refresh_list()
        messagebox.showinfo("Success", f"Task '{completed_task['name']}' completed!")

    def delete_task(self):
        selection = self.task_list.curselection()
        if not selection or selection[0] <= 1:
            messagebox.showwarning("Warning", "Please select a task")
            return

        task_idx = selection[0] - 2
        deleted_task = self.tasks["open_tasks"].pop(task_idx)
        self._save_tasks(self.tasks)
        self.refresh_list()
        messagebox.showinfo("Success", f"Task '{deleted_task['name']}' deleted!")

    def show_completed(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Completed Tasks")
        dialog.geometry("400x300")
        dialog.grab_set()
        dialog.transient(self.root)

        frame = tk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        completed_list = tk.Listbox(
            frame, 
            width=50, 
            height=15,
            yscrollcommand=scrollbar.set
        )
        completed_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=completed_list.yview)

        completed_list.insert(tk.END, "=== COMPLETED TASKS ===")
        completed_list.insert(tk.END, "")

        for i, task in enumerate(reversed(self.tasks["completed_tasks"]), 1):
            completed_time = datetime.fromisoformat(task["completed_at"]).strftime("%Y-%m-%d %H:%M")
            completed_list.insert(tk.END, 
                f"{i}. {task['name']} - Priority: {task['priority']} - Completed: {completed_time}")

        tk.Button(dialog, text="Close", command=dialog.destroy, width=10).pack(pady=5)

    def show_activity_history(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Activity History")
        dialog.geometry("500x400")
        dialog.grab_set()
        dialog.transient(self.root)

        frame = tk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        history_list = tk.Listbox(
            frame, 
            width=60, 
            height=20,
            yscrollcommand=scrollbar.set
        )
        history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_list.yview)

        history_list.insert(tk.END, "=== ACTIVITY HISTORY ===")
        history_list.insert(tk.END, "")

        for i, entry in enumerate(reversed(self.tasks["activity_history"]), 1):
            timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            history_list.insert(tk.END, 
                f"{i}. {timestamp} - {entry['program']} ({entry['language']})")

        tk.Button(dialog, text="Close", command=dialog.destroy, width=10).pack(pady=5)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TaskManagerApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")