#!/usr/bin/env python

import random
import curses
import sys
import time
import credits

print "\x1b[8;24;80t" #Resize screen

#Graphics before game starts
credits.snake()
credits.snake_fig()
credits.spacing(2)
credits.names()

#Class for giving a player recommadations
class suggest:

	def __init__(self,r):
		self.rec = r

	def __str__(self):
		return  "(" + str(self.rec) + ")"

print "I hope you enjoy playing"
rec = input("How many times have you played this game?")

suggest = suggest(rec)

print "since you have played", suggest, "times"

if rec < 20 and rec > 0:
   print "we recommend you try easy difficulty"
elif rec == 0:
   print "And this is your very first game you should try turtle mode : )"
elif rec >= 20 and rec < 40:
   print "we suggest you try medium difficulty"
elif rec >= 40 and rec < 100:
   print "we recommend you try hard difficulty"
elif rec >= 100:
   print "And you are clearly a tryhard you should try a different mode : p"

#Get users diffuculty and check that the diffuculty exists in the dictionary
def difficulty(a,dictionary):
    dif = a.lower()
    if dif in dictionary:
        if dif == "easy":
            x = 100
        elif dif == "medium":
            x = 75
        elif dif == "hard":
            x = 50
        elif dif == "flash":
            x = 25
            print "Speed"
        elif dif == "turtle":
            x = 200
            print "Slow and steady wins the race"
        elif dif == "fun":
            x = 85
            print "Sides are your enemies, you also have 5 lifes to run over yourself"
    else:
        x = False
    return x

#input for player name and difficulty
name = raw_input("Enter you name:\n")
dif = raw_input("Enter Difficulty:\nEasy, Medium, Hard\n")

mode = 'normal' #default mode is set to normal

difficulties = ['easy','medium','hard','flash','turtle','fun'] #Difficulties put in list, for checking user input

#Changing the speed of snake based on the difficulty inputted by user
x = difficulty(dif,difficulties)

#Repeat the question if user made a typo
if x == False:
    while difficulty(dif,difficulties) == False:
        dif = raw_input("Enter Difficulty:\nEasy, Medium, Hard\n")
        x = difficulty(dif, difficulties)

#Fun mode setting
if x == 85:
    mode = "Fun"

print "Press any key to quit to the game"
time.sleep(2)

#Counts the users score
score = 0

screen = curses.initscr() #Remove the text field of terminal and make it to a blank screen
curses.curs_set(0) #Takes away the grey highlight block from the snake

#Screen size for game
height = 24
width = 80

curses.start_color(); #Add colour
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #The colours to add
window = curses.newwin(height, width, 0, 0) #Window measurements
window.keypad(1) #The arrow keys as input for the movement of the snake
window.timeout(x) #Speed of snake
window.border()   #Border around window
window.bkgd(' ', curses.color_pair(1)) #Add colour to game

#Snake measurements on screen - place snake on middle of screen
snake = [ [height/2, width/4], [height/2, width/4-1], [height/2, width/4-2] ]

food_spawner = [random.randint(1, height-2), random.randint(1, width-2)] #Food spawner
food = food_spawner
window.addch(food[0], food[1], "@") #Add food to screen

#Default key when user starts the game, snake will move to the right
key = curses.KEY_RIGHT

health = 5 #For fun game mode

game_status = True #Use as a tracker for when game ends, when false player is returned to terminal

while game_status == True:

    next_key = window.getch() #Get key pressed
    
    current_key = -1
    
#Settings so the snake cannot run over itself if user pressed the opposite key, hence snake would run back over itself
    if next_key == current_key:
        key = key
    elif key == curses.KEY_DOWN and next_key == curses.KEY_UP:
        next_key = key
    elif key == curses.KEY_UP and next_key == curses.KEY_DOWN:
        next_key = key
    elif key == curses.KEY_LEFT and next_key == curses.KEY_RIGHT:
        next_key = key
    elif key == curses.KEY_RIGHT and next_key == curses.KEY_LEFT:
        next_key = key
    else:
        key = next_key
        
        
        
    if mode == "normal":
        if snake[0] in snake[1:]: #If the snake runs over itself; gameover
            game_status = False

#The borders: Make snake teleport to other side if it hits the border    
        if snake[0][0] in [0, height]:
            snake[0][0] = height-2
            window.border() # Add the border back as snake passes through the edge of screen

        if snake[0][1] in [0, width]:
            snake[0][1] = width - 2
            window.border()

        if snake[0][0] in [height-1, 0]:
            snake[0][0] = 1
            window.border()

        if snake[0][1] in [width-1, 0]:
            snake[0][1] = 1
            window.border()

    elif mode == "Fun":
        if snake[0][0] in [0,height] or snake[0][1] in [0,width] or snake[0][0] in [height-1, 0] or snake[0][1] in [width-1,0]: #If snake in margin; gameover
            game_status = False

        elif snake[0] in snake[1:]: #If the snake runs over itself remove health
            health -= 1
            if health == 0: #If health is 0 end the game
                game_status = False

#Stop Game when Player Loses
    if game_status != True:
        curses.endwin()
        break

    snake_head = [snake[0][0], snake[0][1]]

#The controls of the snake: UP, DOWN, LEFT, RIGHT keys
    if key == curses.KEY_DOWN:
        snake_head[0] += 1
    if key == curses.KEY_UP:
        snake_head[0] -= 1
    if key == curses.KEY_LEFT:
        snake_head[1] -= 1
    if key == curses.KEY_RIGHT:
        snake_head[1] += 1

#Add to the head of snake to the body
    snake.insert(0, snake_head)

#When the snake approaches the food, i.e. eats it
    if snake[0] == food:
        score += 1
        food = "eaten"

#When food is eaten, make it appear on a random spot on the screen
        while food is "eaten":
            food_spawner = [random.randint(1, height-2), random.randint(1, width-2)] #Generate food at random spot on screen within window limits
            if food not in snake:
                food = food_spawner
            else:
                food = "eaten"
                
        window.addch(food[0], food[1], '@') #Add food to screen

#Make snake tail move with body
    else:
        tail = snake.pop()
        window.addch(tail[0], tail[1], ' ')

    window.addch(snake[0][0], snake[0][1], 'O') #Add the snake to screen

#Graphics printed to screen when game ends
credits.spacing(2)
credits.greetings()

#Print the users score when he loses or stops the game
print
print '\x1b[6;30;42m' + name + " " + " "  "your score was:" + " " + str(score) + '\x1b[0m' #Print score in green

#Save And/Or Display the highest score
highscore = dif + ".txt"
with open(highscore, 'r') as f:
    text = f.readline()
    f.close()

print
token = text.strip().split(":")
if score > int(token[1]):
    with open(highscore, 'w+') as wf:
        text = name + ':' + " " + str(score)
        wf.write(text)
        print
        print "Highscore:\n", text.strip()
else:
    print
    print "Highscore:\n", text.strip()
