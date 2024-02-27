import random

top_number = input("Enter the range number: ")

if top_number.isdigit():
    top_number = int(top_number)
    
    if top_number <=0:
        print('Please enter lager number next time!!')
        quit()

else:
    print('Incorrect type of variable!! Enter a number next time!!')
    quit()


guesses = 1
number = random.randint(0, top_number)

while True:

    guesses += 1
    guess = input('Try a guess: ')

    if guess.isdigit():
        guess = int(guess)
    else:
        print("Please enter a digit next time!!")
        continue
    
    if guess == number:
        print("You get it!!!")
        break
    elif guess < number:
        print("Not so low!!")
    elif guess > number:
        print('Not so high!!')

print(f'You made it in {guesses} guesses')
print('YOu made it in {0} guesses'.format(guesses))
