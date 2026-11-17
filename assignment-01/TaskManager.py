# ---------------------------
# Command-Line Task Manager
# ---------------------------

tasks = []


# ---------------------------
# Core Functions
# ---------------------------

def add_task(description):
    task_id = tasks[-1]["id"] + 1 if tasks else 1

    task = {
        "id": task_id,
        "description": description,
        "completed": False
    }

    tasks.append(task)
    print(f"[ADD] Task '{description}' added with ID {task_id}")


def view_tasks():
    print("\n--- TASK LIST ---")

    if not tasks:
        print("No tasks available.\n")
        return

    for task in tasks:
        status = "Done" if task["completed"] else "Pending"
        print(f"{task['id']}. {task['description']} [{status}]")

    print()


def mark_completed(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            print(f"[COMPLETE] Task {task_id} marked as completed")
            return

    print(f"[ERROR] Task {task_id} not found")


def delete_task(task_id):
    global tasks

    before = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]

    if len(tasks) < before:
        print(f"[DELETE] Task {task_id} deleted")
    else:
        print(f"[ERROR] Task {task_id} not found")


# ---------------------------
# Command Processor
# ---------------------------

def process_command(command):
    action = command[0]

    if action == "add":
        if len(command) > 1:
            add_task(command[1])
        else:
            print("[ERROR] Missing description")

    elif action == "view":
        view_tasks()

    elif action == "complete":
        if len(command) > 1:
            try:
                task_id = int(command[1])
                mark_completed(task_id)
            except ValueError:
                print("[ERROR] Invalid task ID")
        else:
            print("[ERROR] Missing task ID")

    elif action == "delete":
        if len(command) > 1:
            try:
                task_id = int(command[1])
                delete_task(task_id)
            except ValueError:
                print("[ERROR] Invalid task ID")
        else:
            print("[ERROR] Missing task ID")

    elif action == "exit":
        print("Exiting Task Manager...\n")
        return False

    else:
        print(f"[ERROR] Unknown command: {action}")

    return True


# ---------------------------
# Main Runner (AUTO INPUT)
# ---------------------------

def main(commands):
    print("=== TASK MANAGER START ===\n")

    for cmd in commands:
        print(f"> Command: {cmd}")

        if not process_command(cmd):
            break

    print("=== TASK MANAGER END ===")


# ---------------------------
# Test Input (IMPORTANT)
# ---------------------------

if __name__ == "__main__":
    commands_to_execute = [
        ("add", "Buy groceries"),
        ("add", "Walk the dog"),
        ("add", "Finish report"),
        ("view",),
        ("complete", "2"),
        ("view",),
        ("delete", "1"),
        ("view",),
        ("complete", "10"),   # invalid ID case
        ("delete", "99"),     # invalid ID case
        ("exit",)
    ]

    main(commands_to_execute)