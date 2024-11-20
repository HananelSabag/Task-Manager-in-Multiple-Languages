# Python Task Manager

A Python implementation of the task manager with both GUI and CLI interfaces.

## Features
- GUI implementation using tkinter
- CLI implementation with interactive menu
- Calendar-based deadline selection
- Priority management (High/Medium/Low)
- Activity history tracking
- Completed tasks tracking

## Requirements
```
Python 3.x
tkcalendar (for GUI version)
```

## Installation
```bash
pip install tkcalendar
```

## Usage
### GUI Version
```bash
python task_manager_gui.py
```

### CLI Version
```bash
python task_manager_cli.py
```

## Implementation Details
- GUI: Uses tkinter for interface, tkcalendar for date selection
- CLI: Console-based interactive menu
- Both versions share common JSON data structure
- Input validation and error handling
- Activity tracking between versions

## File Structure
- `task_manager_gui.py`: GUI implementation
- `task_manager_cli.py`: CLI implementation
- `tasks.json`: Shared data storage

## Author
Created by Hananel Sabag
