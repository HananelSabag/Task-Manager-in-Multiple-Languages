/*
 * Task Manager CLI Implementation
 * A command-line interface for managing tasks with history tracking.
 * Author: Hananel Sabag
 */

using System;
using System.IO;
using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

public class Program
{
    public static void Main(string[] args)
    {
        try
        {
            var app = new TaskManagerCLI();
            app.ShowMenu();
        }
        catch (Exception e)
        {
            Console.WriteLine($"\nAn unexpected error occurred: {e.Message}");
        }
    }
}


public class TaskManagerCLI
{
    // Global constants for file and program configuration
    private static readonly string DATA_DIR = Path.Combine("..", "data");
    private static readonly string TASKS_FILE = Path.Combine(DATA_DIR, "DB_task_manager.json");
    private static readonly string SIGNATURE = "TaskManager";
    private static readonly string LANGUAGE = "(C#-CLI Version)";
    private static readonly string AUTHOR = "Hananel Sabag";

    private JObject tasks;

    /**
     * Initialize task manager and load tasks
     */
    public TaskManagerCLI()
    {
        tasks = LoadOrInitTasks();
    }

    /**
     * Load existing tasks file or create new one if doesn't exist
     */
    private JObject LoadOrInitTasks()
    {
        if (!Directory.Exists(DATA_DIR))
        {
            Directory.CreateDirectory(DATA_DIR);
        }

        if (!File.Exists(TASKS_FILE))
        {
            var initialData = new JObject
            {
                ["metadata"] = new JObject
                {
                    ["signature"] = SIGNATURE,
                    ["language"] = LANGUAGE,
                    ["last_modified"] = GetCurrentTimestamp(),
                    ["author"] = AUTHOR
                },
                ["open_tasks"] = new JArray(),
                ["completed_tasks"] = new JArray(),
                ["activity_history"] = new JArray()
            };
            SaveTasks(initialData);
            return initialData;
        }

        try
        {
            string content = File.ReadAllText(TASKS_FILE);
            var data = JObject.Parse(content);
            if (ValidateData(data))
            {
                return data;
            }
            throw new Exception("Invalid data structure");
        }
        catch
        {
            return LoadOrInitTasks();
        }
    }

    /**
     * Save tasks to file and update metadata
     */
    private void SaveTasks(JObject data)
    {
        data["metadata"]["last_modified"] = GetCurrentTimestamp();
        data["metadata"]["language"] = LANGUAGE;
        File.WriteAllText(TASKS_FILE, data.ToString(Formatting.Indented));
    }

    /**
     * Add program exit signature to activity history
     */
    private void AddExitSignature()
    {
        var signature = new JObject
        {
            ["program"] = "Task Manager",
            ["language"] = LANGUAGE,
            ["timestamp"] = GetCurrentTimestamp()
        };

        ((JArray)tasks["activity_history"]).Add(signature);
        SaveTasks(tasks);
    }

    /**
     * Validate the JSON data structure
     */
    private bool ValidateData(JObject data)
    {
        string[] requiredKeys = { "metadata", "open_tasks", "completed_tasks", "activity_history" };
        foreach (var key in requiredKeys)
        {
            if (!data.ContainsKey(key)) return false;
        }

        string[] metadataKeys = { "signature", "language", "last_modified", "author" };
        var metadata = data["metadata"] as JObject;
        foreach (var key in metadataKeys)
        {
            if (!metadata.ContainsKey(key)) return false;
        }

        return true;
    }

    /**
     * Get current timestamp in ISO format
     */
    private string GetCurrentTimestamp()
    {
        return DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss");
    }

    /**
     * Validate date format and ensure it's not in the past
     */
    private bool ValidateDate(string date)
    {
        if (!date.Contains("-") || date.Length != 10) return false;

        try
        {
            var parts = date.Split('-');
            if (parts.Length != 3) return false;

            int day = int.Parse(parts[0]);
            int month = int.Parse(parts[1]);
            int year = int.Parse(parts[2]);

            if (month < 1 || month > 12) return false;
            if (day < 1 || day > 31) return false;

            var inputDate = new DateTime(year, month, day);
            if (inputDate.Date < DateTime.Today) return false;

            return true;
        }
        catch
        {
            return false;
        }
    }

    /**
     * Display and handle main menu options
     */
    public void ShowMenu()
    {
        while (true)
        {
            Console.WriteLine("\n=== Task Manager ===");
            Console.WriteLine("1. List Tasks");
            Console.WriteLine("2. Add Task");
            Console.WriteLine("3. Mark Task as Done");
            Console.WriteLine("4. Delete Task");
            Console.WriteLine("5. Show Completed Tasks");
            Console.WriteLine("6. Show Activity History");
            Console.WriteLine("0. Exit");

            Console.Write("\nEnter your choice (0-6): ");
            string choice = Console.ReadLine();

            switch (choice)
            {
                case "1": ListTasks(); break;
                case "2": AddTask(); break;
                case "3": MarkDone(); break;
                case "4": DeleteTask(); break;
                case "5": ShowCompleted(); break;
                case "6": ShowActivityHistory(); break;
                case "0":
                    AddExitSignature();
                    Console.WriteLine($"\nGoodbye! Made by {AUTHOR} {LANGUAGE}");
                    return;
                default:
                    Console.WriteLine("\nInvalid choice. Please try again.");
                    break;
            }
        }
    }

