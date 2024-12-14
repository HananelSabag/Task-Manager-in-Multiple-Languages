/**
 * Task Manager CLI Implementation
 * A command-line interface for managing tasks with history tracking.
 * Author: Hananel Sabag
 */

import com.google.gson.*;
import java.io.*;
import java.nio.file.*;
import java.time.*;
import java.time.format.*;
import java.util.*;

public class TaskManagerCLI {
    // Global constants for file and program configuration
    private static final String DATA_DIR = "../data";
    private static final String TASKS_FILE = DATA_DIR + "/DB_task_manager.json";
    private static final String SIGNATURE = "TaskManager";
    private static final String LANGUAGE = "(Java-CLI Version)";
    private static final String AUTHOR = "Hananel Sabag";
    
    private final Gson gson;
    private JsonObject tasks;
    private final Scanner scanner;

    /**
     * Initialize task manager with JSON parser and input scanner
     */
    public TaskManagerCLI() {
        gson = new GsonBuilder().setPrettyPrinting().create();
        scanner = new Scanner(System.in);
        tasks = loadOrInitTasks();
    }

    /**
     * Load existing tasks file or create new one if doesn't exist
     */
    private JsonObject loadOrInitTasks() {
        try {
            Files.createDirectories(Paths.get(DATA_DIR));
            
            if (!Files.exists(Paths.get(TASKS_FILE))) {
                JsonObject initial = new JsonObject();
                JsonObject metadata = new JsonObject();
                metadata.addProperty("signature", SIGNATURE);
                metadata.addProperty("language", LANGUAGE);
                metadata.addProperty("last_modified", getCurrentTimestamp());
                metadata.addProperty("author", AUTHOR);

                initial.add("metadata", metadata);
                initial.add("open_tasks", gson.toJsonTree(new ArrayList<>()));
                initial.add("completed_tasks", gson.toJsonTree(new ArrayList<>()));
                initial.add("activity_history", gson.toJsonTree(new ArrayList<>()));

                saveTasks(initial);
                return initial;
            }

            String content = Files.readString(Paths.get(TASKS_FILE));
            JsonObject data = gson.fromJson(content, JsonObject.class);
            if (validateData(data)) {
                return data;
            }
            throw new IllegalStateException("Invalid data structure");
        } catch (Exception e) {
            return loadOrInitTasks();
        }
    }

    /**
     * Save tasks to file and update metadata
     */
    private void saveTasks(JsonObject data) {
        try {
            data.getAsJsonObject("metadata").addProperty("last_modified", getCurrentTimestamp());
            data.getAsJsonObject("metadata").addProperty("language", LANGUAGE);
            
            Files.writeString(Paths.get(TASKS_FILE), gson.toJson(data));
        } catch (IOException e) {
            System.out.println("Error saving tasks: " + e.getMessage());
        }
    }

    /**
     * Add program exit signature to activity history
     */
    private void addExitSignature() {
        JsonObject signature = new JsonObject();
        signature.addProperty("program", "Task Manager");
        signature.addProperty("language", LANGUAGE);
        signature.addProperty("timestamp", getCurrentTimestamp());

        tasks.getAsJsonArray("activity_history").add(signature);
        saveTasks(tasks);
    }

    /**
     * Validate the JSON data structure
     */
    private boolean validateData(JsonObject data) {
        String[] requiredKeys = {"metadata", "open_tasks", "completed_tasks", "activity_history"};
        for (String key : requiredKeys) {
            if (!data.has(key)) return false;
        }

        String[] metadataKeys = {"signature", "language", "last_modified", "author"};
        JsonObject metadata = data.getAsJsonObject("metadata");
        for (String key : metadataKeys) {
            if (!metadata.has(key)) return false;
        }

        return true;
    }

    /**
     * Get current timestamp in ISO format
     */
    private String getCurrentTimestamp() {
        return LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
    }

