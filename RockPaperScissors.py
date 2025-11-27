import random
# Variables for game
choices = ['rock', 'paper', 'scissors']
player = computer = ties = rounds = 0

def winner(user, comp):
    if user == comp:
        return 'tie'
    elif (user == 'rock' and comp == 'scissors') or \
         (user == 'paper' and comp == 'rock') or \
         (user == 'scissors' and comp == 'paper'):
        return 'player'
    return 'computer'


while True:
    print(f'\nStone, Paper, Scissors')
    print('1. Play Round')
    print('2. View Score')
    print('3. Reset Score')
    print('4. Quit')

# Get user menu choice
    choice = input('Choose an option (1-4): ')  

    if choice == '1':
        user = input('Enter rock / paper / scissors: ').lower()

        if user not in choices:
            print('Invalid choice. Please try again.')
            continue
        
        comp = random.choice(choices)
        rounds += 1

        result = winner(user, comp)

        print(f"You: {user} | Computer: {comp}")

        # update and display result
        if result == 'player':
            player += 1
            print('You win this round!')
        elif result == 'computer':
            computer += 1
            print('Computer wins this round!')
        else:
            ties += 1
            print("It's a tie!")

    elif choice == '2':
        print(f"\nScore -> You: {player} | Computer: {computer} | Ties: {ties}")

    elif choice == '3':
        player = computer = ties = rounds = 0
        print('Scores have been reset.')

    elif choice == '4':
        print('Thanks for playing!')
        break

    else:
        print('Invalid option. Please choose between 1-4.')
