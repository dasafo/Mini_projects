print("Welcome to my quiz game!")

playing = input("Do you want to play with me? ")

if playing.lower() != "yes":
    quit()

print("Awsome! Let's go to play :)")
score = 0

answer = input("What does ASAP mean? ")
if answer.lower() == "as soon as posible":
    print('Correct!')
    score += 1
else:
    print("Nop!")

answer = input("What does FYI mean? ")
if answer.lower() == "for your information":
    print('Correct!')
    score += 1
else:
    print("Nop!")

answer = input("What does LOL mean? ")
if answer.lower() == "laugh out loud":
    print('Nop!')
    score += 1
else:
    print("Incorrect!")

answer = input("What does TTYL mean? ")
if answer.lower() == "talk to you later":
    print('Nop!')
    score += 1
else:
    print("Nop!")

print("You got " + str(score) + " questions correct!")
print("You have " + str((score / 4) * 100) + "%.")