    /**
     * Validate date format and ensure it's not in the past
     */
    private boolean validateDate(String date) {
        try {
            if (!date.matches("\\d{2}-\\d{2}-\\d{4}")) return false;

            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd-MM-yyyy");
            LocalDate inputDate = LocalDate.parse(date, formatter);
            LocalDate today = LocalDate.now();

            return !inputDate.isBefore(today);
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * Display and handle main menu options
     */
    public void showMenu() {
        while (true) {
            System.out.println("\n=== Task Manager ===");
            System.out.println("1. List Tasks");
            System.out.println("2. Add Task");
            System.out.println("3. Mark Task as Done");
            System.out.println("4. Delete Task");
            System.out.println("5. Show Completed Tasks");
            System.out.println("6. Show Activity History");
            System.out.println("0. Exit");

            System.out.print("\nEnter your choice (0-6): ");
            String choice = scanner.nextLine();

            switch (choice) {
                case "1" -> listTasks();
                case "2" -> addTask();
                case "3" -> markDone();
                case "4" -> deleteTask();
                case "5" -> showCompleted();
                case "6" -> showActivityHistory();
                case "0" -> {
                    addExitSignature();
                    System.out.println("\nGoodbye! Made by " + AUTHOR + " " + LANGUAGE);
                    return;
                }
                default -> System.out.println("\nInvalid choice. Please try again.");
            }
        }
    }

    /**
     * Display all active tasks
     */
    private void listTasks() {
        System.out.println("\n=== ACTIVE TASKS ===\n");
        JsonArray openTasks = tasks.getAsJsonArray("open_tasks");
        
        if (openTasks.isEmpty()) {
            System.out.println("No active tasks.");
            return;
        }

        int i = 1;
        for (JsonElement taskElement : openTasks) {
            JsonObject task = taskElement.getAsJsonObject();
            System.out.printf("%d. %s - Priority: %s - Deadline: %s\n",
                i++,
                task.get("name").getAsString(),
                task.get("priority").getAsString(),
                task.get("deadline").getAsString());
        }
    }

    /**
     * Add a new task with name, priority, and deadline
     */
    private void addTask() {
        System.out.println("\n=== Add New Task ===\n");
        
        System.out.print("Enter task name: ");
        String name = scanner.nextLine().trim();
        if (name.isEmpty()) {
            System.out.println("Task name cannot be empty!");
            return;
        }

        System.out.println("\nPriority:");
        System.out.println("1. High");
        System.out.println("2. Medium");
        System.out.println("3. Low");
        
        System.out.print("Choose priority (1-3): ");
        String priorityChoice = scanner.nextLine();

        String priority = switch (priorityChoice) {
            case "1" -> "high";
            case "3" -> "low";
            default -> "medium";
        };

        String deadline;
        while (true) {
            System.out.print("Enter deadline (DD-MM-YYYY): ");
            deadline = scanner.nextLine();
            if (validateDate(deadline)) break;
            System.out.println("Invalid date format or past date! Please use DD-MM-YYYY");
        }

        try {
            JsonObject newTask = new JsonObject();
            newTask.addProperty("name", name);
            newTask.addProperty("priority", priority);
            newTask.addProperty("deadline", deadline);
            newTask.addProperty("created_at", getCurrentTimestamp());

            tasks.getAsJsonArray("open_tasks").add(newTask);
            saveTasks(tasks);
            System.out.println("\nTask added successfully!");
        } catch (Exception e) {
            System.out.println("Error adding task: " + e.getMessage());
        }
    }

    /**
     * Mark a task as completed and move it to completed tasks
     */
    private void markDone() {
        if (tasks.getAsJsonArray("open_tasks").isEmpty()) {
            System.out.println("\nNo tasks to mark as done!");
            return;
        }

        System.out.println("\n=== Mark Task as Done ===");
        listTasks();

        System.out.print("\nEnter task number to mark as done: ");
        try {
            int idx = Integer.parseInt(scanner.nextLine()) - 1;
            JsonArray openTasks = tasks.getAsJsonArray("open_tasks");
            
            if (idx >= 0 && idx < openTasks.size()) {
                JsonObject completedTask = openTasks.get(idx).getAsJsonObject();
                completedTask.addProperty("completed_at", getCurrentTimestamp());
                completedTask.addProperty("status", "completed");

                openTasks.remove(idx);
                tasks.getAsJsonArray("completed_tasks").add(completedTask);
                saveTasks(tasks);

                System.out.println("\nTask '" + completedTask.get("name").getAsString() + "' marked as done!");
            } else {
                System.out.println("\nInvalid task number!");
            }
        } catch (NumberFormatException e) {
            System.out.println("\nPlease enter a valid number!");
        }
    }

    /**
     * Delete a task from active tasks
     */
    private void deleteTask() {
        if (tasks.getAsJsonArray("open_tasks").isEmpty()) {
            System.out.println("\nNo tasks to delete!");
            return;
        }

        System.out.println("\n=== Delete Task ===");
        listTasks();

        System.out.print("\nEnter task number to delete: ");
        try {
            int idx = Integer.parseInt(scanner.nextLine()) - 1;
            JsonArray openTasks = tasks.getAsJsonArray("open_tasks");
            
            if (idx >= 0 && idx < openTasks.size()) {
                String taskName = openTasks.get(idx).getAsJsonObject().get("name").getAsString();
                openTasks.remove(idx);
                saveTasks(tasks);
                System.out.println("\nTask '" + taskName + "' deleted!");
            } else {
                System.out.println("\nInvalid task number!");
            }
        } catch (NumberFormatException e) {
            System.out.println("\nPlease enter a valid number!");
        }
    }

    /**
     * Display all completed tasks
     */
    private void showCompleted() {
        System.out.println("\n=== COMPLETED TASKS ===\n");
        JsonArray completedTasks = tasks.getAsJsonArray("completed_tasks");
        
        if (completedTasks.isEmpty()) {
            System.out.println("No completed tasks.");
            return;
        }

        int i = 1;
        for (int j = completedTasks.size() - 1; j >= 0; j--) {
            JsonObject task = completedTasks.get(j).getAsJsonObject();
            System.out.printf("%d. %s - Priority: %s - Completed: %s\n",
                i++,
                task.get("name").getAsString(),
                task.get("priority").getAsString(),
                task.get("completed_at").getAsString());
        }
    }

    /**
     * Display activity history including program usage
     */
    private void showActivityHistory() {
        System.out.println("\n=== ACTIVITY HISTORY ===\n");
        JsonArray history = tasks.getAsJsonArray("activity_history");
        
        if (history.isEmpty()) {
            System.out.println("No activity history.");
            return;
        }

        int i = 1;
        for (int j = history.size() - 1; j >= 0; j--) {
            JsonObject entry = history.get(j).getAsJsonObject();
            String timestamp = entry.get("timestamp").getAsString();
            
            // Remove seconds from timestamp
            if (timestamp.length() > 16) {
                timestamp = timestamp.substring(0, 16);
            }
            
            System.out.printf("%d. %s - %s %s\n",
                i++,
                timestamp,
                entry.get("program").getAsString(),
                entry.get("language").getAsString());
        }
    }

    public static void main(String[] args) {
        try {
            TaskManagerCLI app = new TaskManagerCLI();
            app.showMenu();
        } catch (Exception e) {
            System.out.println("\nAn unexpected error occurred: " + e.getMessage());
        }
    }
}
