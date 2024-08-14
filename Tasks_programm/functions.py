import json
from datetime import datetime

tasks = []


def add_task():
    
    task = input("Enter the description of your new taks please: ")
    due_date = input("Enter the due date (YYYY-MM-DD) or leave blank: ")
    due_date = datetime.strptime(due_date, "%Y-%m-%d").date() if due_date else None
    
    priority = input("Enter priority (low, medium, high): ").lower()
    
    tags = input("Enter tags separated by commas: ").split(",")
    
    tasks.append({"description" : task, 
                  "completed" : False, 
                  "due_date" : due_date, 
                  "priority": priority, 
                  "tags": [tag.strip() for tag in tags]})
    
    print("Task added successfully!")
    
    
    
    
def view_tasks():
    
    print("INCOMPLETED tasks:")
    for i, task in enumerate(tasks):
        if not task["completed"]:
            tags = ", ".join(task.get('tags', []))
            due = f" (Due: {task['due_date']})" if task["due_date"] else ""
            print(f"{i+1}. {task['description']} (Priority: {task['priority']}) (Tags: {tags}) {due}")
    
    print("COMPLETED tasks:")
    for i, task in enumerate(tasks):
        if task["completed"]:
            print(f"{i+1}. {task['description']}")
    print()



def mark_task_completed():
    view_tasks()
    
    completed_task = int(input("Enter the number of the task you want to mark as completed: "))
    
    if 0 < completed_task <= len(tasks):
        tasks[completed_task - 1]["completed"] = True
        print("Task marked as completed.")
    else:
        print("Invalid number.")
     
        

def delete_task():
    view_tasks()
    
    delete_task = int(input("Enter the number of the task you want to delete: "))
    
    if 0 < delete_task <= len(tasks):
        tasks.pop(delete_task - 1)
        print("Taks deleted.")
    else:
        print("Invalid task number.")



def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)
        
    print("Tasks saved successfully.")



def load_tasks():
    
    try:
        with open("tasks.json", "r") as file:
            global tasks
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
        

def sort_tasks_by_due_date():
    tasks.sort(key=lambda task: (task['due_date'] is None, task['due_date']))
    print("Tasks sorted by due date.")
    
    
def sort_tasks_by_priority():
    priority_order = {"low": 1, "medium": 2, "high": 3}
    tasks.sort(key=lambda task: priority_order.get(task['priority'], 0))
    print("Tasks sorted by priority.")