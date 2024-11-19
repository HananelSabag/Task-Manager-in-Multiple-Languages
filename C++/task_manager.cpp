#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

// Class to represent a Task
class Task {
public:
    string name;     // Task name
    string status;   // Task status (pending/completed)
    string priority; // Task priority (High/Medium/Low)

    // Constructor
    Task(string name, string priority) {
        this->name = name;
        this->status = "pending";
        this->priority = priority;
    }

    // Represent task as a string for display
    string toString() const {
        return name + " - " + status + " - Priority: " + priority;
    }
};

// Vector to store tasks
vector<Task> tasks;

// Function to add a new task
void addTask() {
    string name, priority;
    cout << "Enter task name: ";
    cin.ignore(); // Clear newline character from input buffer
    getline(cin, name);

    cout << "Enter task priority (High/Medium/Low): ";
    getline(cin, priority);

    if (priority != "High" && priority != "Medium" && priority != "Low" && priority != "high" && priority != "medium" && priority != "low") {
        cout << "Invalid priority. Please enter High, Medium, or Low." << endl;
        return;
    }

    tasks.emplace_back(name, priority);
    cout << "Task '" << name << "' with priority '" << priority << "' added successfully." << endl;
}

// Function to list all tasks
void listTasks() {
    if (tasks.empty()) {
        cout << "No tasks to display." << endl;
        return;
    }

    for (size_t i = 0; i < tasks.size(); ++i) {
        cout << (i + 1) << ". " << tasks[i].toString() << endl;
    }
}

// Function to update a task
void updateTask() {
    listTasks();

    cout << "Enter task number to update: ";
    size_t taskNumber;
    cin >> taskNumber;

    if (taskNumber < 1 || taskNumber > tasks.size()) {
        cout << "Invalid task number." << endl;
        return;
    }

    string status;
    cout << "Enter new status (pending/completed): ";
    cin >> status;

    if (status != "pending" && status != "completed") {
        cout << "Invalid status. Please enter pending or completed." << endl;
        return;
    }

    tasks[taskNumber - 1].status = status;
    cout << "Task " << taskNumber << " updated to '" << status << "'." << endl;
}

// Function to delete a task
void deleteTask() {
    listTasks();

    size_t taskNumber;
    cout << "Enter task number to delete: ";

    while (true) {
        cin >> taskNumber;

        // Check if the input is valid
        if (cin.fail()) {
            // Clear the error flag
            cin.clear();
            // Ignore invalid input
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Invalid input. Please enter a valid task number: ";
        } else if (taskNumber < 1 || taskNumber > tasks.size()) {
            cout << "Invalid task number. Please enter a number between 1 and " << tasks.size() << ": ";
        } else {
            break; // Input is valid, exit the loop
        }
    }

    cout << "Task '" << tasks[taskNumber - 1].name << "' deleted successfully." << endl;
    tasks.erase(tasks.begin() + taskNumber - 1);
}


// Main function
int main() {
    while (true) {
        // Display menu
        cout << "\nTask Manager" << endl;
        cout << "1. Add Task" << endl;
        cout << "2. List Tasks" << endl;
        cout << "3. Update Task" << endl;
        cout << "4. Delete Task" << endl;
        cout << "5. Exit" << endl;
        cout << "Enter your choice: ";

        int choice;
        cin >> choice;

        // Handle user choice
        switch (choice) {
            case 1:
                addTask();
                break;
            case 2:
                listTasks();
                break;
            case 3:
                updateTask();
                break;
            case 4:
                deleteTask();
                break;
            case 5:
                cout << "Exiting Task Manager. Goodbye!" << endl;
                return 0;
            default:
                cout << "Invalid choice. Please try again." << endl;
        }
    }
}
