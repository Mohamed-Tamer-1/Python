import random
def random_num():
    min_num = int(input("Enter Minimum Num : "))
    max_num = int(input("Enter Maximum Num : "))
    r = random.randrange(min_num,max_num)
    return r
def guessing():
    r = random_num()
    attempts = 0
    while True :
        attempts += 1
        n = int(input("Enter Guessing Num : "))
        if attempts == 7 :
            print("You Have Reached Maximum Attempts")
            break
        if r > n :
            print("The Guessing Num is Too Low")
        elif r < n :
            print("The Guessing Num is Too High")
        else :
            print("Congratulations! You have guessed the correct number")
            print("Number of Attempts : ",attempts)
            break
guessing()
