# C++ Task Manager

A C++ implementation of the task manager with a CLI interface.

## Features
- CLI implementation with interactive menu
- Priority management (High/Medium/Low)
- Deadline validation
- Activity history tracking
- Completed tasks tracking
- Cross-language JSON compatibility

## Requirements
```
C++17 or higher
G++ compiler
nlohmann/json library (included)
```

## Installation
1. Install MinGW-w64 with GCC compiler:
   ```
   https://www.mingw-w64.org/downloads/
   ```
2. Add MinGW bin directory to system PATH
3. Verify installation:
   ```
   g++ --version
   ```

## Compilation
```bash
g++ -std=c++17 -o task_manager_cli.exe task_manager_cli.cpp
```

## Usage
```bash
./task_manager_cli
```

## Implementation Details
- Modern C++17 features
- File system operations
- JSON data structure support
- Input validation
- Error handling
- Cross-platform compatibility
- Activity tracking between versions

## File Structure
- `task_manager_cli.cpp`: Main implementation
- `json.hpp`: JSON library header
- `data/DB_task_manager.json`: Shared data storage

## Author
Created by Hananel Sabag