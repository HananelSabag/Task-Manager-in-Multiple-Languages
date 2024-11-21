# Task Manager in Multiple Languages

A comprehensive task management application implemented across multiple programming languages, demonstrating cross-language data sharing and different programming approaches.

## Overview
This project implements a task manager application with command-line interfaces in multiple languages:
- Python (CLI + GUI)
- C++ (CLI)
- Java (CLI)
*(More languages planned)*

## Features
- Task Management (Add, Delete, Complete)
- Priority Levels (High/Medium/Low)
- Deadline Management
- Activity History
- Completion Tracking
- Cross-Language JSON Data Compatibility

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
├── Java/                    # Java implementation
│   ├── task_manager_cli.java
│   └── README.md           # Java documentation
├── data/                    # Shared data directory
│   └── DB_task_manager.json
└── README.md               # Project overview
```

## Data Storage
All implementations share a common JSON data format stored in `data/DB_task_manager.json`, enabling seamless cross-language compatibility and consistent task management.

## Implementation Details
- Cross-platform compatibility
- Consistent data format across languages
- Activity history tracking between versions
- Robust file validation and error handling
- Exit signature tracking system
- Standardized date format (DD-MM-YYYY)

## Author
Created by Hananel Sabag