    /**
     * Display all active tasks
     */
    private void ListTasks()
    {
        Console.WriteLine("\n=== ACTIVE TASKS ===\n");
        var openTasks = tasks["open_tasks"] as JArray;

        if (openTasks.Count == 0)
        {
            Console.WriteLine("No active tasks.");
            return;
        }

        int i = 1;
        foreach (var task in openTasks)
        {
            Console.WriteLine($"{i++}. {task["name"]} - Priority: {task["priority"]} - Deadline: {task["deadline"]}");
        }
    }

    /**
     * Add a new task with name, priority, and deadline
     */
    private void AddTask()
    {
        Console.WriteLine("\n=== Add New Task ===\n");

        Console.Write("Enter task name: ");
        string name = Console.ReadLine().Trim();
        if (string.IsNullOrEmpty(name))
        {
            Console.WriteLine("Task name cannot be empty!");
            return;
        }

        Console.WriteLine("\nPriority:");
        Console.WriteLine("1. High");
        Console.WriteLine("2. Medium");
        Console.WriteLine("3. Low");

        Console.Write("Choose priority (1-3): ");
        string priorityChoice = Console.ReadLine();

        string priority = priorityChoice switch
        {
            "1" => "high",
            "3" => "low",
            _ => "medium"
        };

        string deadline;
        while (true)
        {
            Console.Write("Enter deadline (DD-MM-YYYY): ");
            deadline = Console.ReadLine();
            if (ValidateDate(deadline)) break;
            Console.WriteLine("Invalid date format or past date! Please use DD-MM-YYYY");
        }

        try
        {
            var newTask = new JObject
            {
                ["name"] = name,
                ["priority"] = priority,
                ["deadline"] = deadline,
                ["created_at"] = GetCurrentTimestamp()
            };

            ((JArray)tasks["open_tasks"]).Add(newTask);
            SaveTasks(tasks);
            Console.WriteLine("\nTask added successfully!");
        }
        catch (Exception e)
        {
            Console.WriteLine($"Error adding task: {e.Message}");
        }
    }

    /**
     * Mark a task as completed and move it to completed tasks
     */
    private void MarkDone()
    {
        var openTasks = tasks["open_tasks"] as JArray;
        if (openTasks.Count == 0)
        {
            Console.WriteLine("\nNo tasks to mark as done!");
            return;
        }

        Console.WriteLine("\n=== Mark Task as Done ===");
        ListTasks();

        Console.Write("\nEnter task number to mark as done: ");
        if (int.TryParse(Console.ReadLine(), out int choice) && choice > 0 && choice <= openTasks.Count)
        {
            var completedTask = openTasks[choice - 1];
            completedTask["completed_at"] = GetCurrentTimestamp();
            completedTask["status"] = "completed";

            openTasks.RemoveAt(choice - 1);
            ((JArray)tasks["completed_tasks"]).Add(completedTask);
            SaveTasks(tasks);

            Console.WriteLine($"\nTask '{completedTask["name"]}' marked as done!");
        }
        else
        {
            Console.WriteLine("\nInvalid task number!");
        }
    }

    /**
     * Delete a task from active tasks
     */
    private void DeleteTask()
    {
        var openTasks = tasks["open_tasks"] as JArray;
        if (openTasks.Count == 0)
        {
            Console.WriteLine("\nNo tasks to delete!");
            return;
        }

        Console.WriteLine("\n=== Delete Task ===");
        ListTasks();

        Console.Write("\nEnter task number to delete: ");
        if (int.TryParse(Console.ReadLine(), out int choice) && choice > 0 && choice <= openTasks.Count)
        {
            string taskName = openTasks[choice - 1]["name"].ToString();
            openTasks.RemoveAt(choice - 1);
            SaveTasks(tasks);
            Console.WriteLine($"\nTask '{taskName}' deleted!");
        }
        else
        {
            Console.WriteLine("\nInvalid task number!");
        }
    }

    /**
     * Display all completed tasks
     */
    private void ShowCompleted()
    {
        Console.WriteLine("\n=== COMPLETED TASKS ===\n");
        var completedTasks = tasks["completed_tasks"] as JArray;

        if (completedTasks.Count == 0)
        {
            Console.WriteLine("No completed tasks.");
            return;
        }

        int i = 1;
        for (int j = completedTasks.Count - 1; j >= 0; j--)
        {
            var task = completedTasks[j];
            Console.WriteLine($"{i++}. {task["name"]} - Priority: {task["priority"]} - Completed: {task["completed_at"]}");
        }
    }

    /**
     * Display activity history including program usage
     */
    private void ShowActivityHistory()
    {
        Console.WriteLine("\n=== ACTIVITY HISTORY ===\n");
        var history = tasks["activity_history"] as JArray;

        if (history.Count == 0)
        {
            Console.WriteLine("No activity history.");
            return;
        }

        int i = 1;
        for (int j = history.Count - 1; j >= 0; j--)
        {
            var entry = history[j];
            string timestamp = entry["timestamp"].ToString();
            
            // Remove seconds from timestamp
            if (timestamp.Length > 16)
            {
                timestamp = timestamp.Substring(0, 16);
            }

            Console.WriteLine($"{i++}. {timestamp} - {entry["program"]} {entry["language"]}");
        }
    }
}