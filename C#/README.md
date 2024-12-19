# C# Task Manager

A C# implementation of the task manager with a CLI interface.

## Features
- CLI implementation with interactive menu
- Priority management (High/Medium/Low)
- Deadline validation
- Activity history tracking
- Completed tasks tracking
- Cross-language JSON data compatibility

## Requirements Installation Guide

### 1. Install .NET SDK
1. Visit: https://dotnet.microsoft.com/download/dotnet/7.0
2. Download ".NET SDK 7.0.x (Windows x64)"
3. Run the installer
4. Open a new terminal/PowerShell and verify installation:
   ```bash
   dotnet --version   # Should show 7.x.x
   ```

### 2. Project Setup
1. Ensure you're in the C# directory
2. Create project file `task_manger_cli.csproj`:
   ```xml
   <Project Sdk="Microsoft.NET.Sdk">
     <PropertyGroup>
       <OutputType>Exe</OutputType>
       <TargetFramework>net7.0</TargetFramework>
     </PropertyGroup>
     <ItemGroup>
       <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
     </ItemGroup>
   </Project>
   ```
3. Restore packages:
   ```bash
   dotnet restore
   ```

## Building & Running
1. Build the project:
   ```bash
   dotnet build
   ```

2. Run the application:
   ```bash
   dotnet run
   ```

## File Structure
```
C#/
├── task_manger_cli.cs     # Main implementation
├── task_manger_cli.csproj # Project configuration
└── README.md             # This file
```

## Common Issues & Solutions
1. If `dotnet` command not found:
   - Restart your terminal after installation
   - Ensure PATH environment variable is set

2. If build fails with JSON errors:
   ```bash
   dotnet restore    # Try restoring packages first
   dotnet build     # Then build again
   ```

3. If file not found errors:
   - Ensure file names match exactly (case sensitive)
   - Check you're in the right directory

## Author
Created by Hananel Sabag