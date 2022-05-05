import requests
import turtle


table = turtle.Screen() #Game Table
table.setup(width = 1000) #Table Width - Screen Width

#Screen Height and Width Variables
height = table.window_height()
width = table.window_width()

#Ball Start Position
centre_border = turtle.Turtle(shape="circle")
centre_border.penup()
centre_border.shapesize(stretch_len = 2.5, stretch_wid = 2.5)

centre = turtle.Turtle(shape="circle")
centre.color("White")
centre.penup()
centre.shapesize(stretch_len = 2.4, stretch_wid = 2.4)

#Divider Line
line = turtle.Turtle(shape="square")
line.penup()
line.shapesize(stretch_len=0.1, stretch_wid = height)

#Pong Ball
ball = turtle.Turtle(shape="circle")
ball.penup()
ball.shapesize(stretch_len = 0.8, stretch_wid = 0.8)
ball.dx = -8
ball.dy = 8
ball.speed(50)

#Player 1
player1_pad = turtle.Turtle(shape="square", visible=False) #Pad
player1_pad.penup()
player1_pad.goto(((width/2) - width), 0)
player1_pad.shapesize(stretch_len = 1, stretch_wid=5)
player1_pad.showturtle()
player1_score = 0 #Score
player1_controller = 0 #X coordinate tracking

#Player 2
player2_pad = turtle.Turtle(shape="square", visible=False) #Pad
player2_pad.penup()
player2_pad.goto(width - (width/2) - 10, 0)
player2_pad.shapesize(stretch_len = 1, stretch_wid=5)
player2_pad.showturtle()
player2_pad.dy = -5
player2_score = 0 #Score
player2_controller = 0 #X coordinate tracking

#Score Display
scoreboard = turtle.Turtle(visible=False)
scoreboard.penup()
scoreboard.goto(0, height/2 - 40)
scoreboard.write("Player 1: " + str(player1_score) + "               " + "Player 2: "  + str(player2_score), font=("Sans Serif", 20, "bold"), align = "center")

#Set Pads to 0 Movement
requests.post('http://192.168.0.17:8000/update_player1_data/', data = {'id': 1, 'player1_x': '0', 'player1_y': '0', 'player1_z': '0'})
requests.post('http://192.168.0.17:8000/update_player2_data/', data = {'id': 1, 'player2_x': '0', 'player2_y': '0', 'player2_z': '0'})


while True:
    table.update()

    #Screen Height and Width Variables - In Case of Window Resize
    height = table.window_height()
    width = table.window_width()

 

    #Fetch Phone X coordinates

    response = requests.get('http://192.168.0.17:8000/player/')
    coordinates = response.json()

    player1_controller = (float(coordinates[0]['player1_x']) + player1_controller)
    player2_controller = (float(coordinates[0]['player2_x']) + player2_controller)

    controller = player1_pad.ycor()  
    controller = controller + player1_controller

    controller2 = player2_pad.ycor()  
    controller2 = controller2 + player2_controller


    player1_pad.sety(controller2)
    player2_pad.sety(controller2)
    


    #Ball Rules
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    #Ball hits right pad
    if(ball.xcor() > (width/2 - 30) and ball.xcor() < (width/2 - 20)):
        if(ball.ycor() < player2_pad.ycor() + 80 and ball.ycor() > player2_pad.ycor() - 80):
            ball.setx(width/2 - 30)
            ball.dx *= -1

    #Ball hits left pad
    if(ball.xcor() > ((width/2) * -1) and ball.xcor() < ((width/2 - 20) * -1)):
        if(ball.ycor() < player1_pad.ycor() + 80 and ball.ycor() > player1_pad.ycor() - 80):
            ball.setx((width/2 - 30) * -1)
            ball.dx *= -1

    #Ball hits top of table
    if ball.ycor() > ((height/2) - 20):
        ball.sety(((height/2) - 20))
        ball.dy *= -1


    #Ball hits bottom of table
    if ball.ycor() < (((height/2) - 25) * -1):
        ball.sety((((height/2) - 25) * -1))
        ball.dy *= -1




    #Ball hits the right of table
    if(ball.xcor() < ((width/2) * -1)):
        scoreboard.clear()
        player1_score = player1_score + 1
        scoreboard.write("Player 1: " + str(player1_score) + "               " + "Player 2: "  + str(player2_score), font=("Sans Serif", 20, "bold"), align = "center")
        ball.goto(0, 0)
        ball.dy *= -1

    #Ball hits left of table
    if(ball.xcor() > width/2):
        scoreboard.clear()
        player2_score = player2_score + 1
        scoreboard.write("Player 1: " + str(player1_score) + "               " + "Player 2: "  + str(player2_score), font=("Sans Serif", 20, "bold"), align = "center")
        ball.goto(0, 0)
        ball.dy *= -1



    #Pad Rules

    if(player2_pad.ycor() > (((width/3) - 95))):
        controller = player2_pad.ycor()  
        controller -= 10
        player2_pad.sety(controller)

    if(player2_pad.ycor() < (((width/3) - 85) * -1)):
        controller = player2_pad.ycor()  
        controller += 10
        player2_pad.sety(controller)

    if(player1_pad.ycor() > 230):
        player1_pad.sety(230)

    if(player1_pad.ycor() < -230):
        player1_pad.sety(-230)




