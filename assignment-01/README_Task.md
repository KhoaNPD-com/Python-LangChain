# Command-Line Task Manager

A simple, lightweight Python-based command-line task manager that allows users to add, view, complete, and delete tasks directly from a scripted command list.

---

## Features

- **Add Tasks**: Automatically assigns unique sequential IDs to new tasks.
- **View Tasks**: Lists all current tasks along with their real-time status (`Pending` or `Done`).
- **Mark Complete**: Updates a task's status to completed using its unique ID.
- **Delete Tasks**: Removes tasks securely from the list by ID.
- **Error Handling**: Gracefully handles invalid task IDs, missing descriptions, and unknown commands.
- **Automated Command Runner**: Executes predefined sequences of commands for automated testing and demonstration.

---

## Code Structure

- **Core Functions**:
  - `add_task(description)`: Creates and appends a new task dictionary with an auto-incremented ID.
  - `view_tasks()`: Displays all existing tasks and their completion status.
  - `mark_completed(task_id)`: Finds a task by ID and marks it as completed.
  - `delete_task(task_id)`: Removes a task by ID.
- **Command Processor**:
  - `process_command(command)`: Parses incoming tuples, maps them to the appropriate core functions, and handles validation errors.
- **Main Runner**:
  - `main(commands)`: Iterates through the command queue and controls program flow.

---

## Getting Started

### Prerequisites
Make sure you have Python installed on your system (Python 3.x recommended).

### Running the Script
1. Save the code into a file, for example, `task_manager.py`.
2. Run the script using your terminal or command prompt:

```bash
python task_manager.py