import turtle
import time

win = turtle.Screen()
win.title("Ping Pong")
win.bgcolor("black")
win.setup(width=1280 , height=720)
win.tracer(0) # stop thw window from auto updating
# score
w = 0
w = turtle.Turtle()
w.speed(0)
w.color("white")
w.penup()
w.hideturtle()
w.goto(0 , 320)
w.write("Player 1       Player 2", align="center",font=("courier",24,"normal"))
score_1 = 0
score_2 = 0
score = turtle.Turtle()
score.speed(0)
score.color("white")
score.penup()
score.hideturtle()
score.goto(0 , 280)
score.write("0              0", align="center",font=("courier",24,"normal"))
# madrab 1
madrab1 = turtle.Turtle()
madrab1.speed(0)
madrab1.shape("square")
madrab1.shapesize(stretch_wid=5 , stretch_len=1)
madrab1.color("blue")
madrab1.penup()
madrab1.goto(-630 , 0)
# madrab 2
madrab2 = turtle.Turtle()
madrab2.speed(0)
madrab2.shape("square")
madrab2.shapesize(stretch_wid=5 , stretch_len=1)
madrab2.color("red")
madrab2.penup() # stop object from drawing lines
madrab2.goto(625 , 0)
# ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0 , 0)
ball.dx = 0.5 # الكوره تتحرك نص بكسل
ball.dy = 0.5
# functions
def madrab1_up():
    y = madrab1.ycor() # بحدد مكان المضرب
    y += 80 # بتحرك 20 بكسب لقوق
    madrab1.sety(y) # بحط النتيجه في ال واي
def madrab1_down():
    y = madrab1.ycor() # بحدد مكان المضرب
    y -= 80 # بتحرك 20 خطوه لقوق
    madrab1.sety(y) # بحط النتيجه في ال واي 
def madrab2_up():
    y = madrab2.ycor() # بحدد مكان المضرب
    y += 80 # بتحرك 20 خطوه لقوق
    madrab2.sety(y) # بحط النتيجه في ال واي
def madrab2_down():
    y = madrab2.ycor() # بحدد مكان المضرب
    y -= 80 # بتحرك 20 خطوه لقوق
    madrab2.sety(y) # بحط النتيجه في ال واي 
# keboard binding
win.listen() # ان في احتمال ان فيه زراير تداس 
win.onkey(madrab1_up , "w") # لما تدوس علي الزرا ينده الداله دي
win.onkey(madrab1_down , "s")
win.onkey(madrab2_up , "Up")
win.onkey(madrab2_down , "Down")
while True:
    win.update()
    time.sleep(0.001)
    # move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # border check
    if ball.ycor() > 350 : # لما الكوره توصل لاخر الاسكرين (اللي هي الحيطه)
        ball.sety(350) # ف لو هو اكبر من 700 يرجع الكوره ال700 تاني (اللي هي اخر الحيطه)
        ball.dy *= -1 # يعكس اجاه الكوره يعني الكوره تخبط و ترجع 
    if ball.ycor() < -350 :
        ball.sety(-350)
        ball.dy *= -1
    if ball.xcor() > 630 : # الكوره هنا تتحسب جون فيك لما تخبط في الحيطه
        ball.goto(0 , 0) # ف الكوره ترجع في النص
        ball.dx = 0.5
        ball.dx *= 1 # نعكس اتجاها و تروح لخصمك
        score_1 += 1
        score.clear()
        score.write("{}              {}".format(score_1, score_2), align="center",font=("courier",24,"normal"))
    if ball.xcor() < -640 :
        ball.goto(0 , 0)
        ball.dx = 0.5
        ball.dx *= -1
        score_2 += 1
        score.clear()
        score.write("{}              {}".format(score_1, score_2), align="center",font=("courier",24,"normal"))
    
    # paddle collision
    if ((ball.xcor() < -600 and ball.xcor() > -610) 
        and (ball.ycor() < madrab1.ycor() + 45 and ball.ycor() > madrab1.ycor() - 45)):
        ball.setx(-600)
        ball.dx *= -1
        ball.dx *= 1.1
        ball.dy *= 1.1

    if ((ball.xcor() > 600 and ball.xcor() < 610) 
        and (ball.ycor() < madrab2.ycor() + 45 and ball.ycor() > madrab2.ycor() - 45)):
        ball.setx(600)
        ball.dx *= -1
        ball.dx *= 1.1
        ball.dy *= 1.1

    # paddle max hight
    if madrab1.ycor() > 350 :
        madrab1.sety(305) 
    if madrab1.ycor() < -350 :
        madrab1.sety(-305)
    if madrab2.ycor() > 350 :
        madrab2.sety(305) 
    if madrab2.ycor() < -350 :
        madrab2.sety(-305)
    