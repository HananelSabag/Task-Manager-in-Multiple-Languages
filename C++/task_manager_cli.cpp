#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>
#include <chrono>
#include <ctime>
#include <csignal>
#include "json.hpp"

/**
 * Task Manager CLI Implementation
 * A command-line interface for managing tasks with history tracking.
 * Author: Hananel Sabag
 */

using json = nlohmann::json;
using namespace std;
namespace fs = std::filesystem;

// Global constants for file and program configuration
const string DATA_DIR = "../data";
const string TASKS_FILE = DATA_DIR + "/DB_task_manager.json";
const string SIGNATURE = "TaskManager";
const string LANGUAGE = "(CPP-CLI Version)";
const string AUTHOR = "Hananel Sabag";

// Global pointer for signal handler
class TaskManager;
TaskManager* globalTaskManager = nullptr;

class TaskManager {
private:
    json tasks;

    /**
     * Load existing tasks file or create new one if doesn't exist
     */
    json loadOrInitTasks() {
        if (!fs::exists(DATA_DIR)) {
            fs::create_directory(DATA_DIR);
        }

        if (!fs::exists(TASKS_FILE)) {
            json initial_data = {
                {"metadata", {
                    {"signature", SIGNATURE},
                    {"language", LANGUAGE},
                    {"last_modified", getCurrentTimestamp()},
                    {"author", AUTHOR}
                }},
                {"open_tasks", json::array()},
                {"completed_tasks", json::array()},
                {"activity_history", json::array()}
            };
            saveTasks(initial_data);
            return initial_data;
        }

        try {
            ifstream file(TASKS_FILE);
            json data = json::parse(file);
            if (validateData(data)) {
                return data;
            }
            throw runtime_error("Invalid data structure");
        }
        catch (...) {
            return loadOrInitTasks();
        }
    }

    /**
     * Validate the JSON data structure
     */
    bool validateData(const json& data) {
        vector<string> required_keys = {"metadata", "open_tasks", "completed_tasks", "activity_history"};
        for (const auto& key : required_keys) {
            if (!data.contains(key)) return false;
        }

        vector<string> metadata_keys = {"signature", "language", "last_modified", "author"};
        for (const auto& key : metadata_keys) {
            if (!data["metadata"].contains(key)) return false;
        }

        return true;
    }

    /**
     * Save tasks to file and update metadata
     */
    void saveTasks(json& data) {
        string timestamp = getCurrentTimestamp();
        data["metadata"]["last_modified"] = timestamp;
        data["metadata"]["language"] = LANGUAGE;
        
        ofstream file(TASKS_FILE, ios::trunc);
        file << setw(4) << data;
        file.close();
    }

    /**
     * Add program exit signature to activity history
     */
    void addExitSignature() {
        string timestamp = getCurrentTimestamp();
        tasks["activity_history"].push_back({
            {"program", "Task Manager"},
            {"language", LANGUAGE},
            {"timestamp", timestamp}
        });
        
        ofstream file(TASKS_FILE, ios::trunc);
        file << setw(4) << tasks;
        file.close();
    }

    /**
     * Get current timestamp in ISO format
     */
    string getCurrentTimestamp() {
        auto now = chrono::system_clock::now();
        auto now_c = chrono::system_clock::to_time_t(now);
        char buffer[30];
        strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%S", localtime(&now_c));
        return string(buffer);
    }

    /**
     * Validate date format and ensure it's not in the past
     */
    bool validateDate(const string& date) {
        if (date.length() != 10) return false;
        if (date[2] != '-' || date[5] != '-') return false;

        try {
            int day = stoi(date.substr(0, 2));
            int month = stoi(date.substr(3, 2));
            int year = stoi(date.substr(6, 4));

            if (month < 1 || month > 12) return false;
            if (day < 1 || day > 31) return false;

            auto now = chrono::system_clock::now();
            auto now_c = chrono::system_clock::to_time_t(now);
            auto current_year = localtime(&now_c)->tm_year + 1900;

            if (year < current_year) return false;

            return true;
        }
        catch (...) {
            return false;
        }
    }

public:
    /**
     * Initialize task manager and set up signal handling
     */
    TaskManager() {
        tasks = loadOrInitTasks();
        globalTaskManager = this;
    }

    /**
     * Cleanup and reset global pointer
     */
    ~TaskManager() {
        globalTaskManager = nullptr;
    }

    /**
     * Handle program exit with signature
     */
    void exitProgram() {
        addExitSignature();
        cout << "\nGoodbye! Made by " << AUTHOR << " " << LANGUAGE << "." << endl;
        exit(0);
    }

    /**
     * Display and handle main menu options
     */
    void showMenu() {
        while (true) {
            cout << "\n=== Task Manager ===\n";
            cout << "1. List Tasks\n";
            cout << "2. Add Task\n";
            cout << "3. Mark Task as Done\n";
            cout << "4. Delete Task\n";
            cout << "5. Show Completed Tasks\n";
            cout << "6. Show Activity History\n";
            cout << "0. Exit\n";

            string choice;
            cout << "\nEnter your choice (0-6): ";
            getline(cin, choice);

            if (choice == "1") listTasks();
            else if (choice == "2") addTask();
            else if (choice == "3") markDone();
            else if (choice == "4") deleteTask();
            else if (choice == "5") showCompleted();
            else if (choice == "6") showActivityHistory();
            else if (choice == "0") {
                exitProgram();
                break;
            }
            else cout << "\nInvalid choice. Please try again.\n";
        }
    }

