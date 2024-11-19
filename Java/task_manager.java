import java.util.ArrayList;
import java.util.Scanner;

// Class to represent a Task
class Task {
    String name;     // Task name
    String status;   // Task status (pending/completed)
    String priority; // Task priority (High/Medium/Low)

    // Constructor to create a new task
    public Task(String name, String priority) {
        this.name = name;
        this.status = "pending"; // Default status: pending
        this.priority = priority.toLowerCase();
    }

    // Represent the task as a string for display
    @Override
    public String toString() {
        return name + " - " + status + " - Priority: " + priority;
    }
}

// Main class to manage tasks
public class task_manager {
    private static ArrayList<Task> tasks = new ArrayList<>(); // List of tasks
    private static Scanner scanner = new Scanner(System.in); // Scanner for user input

    public static void main(String[] args) {
        while (true) {
            // Display menu
            System.out.println("\nTask Manager");
            System.out.println("1. Add Task");
            System.out.println("2. List Tasks");
            System.out.println("3. Update Task");
            System.out.println("4. Delete Task");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");

            // Read user choice
            int choice = scanner.nextInt();
            scanner.nextLine(); // Consume newline character

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
                    System.out.println("Exiting Task Manager. Goodbye!");
                    return;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }

    // Add a new task
    private static void addTask() {
        System.out.print("Enter task name: ");
        String name = scanner.nextLine();

        System.out.print("Enter task priority (High/Medium/Low): ");
        String priority = scanner.nextLine();

        if (!priority.equalsIgnoreCase("High") &&
            !priority.equalsIgnoreCase("Medium") &&
            !priority.equalsIgnoreCase("Low")) {
            System.out.println("Invalid priority. Please enter High, Medium, or Low.");
            return;
        }

        tasks.add(new Task(name, priority));
        System.out.println("Task '" + name + "' with priority '" + priority + "' added successfully.");
    }

    // List all tasks
    private static void listTasks() {
        if (tasks.isEmpty()) {
            System.out.println("No tasks to display.");
            return;
        }

        for (int i = 0; i < tasks.size(); i++) {
            System.out.println((i + 1) + ". " + tasks.get(i));
        }
    }

    // Update a task
    private static void updateTask() {
        listTasks();

        System.out.print("Enter task number to update: ");
        int taskNumber = scanner.nextInt();
        scanner.nextLine(); // Consume newline character

        if (taskNumber < 1 || taskNumber > tasks.size()) {
            System.out.println("Invalid task number.");
            return;
        }

        Task task = tasks.get(taskNumber - 1);

        System.out.print("Enter new status (pending/completed): ");
        String status = scanner.nextLine();

        if (!status.equalsIgnoreCase("pending") && !status.equalsIgnoreCase("completed")) {
            System.out.println("Invalid status. Please enter pending or completed.");
            return;
        }

        task.status = status.toLowerCase();
        System.out.println("Task " + taskNumber + " updated to '" + status + "'.");
    }

    // Delete a task
    private static void deleteTask() {
        listTasks();

        System.out.print("Enter task number to delete: ");
        int taskNumber = scanner.nextInt();
        scanner.nextLine(); // Consume newline character

        if (taskNumber < 1 || taskNumber > tasks.size()) {
            System.out.println("Invalid task number.");
            return;
        }

        Task removedTask = tasks.remove(taskNumber - 1);
        System.out.println("Task '" + removedTask.name + "' deleted successfully.");
    }
}
