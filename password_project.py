pwd = input('Introduce the password: ')

def view():
    pass
def add():
    name = input('Name: ')
    pwd = input('Password: ')

    with open('password.txt', 'a') as f:
        f.write(name + " | " + pwd + "\n")

while True:
    action = input('Would you like to add a new password or view exsiting ones (view, add) or press q to exit: ').lower()

    if action == 'q':
        break

    elif action == 'view':
        view() 

    elif action == 'add':
        add()

    else:
        print('Invalid action!!')
        continue