    /**
     * Display all active tasks
     */
    void listTasks() {
        cout << "\n=== ACTIVE TASKS ===\n\n";
        if (tasks["open_tasks"].empty()) {
            cout << "No active tasks.\n";
            return;
        }

        int i = 1;
        for (const auto& task : tasks["open_tasks"]) {
            cout << i++ << ". " << task["name"] << " - Priority: " 
                 << task["priority"] << " - Deadline: " << task["deadline"] << "\n";
        }
    }

    /**
     * Add a new task with name, priority, and deadline
     */
    void addTask() {
        cout << "\n=== Add New Task ===\n\n";
        
        string name;
        cout << "Enter task name: ";
        getline(cin, name);
        if (name.empty()) {
            cout << "Task name cannot be empty!\n";
            return;
        }

        cout << "\nPriority:\n";
        cout << "1. High\n";
        cout << "2. Medium\n";
        cout << "3. Low\n";
        
        string priority_choice;
        cout << "Choose priority (1-3): ";
        getline(cin, priority_choice);

        string priority = "medium";
        if (priority_choice == "1") priority = "high";
        else if (priority_choice == "3") priority = "low";

        string deadline;
        while (true) {
            cout << "Enter deadline (DD-MM-YYYY): ";
            getline(cin, deadline);
            if (validateDate(deadline)) break;
            cout << "Invalid date format or past date! Please use DD-MM-YYYY\n";
        }

        try {
            json new_task = {
                {"name", name},
                {"priority", priority},
                {"deadline", deadline},
                {"created_at", getCurrentTimestamp()}
            };

            tasks["open_tasks"].push_back(new_task);
            saveTasks(tasks);
            cout << "\nTask added successfully!\n";
        }
        catch (const exception& e) {
            cout << "Error adding task: " << e.what() << endl;
        }
    }

    /**
     * Mark a task as completed and move it to completed tasks
     */
    void markDone() {
        if (tasks["open_tasks"].empty()) {
            cout << "\nNo tasks to mark as done!\n";
            return;
        }

        cout << "\n=== Mark Task as Done ===\n";
        listTasks();

        string choice;
        cout << "\nEnter task number to mark as done: ";
        getline(cin, choice);

        try {
            int idx = stoi(choice) - 1;
            if (idx >= 0 && idx < tasks["open_tasks"].size()) {
                json completed_task = tasks["open_tasks"][idx];
                completed_task["completed_at"] = getCurrentTimestamp();
                completed_task["status"] = "completed";

                tasks["open_tasks"].erase(tasks["open_tasks"].begin() + idx);
                tasks["completed_tasks"].push_back(completed_task);
                saveTasks(tasks);

                cout << "\nTask '" << completed_task["name"] << "' marked as done!\n";
            }
            else {
                cout << "\nInvalid task number!\n";
            }
        }
        catch (...) {
            cout << "\nPlease enter a valid number!\n";
        }
    }

    /**
     * Delete a task from active tasks
     */
    void deleteTask() {
        if (tasks["open_tasks"].empty()) {
            cout << "\nNo tasks to delete!\n";
            return;
        }

        cout << "\n=== Delete Task ===\n";
        listTasks();

        string choice;
        cout << "\nEnter task number to delete: ";
        getline(cin, choice);

        try {
            int idx = stoi(choice) - 1;
            if (idx >= 0 && idx < tasks["open_tasks"].size()) {
                string task_name = tasks["open_tasks"][idx]["name"];
                tasks["open_tasks"].erase(tasks["open_tasks"].begin() + idx);
                saveTasks(tasks);
                cout << "\nTask '" << task_name << "' deleted!\n";
            }
            else {
                cout << "\nInvalid task number!\n";
            }
        }
        catch (...) {
            cout << "\nPlease enter a valid number!\n";
        }
    }

    /**
     * Display all completed tasks
     */
    void showCompleted() {
        cout << "\n=== COMPLETED TASKS ===\n\n";
        if (tasks["completed_tasks"].empty()) {
            cout << "No completed tasks.\n";
            return;
        }

        int i = 1;
        for (auto it = tasks["completed_tasks"].rbegin(); 
             it != tasks["completed_tasks"].rend(); ++it) {
            cout << i++ << ". " << (*it)["name"] 
                 << " - Priority: " << (*it)["priority"]
                 << " - Completed: " << (*it)["completed_at"] << "\n";
        }
    }

    /**
     * Display activity history including program usage
     */
    void showActivityHistory() {
        cout << "\n=== ACTIVITY HISTORY ===\n\n";
        if (tasks["activity_history"].empty()) {
            cout << "No activity history.\n";
            return;
        }

        int i = 1;
        for (auto it = tasks["activity_history"].rbegin(); 
             it != tasks["activity_history"].rend(); ++it) {
            string timestamp = (*it)["timestamp"];
            
            // Remove seconds from timestamp
            if (timestamp.length() > 16) {
                timestamp = timestamp.substr(0, 16);
            }

            cout << i++ << ". " << timestamp 
                 << " - " << (*it)["program"]
                 << " " << (*it)["language"] << "\n";
        }
    }
};

/**
 * Signal handler for Ctrl+C
 */
void signalHandler(int signum) {
    if (globalTaskManager) {
        cout << "\nReceived interrupt signal. Cleaning up...\n";
        globalTaskManager->exitProgram();
    }
    exit(signum);
}

int main() {
    try {
        signal(SIGINT, signalHandler);
        TaskManager app;
        app.showMenu();
    }
    catch (const exception& e) {
        cout << "\nAn unexpected error occurred: " << e.what() << endl;
    }
    return 0;
}