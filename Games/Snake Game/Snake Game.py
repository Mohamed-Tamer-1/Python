#import required modules
import turtle
import time
import random
import os
delay = 0.1
score = 0
def load_high_score():
    try:
        file_path = r"D:\Projecrs\VS Code\Python\Games\Snake Game\Snake Game.txt"
        with open(file_path, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Save high score to file
def save_high_score(high_score):
    file_path = r"D:\Projecrs\VS Code\Python\Games\Snake Game\Snake Game.txt"
    with open(file_path, "w") as file:
        file.write(str(high_score))

high_score = load_high_score()
#Creating a window screen
wn=turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
#the width and height can be put as user's choice
wn.setup(width=1280, height=720)
#disable window resize
wn.cv._rootwindow.resizable(True, True)
wn.tracer(0) # set delay for update drawings
#head of the snake
head = turtle.Turtle()
head.shape("square")
head.color("white")
head.penup() # stop drawing lines when moving
head.speed(0)
head.goto(0, 0)
head.direction = "Stop"
#food in the game
food = turtle.Turtle()
colors = random.choice(["red", "green", "blue"])
shapes = random.choice(["square", "circle"])
food.shape(shapes)
food.shapesize(stretch_wid=1 , stretch_len=1)
food.color(colors)
food.penup()
food.speed(0)
food.goto(0, 100)
pen = turtle.Turtle()
pen.shape("square")
pen.color("white")
pen.penup()
pen.speed(0)
pen.goto(0, 320)
pen.hideturtle()
pen.write("Score: 0", "High Score: 0", align="center", font=("Arial", 24, "bold"))
#assigning key directions
def goup():
    if head.direction != "down":
        head.direction = "up"
def godown():
    if head.direction != "up":
        head.direction = "down"
def goleft():
    if head.direction != "right":
        head.direction = "left"
def goright():
    if head.direction != "left":
        head.direction = "right"
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+ 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y-20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)
# key binding
wn.listen()
wn.onkeypress(goup, "w")
wn.onkeypress(goup, "Up")
wn.onkeypress(godown, "s")
wn.onkeypress(godown, "Down")
wn.onkeypress(goleft, "a")
wn.onkeypress(goleft, "Left")
wn.onkeypress(goright, "d")
wn.onkeypress(goright, "Right")
segments = []
#Main Gameplay
while True:
    wn.update()
    #checking for head collisions with borders
    if (
        head.xcor() > 630
        or head.xcor() < -630
        or head.ycor() > 350
        or head.ycor() < -350
):
        time.sleep(0)
        head.goto(0, 0)
        head.direction = "Stop"
        colors = random.choice(["red", "green", "blue"])
        shapes = random.choice(["square", "circle"])
        food.shape(shapes)
        
        food.color(colors)
        for segment in segments:
            segment.goto(1000, 1000)
        #segment.hideturt
        segments.clear()
        score = 0
        delay= 0.1
        pen.clear()
        pen.write(
            "Score: {}         High Score: {}".format(score, high_score),
            align="center",
            font=("Arial", 24, "bold"),
        )
    # Checking for head collisions with food
    if head.distance(food) < 20:
        x = random.randint(-270, 270)
        y = random.randint(-270, 270)
        food.goto(x, y)
        #Adding segment
        new_segment = turtle.Turtle()
        new_segment.shape("square")
        new_segment.color("white") # tail colour
        new_segment.speed(0)
        new_segment.penup()
        segments.append(new_segment)
        delay -=0.001 # increase game diffculty
        score += 10
        if score > high_score:
            high_score = score
            save_high_score(high_score)

        pen.clear()
        pen.write(
            "Score: {}         High Score: {}".format(score, high_score),
            align="center",
            font=("Arial", 24, "bold"),
        )
    # Shifting all snake body (segments[]) then move the (head) :
    for index in range(len(segments) - 1, 0, -1) :
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)
        161
    move()
    #  Checking for head collisions with body segments
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            colors = random.choice(["red", "green", "blue"]) 
            shapes = random.choice(["square", "circle"])
            food.shape(shapes)
            food.shapesize(stretch_wid=1 , stretch_len=1)
            food.color(colors)
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0 
            delay = 0.1
            pen.clear()
            pen.write(
                "Score: {} High Score: {} ".format(score, high_score),
                align="center",
                font=("Arial", 24, "bold"),
            )
    time.sleep(delay)
