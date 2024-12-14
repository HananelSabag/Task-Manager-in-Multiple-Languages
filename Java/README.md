# Java Task Manager

A Java implementation of the task manager with a CLI interface.

## Features
- CLI implementation with interactive menu
- Priority management (High/Medium/Low)
- Deadline validation
- Activity history tracking
- Completed tasks tracking
- Cross-language JSON compatibility

## Requirements
```
Java 17 or higher
Gson library (for JSON handling)
```

## Installation
1. Install Java JDK 17+:
   ```
   https://www.oracle.com/java/technologies/downloads/
   ```
2. Add Gson dependency:
   ```xml
   <dependency>
       <groupId>com.google.code.gson</groupId>
       <artifactId>gson</artifactId>
       <version>2.10.1</version>
   </dependency>
   ```

## Compilation
```bash
javac -cp gson-2.10.1.jar TaskManagerCLI.java
```

## Usage
```bash
java -cp .:gson-2.10.1.jar TaskManagerCLI
```

## Implementation Details
- Modern Java features (Switch expressions, Text blocks)
- JSON data structure support
- Input validation and error handling
- Cross-platform compatibility
- Activity tracking between versions

## File Structure
- `TaskManagerCLI.java`: Main implementation
- `data/DB_task_manager.json`: Shared data storage

## Author
Created by Hananel Sabag