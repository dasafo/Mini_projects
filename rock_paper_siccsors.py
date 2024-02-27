import random

you_win = 0
cpu_win = 0

options = ["rock", "paper", "scissors"]

while True:
    choose_you = input("Introduce Rock, Paper o Scissors (or Q to exit): ").lower()

    if choose_you == 'q':
        print("Se you next time!")
        break
    if choose_you not in options:
        print("Please try again!")
        continue

    rand_num = random.randint(0,2)

    # rock = 0, paper = 1, scissor = 2
    choose_cpu = options[rand_num]

    print('The CPU has chosen: {0}.'.format(choose_cpu))

    if choose_you == 'rock' and choose_cpu == 'scissors':
        print('You win!!')
        you_win +=1
    elif choose_you == 'paper' and choose_cpu == 'rock':
        print('You win!!')
        you_win +=1
    elif choose_you == 'scissors' and choose_cpu == 'paper':
        print('You win!!')
        you_win +=1
    else:
        print('You loose!!')
        cpu_win +=1

    print('You won {0} times.'.format(you_win))
    print('CPU won {0} times.'.format(cpu_win))

    


