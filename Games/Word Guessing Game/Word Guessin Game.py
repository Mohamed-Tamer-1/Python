import random

def main():
    words = ['rainbow', 'computer', 'science', 'programming',
            'python', 'mathematics', 'player', 'condition',
            'reverse', 'water', 'board', 'geeks']
    word = random.choice(words)
    print(word)
    print("Guess The Word : ")
    guesses = ''
    attempts = 0
    while attempts < 13 :
        for char in word :
            if char in guesses :
                print(char, end=' ')
            else :
                print("_", end=' ')

        if attempts == 12 :
            print("You Lose")
            
        
        if set(word) == set(guesses) :
            print("\nYou Win")
            break

        print()
        guess = input("Guess The Char : \n")
        guesses += guess
        
        if guess not in word :
            print("Incorrect Guess")
            attempts += 1
main()
