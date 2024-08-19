# imports
import random
import curses
import time
def main():
    # Put all your code in here
    # game speed
    delay = 100
    # score
    score = 0
    # Initialize the curses library to create our screen
    screen = curses.initscr()
    # Set the color pairs for the screen
    curses.start_color()
    # hide the mouse cursor
    curses.curs_set(0)
    # getmax screen helght and width
    screen_height, screen_width = screen.getmaxyx()
    #create a new window
    window = curses.newwin(screen_height, screen_width, 0, 0)
    # allow window to receive input from the keyboard
    window.keypad(1)
    # set the delay for updating the screen
    window.timeout(100)
    # set the x.y coordinates of the initial position of snake's head
    snk_x = screen_width // 4
    snk_y = screen_height // 2
    # define the initial positon of the snake body
    snake = [
        [snk_y, snk_x] , # Head position
        [snk_y, snk_x - 1] , # stomack position
        [snk_y, snk_x - 2] # tail position
    ]
    # Create a color pair 1 with green text on black background
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    # Load high score from file
    try:
        file_path = r"D:\Projecrs\VS Code\Python\Games\Snake Game\Snake.txt"
        with open(file_path, "r") as file:
            high_score = int(file.read())
    except FileNotFoundError:
        high_score = 0
    # create the food in the middle of window
    food = [screen_height // 2, screen_width // 2]
    # set initial blocks
    blocks = []
    # add the food by using PI character from curses nodule.
    food_char = random.choice([curses.ACS_DIAMOND, curses.ACS_DEGREE, curses.ACS_GEQUAL])
    food_color = random.choice([curses.color_pair(1), curses.color_pair(2), curses.color_pair(3), curses.color_pair(4)])
    window.addch(food[0], food[1],curses.ACS_DIAMOND,curses.color_pair(2))
    # set Inttial movement direction to right
    key = curses.KEY_RIGHT
    # create game Loops that loops forever until slaver loses or quits the game
    while True:
        # get the key pressed by the user
        next_key = window.getch()
        # check if the key pressed is a valid key
        key = key if next_key == -1 else next_key
        #check if snake callided with the walls or itself
        if (snake[0][0] in [0, screen_height-1] 
            or snake[0][1] in [0, screen_width-1] 
            or snake[0] in snake[1:]
            # or any(block == snake[0] for block in blocks)
            ):            
            time.sleep(0.5)
            if score > high_score:
                high_score = score
                # Save high score to file
                file_path = r"D:\Projecrs\VS Code\Python\Games\Snake Game\Snake.txt"
                with open(file_path, "w") as file:
                    file.write(str(high_score))
            restart()
            if key == ord('r') :
                restart()
        # Check for user pressing the 'k' key to quit
        if key == ord('k'):
            curses.endwin()
            print("GAME OVER")
            print("score : ", score)
            print("high score : ", high_score)
            quit() # exit the program
        # set the new position of the snake head based on the direction
        new_head = [snake[0][0], snake[0][1]]
        # check if the key pressed is a valid key
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        # insert the new head to the first poisition of snake List
        snake.insert(0 , new_head)
        # check if snake ate the food food
        if snake[0] == food:
            food = None # remove food if snake ate it
            score += 10
            # increase the game speed
            delay -= 5 # reduce delay but don't go below 50 ms
            window.timeout(delay)    
        # while foode is removed, generate new food in a rendom place on screen
            while food is None:
                new_food = [
                    random.randint(1 , screen_height-1) ,
                    random.randint(1 , screen_width-1) 
                ]
                # set the food to new food if new food is not in snake body and add it to screen
                food = new_food if new_food not in snake else None
            # set food in random places
            window.addch(food[0] , food[1] ,curses.ACS_DIAMOND,curses.color_pair(2))
        # # set new blocks in random place
        #     new_block = [
        #             random.randint(1, screen_height - 2),
        #             random.randint(1, screen_width - 2)
        #     ]
        #     if new_block not in snake and new_block != food:
        #             blocks.append(new_block)
        #     window.addch(new_block[0] , new_block[1] , curses.ACS_BLOCK)
        # otherwise remove the last segment of the snake body
        else:
            tail = snake.pop()
            window.addch(tail[0] , tail[1] , ' ')
        # update the position of the snake on the screen
        window.addch(snake[0][0] , snake[0][1] , curses.ACS_BLOCK , curses.color_pair(6))
        # Update the score display
        window.addstr(0, screen_width-50, f"Score: {score} High Score: {high_score}")
        window.refresh()

def restart():
    main()
    exit()
main()