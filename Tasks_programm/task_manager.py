from functions import *

def show_menu():
    print("==================")
    print("== Task Manager ==")
    print("==================")
    print("1. Add a new task")
    print("2. View tasks")
    print("3. Mark task as completed")
    print("4. Delete task")
    print("5. Exit")
    
def main():
    load_tasks()
    while True:
        show_menu()
        option =  input("Choose an option: ")
        
        if option == '1':
            add_task()
        elif option == '2':
            view_tasks()
        elif option == '3':
            mark_task_completed()
        elif option == '4':
            delete_task()
        elif option == '5':
            save_tasks()
            print("Bye bye...")
            break
        else:
            print("Invalid option, please try again.")
            
if __name__ == "__main__":
    main()
