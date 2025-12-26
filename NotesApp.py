import os

FILE_NAME = "tasks.txt"

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return file.read().splitlines()

def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write(task + "\n")

def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.\n")
        return
    print("\nYour Tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
    print()

def add_task(tasks):
    task = input("Enter new task: ")
    tasks.append("[ ] " + task)
    save_tasks(tasks)
    print("Task added!\n")

def complete_task(tasks):
    show_tasks(tasks)
    try:
        num = int(input("Enter task number to mark complete: "))
        tasks[num - 1] = tasks[num - 1].replace("[ ]", "[✔]")
        save_tasks(tasks)
        print("Task marked as completed!\n")
    except:
        print("Invalid input.\n")

def main():
    tasks = load_tasks()
    while True:
        print("---- TO-DO APP ----")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Complete Task")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()
