
tasks = []
def add_task():
    
    task = input("Enter the description of your new taks please: ")
    tasks.append({"description" : task, "completed" : False})
    print("Task added successfully!")
    
    
    
def view_tasks():
    
    print("These are your INCOMPLETED tasks:")
    for i, task in enumerate(tasks):
        if not task["completed"]:
            print(f"{i+1}. {task['description']}")
    
    print("These are your COMPLETED tasks:")
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
    
    if 0 < completed_task <= len(tasks):
        tasks.pop(delete_task - 1)
        print("Taks deleted.")
    else:
        print("Invalid task number.")



            
        