# Task Manager in Multiple Languages

A comprehensive task management application implemented across multiple programming languages, demonstrating cross-language data sharing and different programming approaches.

## Overview
This project implements a task manager application with command-line interfaces in multiple languages:
- Python (CLI + GUI)
- C++ (CLI)
- C (CLI)
- Java (CLI)
- C# (CLI)
*(More languages planned)*

## Features
- Task Management (Add, Delete, Complete)
- Priority Levels (High/Medium/Low)
- Deadline Management
- Activity History
- Completion Tracking
- Cross-Language JSON Data Compatibility
- Signal Handling (Ctrl+C)
- Standardized Exit Signatures

## Project Structure
```
Task-Manager-in-Multiple-Languages/
├── Python/                   # Python implementation
│   ├── task_manager_gui.py  # GUI version
│   ├── task_manager_cli.py  # CLI version
│   └── README.md            # Python documentation
├── C++/                     # C++ implementation
│   ├── json.hpp            # JSON library
│   ├── task_manager_cli.cpp
│   └── README.md           # C++ documentation
├── C/                      # C implementation
│   ├── cJSON.h            # JSON library header
│   ├── cJSON.c            # JSON library source
│   ├── task_manager_cli.c
│   ├── task_manager_cli.h
│   └── README.md          # C documentation
├── Java/                    # Java implementation
│   ├── task_manager_cli.java
│   ├── lib/gson-2.10.1.jar # JSON library for Java
│   └── README.md           # Java documentation
├── C#/                     # C# implementation
│   ├── task_manager_cli.cs
│   └── README.md           # C# documentation
├── .vscode/                # VS Code configuration
│   ├── launch.json
│   ├── tasks.json
│   └── settings.json
├── data/                    # Shared data directory
│   └── DB_task_manager.json
└── README.md               # Project overview
```

## Data Storage & Compatibility
All implementations share a common JSON data format stored in `data/DB_task_manager.json`, enabling seamless cross-language compatibility. Each version can:
- Read and write to the shared JSON file
- Track activity history across all versions
- Maintain consistent data structures
- Handle tasks created by other language versions

## Implementation Details
- Cross-platform compatibility (Windows, Linux, MacOS)
- Consistent JSON data format across all languages
- Activity history tracking between all versions
- Robust file validation and error handling
- Exit signature tracking system
- Standardized date format (DD-MM-YYYY)
- Memory management appropriate for each language
- Signal handling for graceful exits

## JSON Libraries Used
- Python: Built-in json module
- C++: nlohmann/json
- C: cJSON
- Java: Gson
- C#: Newtonsoft.Json

## Building and Running:

### Using VS Code
The project includes pre-configured `launch.json` and `tasks.json` files to simplify compilation and debugging across all language versions. Simply open the project in VS Code and use the provided build and debug tasks.

### Manual Build
Each language implementation includes its own README with specific build instructions:
- Python: Requires Python 3.x
- C++: Requires C++17 compiler
- C: Requires C11 compiler
- Java: Requires JDK 17+ and Gson
- C#: Requires .NET SDK 7.0+

## Author
Created by Hananel Sabag