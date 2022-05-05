import random
while True:
    lines = open("words.txt", "r")
    a=lines.read().splitlines() 
    selected_word = random.choice(a)
    check = ''.join(selected_word)
    word=list(selected_word)
    hidden = []

    print(word)
    for i in range(len(word)):
        hidden.append("_")

    attempts = 0
    max_attempts = 4
    # loop until either the player has won or lost
    GameOver = False
    while not GameOver:
        print("You have {} attempts remaining".format(max_attempts - attempts))
        print("The current word is: {}".format(' '.join(hidden)))
        if attempts == 0:
            print(""" 
                _
                /_\\
            ('>')
            >-- : --<
            ( : )
            _(_______)_""" )
        elif attempts == 1:
            print(""" 
                _
                /_\\
            ('>')
            >-- : --<
            ( : )""" )
        elif attempts == 2:
            print(""" 
                _
            /_\\
            ('>')
            >-- : --<""" )
        elif attempts == 3:
            print(""" 
                _
            /_\\
            ('>')""" )
            # loop until either the player has won or lost
        letterGuessed = input("Please guess a letter: ").lower()
        if letterGuessed in word:
            print("You guessed correctly!", letterGuessed, "is in the word.")
            for i in range(len(word)):
                character = word[i]
                if character == letterGuessed:
                    hidden[i] = word[i]
                    word[i] = "_"
        else:
            print("You guessed wrong!", letterGuessed, "is NOT in the word.")
            attempts += 1
        # if the player has won
        if check == ''.join(hidden):
            print("Congratulations, you won! Snowman is saved!")
            print("The hidden word is", selected_word)
            GameOver = True
        # if the player has won
        if attempts == max_attempts:
            #print(f"The current word is: {' '.join(hidden)}")
            print("The current word is: {}".format(' '.join(hidden)))
            print(""" _
            /_""" )
            print("You lost! Your snowman melted!")
            print("The hidden word is", selected_word)
            GameOver = True
            # if the player has won
    continueGame = input("Do you want to play again? Enter Y to continue, any other key to quit")
    if continueGame.upper() == 'Y':
        GameOver = False
    else:
        print("Thank You for playing. See you next time!")
    break
