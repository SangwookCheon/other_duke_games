"""
Created on Sep 22, 2022

@author: Sangwook Cheon

This module represents a carnival Racer game, in which a number of turtles randomly race across the screen.
"""

# HOURS SPENT: 8 Hours

"""
HOW TO PLAY THE GAME:

This is a stop-motion game that I call "They're After You." As a player (a white square),
you must avoid assassins and agents who try to covertly kill you while trying to get across to the other
side to safety, under darkness of the night. Only when you take a step (with right, left, up, down keys), so
do assassins and agents. Here are what assassins and agents do:

Assassins:
- They start by being behind you. You have a head start. 
- Each time you move up, down, or right, they move in the same direction with some randomness.
- So when you go right 20 pixels, they can move less or more than you did, potentially getting closer
to you (bad!). They also move in slight angles - ex) they can move slightly down while going right. 
-  BUT, if you go LEFT, assassins always go left MORE than you did with no angles, 
giving you some much needed space. 

Agents: 
- There are no agents at the start of the game. 
- Each time you move left, one agent is created on the other side of the screen.
- Their movement is reversed - ex) if you go up, they go down.
- Just like assassins, if you get too close to them, they will kill you. 

Boundary - you cannot move down or up the red boundaries, although assassins and agents can.  

When you successfully get to the other side, you score 1 point. The number of assassins at the start
increases by 1, to increase difficulty. How much can you score with 5 lives?

"""

import random
import turtle
import os

gameName = "They're After You"

# The game is made to be a wide rectangle, as emphasis is on player moving across.
screenWidth = 800
screenHeight = 600

# A list of assassins who follow you from behind (in blue circles)
list_assasins = []

# A list of 'agents,' who move in reverse of player's movement (in orange circles).
list_agents = []

# Determines the amount of pixels the player moves in each key press
# I found 20 to be a good step size
player_speed = 20

# This is for setting the red boundaries --> 210 makes game reasonably more difficult.
boundary_offset = 210

def move_right():
    player.setx(player.xcor() + player_speed)
    move_assasins('right')

def move_left():
    player.setx(player.xcor() - player_speed)
    move_assasins('left')

def move_up():
    if player.ycor() < boundary_offset - 20:
        player.sety(player.ycor() + player_speed)
        move_assasins('up')

def move_down():
    if player.ycor() > -boundary_offset + 20:
        player.sety(player.ycor() - player_speed)
        move_assasins('down')

def reset_player():
    # Resets the player's position to starting position
    player.goto(- screenWidth // 2 + 120, 0)

def create_agent():
    """
    Create an agent and position it based on player's y-coordinate, with some randomness
    """
    agent = turtle.Turtle()
    agent.penup()
    agent.color('orange')
    agent.shape('circle')
    agent.shapesize(0.5, 0.5)
    agent.goto(screenWidth // 2 - 20, random.randrange(player.ycor() - 50, player.ycor() + 50))
    list_agents.append(agent)



def move_assasins(direction):
    '''
    Moves assassins based on keyboard input by player. Also moves agents!
    '''

    if direction == 'right':
        for assasin in list_assasins:

            """
            Here, choosing random value between 10 and 40 for assassins' movement adds 
            excitement and unexpectedness to the game. It also mimic's their dashing movement. 
            The player cannot expect how closer the assassins/agents will move based on the next step.
            """

            assasin.setx(assasin.xcor() + random.randint(10, 40))
            assasin.sety(assasin.ycor() + random.randint(-5, 5))
        for agent in list_agents:
            agent.setx(agent.xcor() - random.randint(10, 40))

    elif direction == 'left':
        """
        # if player moves left, all assasins must track backwards equally, but here's the catch:
        # they bring in agents from the right side of the screen.
        """
        for assasin in list_assasins:
            assasin.setx(assasin.xcor() - 30)
        for agent in list_agents:
            agent.setx(agent.xcor() + random.randint(10, 50))
        create_agent()

    elif direction == 'up':
        for assasin in list_assasins:
            # assasin.setx(assasin.xcor() + random.randint(-5, 5))
            assasin.sety(assasin.ycor() + random.randint(10, 40))
        for agent in list_agents:
            agent.sety(agent.ycor() - random.randint(10, 40))

    elif direction == 'down':
        for assasin in list_assasins:
            # assasin.setx(assasin.xcor() + random.randint(-5, 5))
            assasin.sety(assasin.ycor() - random.randint(10, 40))
        for agent in list_agents:
            agent.sety(agent.ycor() + random.randint(10, 40))

def check_collide():
    '''
    Check if the player collided with any of the assassins or agents - if so, the assassin sliced you like a ninja
    '''
    for assasin in list_assasins:

        """
        Original:
        distance = ((assasin.ycor() - player.ycor()) ** 2 + (assasin.xcor() - player.xcor()) ** 2) ** 0.5
        """

        x_dif = (assasin.xcor() - screenWidth // 2) - (player.xcor() - screenWidth // 2)
        y_dif = (assasin.ycor() - screenHeight // 2) - (player.ycor() - screenHeight // 2)
        distance = (x_dif ** 2 + y_dif ** 2) ** 0.5

        if distance <= 20:
            if theLives.lives > 0:
                update_lives()

                # Optional: Add slicing sound when dead.
                # os.system("afplay " + 'slice.mp3')

                # Prevents turtle 'residues' from staying on the screen
                for assasin in list_assasins:
                    assasin.hideturtle()

                for agent in list_agents:
                    agent.hideturtle()

                list_assasins.clear()
                list_agents.clear()

                theScreen.update()

                setup(int(theScore.score) + 3)

            else:
                end_game()

    for agent in list_agents:

        '''
        Original:
        distance = ((assasin.ycor() - player.ycor()) ** 2 + (assasin.xcor() - player.xcor()) ** 2) ** 0.5
        '''
        x_dif = (agent.xcor() - screenWidth // 2) - (player.xcor() - screenWidth // 2)
        y_dif = (agent.ycor() - screenHeight // 2) - (player.ycor() - screenHeight // 2)
        distance = (x_dif ** 2 + y_dif ** 2) ** 0.5
        if distance <= 20:
            if theLives.lives > 0:
                update_lives()

                # Prevents turtle 'residues' from staying on the screen
                for assasin in list_assasins:
                    assasin.hideturtle()

                for agent in list_agents:
                    agent.hideturtle()

                list_assasins.clear()
                list_agents.clear()

                theScreen.update()

                setup(int(theScore.score) + 3)

            else:
                end_game()


def check_success():
    '''
    Check if the player successfully reached the other side of the screen.
    '''
    # First do one time.
    if player.xcor() > screenWidth // 2 - 50:
        # increase number of initial assasins by 1 to increase difficulty.
        update_score()

        for assasin in list_assasins:
            assasin.hideturtle()

        for agent in list_agents:
            agent.hideturtle()

        list_assasins.clear()
        list_agents.clear()
        theScreen.update()

        setup(int(theScore.score) + 3)

def update_score():
    # updates the score of the player
    theScore.score += 1
    # Adding this line below solved the bug: getting rapid frames, score suddenly dropping
    reset_player()

    draw_score(theScore)

def update_lives():
    # Update the lives left of the player
    theLives.lives -= 1
    reset_player()
    draw_lives(theLives)

def draw_score(score):
    # Draw the score on the screen
    score.penup()
    score.hideturtle()
    score.clear()
    score.color('white')
    score.goto(- screenWidth // 2 + 100, screenHeight // 2 - 50)
    score.write("Score: " + str(score.score), align='center', font=('Courier', 20, 'bold'))

def draw_lives(lives):
    # Draw lives left on the screen
    lives.penup()
    lives.hideturtle()
    lives.clear()
    lives.color('white')
    lives.goto(screenWidth // 2 - 100, screenHeight // 2 - 50)
    lives.write("Lives: " + str(lives.lives), align='center', font=('Courier', 20, 'bold'))

def end_game():
    # displays ending message with final score, and stops updating the game.
    text = turtle.Turtle()
    text.hideturtle()
    text.clear()
    text.penup()
    text.color('white')
    text.goto(0, 0)
    text.write("Final Score: " + str(theScore.score), align='center', font=('Courier', 20, 'bold'))

    restart = turtle.Turtle()
    restart.hideturtle()
    restart.clear()
    restart.penup()
    restart.color('red')
    restart.goto(0, -30)
    restart.write("Re-run Program to Play Again", align='center', font=('Courier', 20, 'bold'))

    theScreen.update()

    # theScreen.listen()
    # theScreen.onkeypress(reset_game, 'Right')

def reset_game():
    # Resets the game.
    setup(3)

# Set up the game scene
def game_step():

    """
    Main function that 'runs' the game, based on player's keyboard input. Calls various functions.
    """

    # Now that assasins are drawn on screen, listen for key presses - this is the main game
    if theLives.lives > 0:
        theScreen.listen()
        theScreen.onkeypress(move_right, 'Right')
        theScreen.onkeypress(move_left, 'Left')
        theScreen.onkeypress(move_down, 'Down')
        theScreen.onkeypress(move_up, 'Up')

        check_success()
        check_collide()

        # start game's mainloop
        theScreen.update()

        # The first parameter re-runs the game. So it's a loop.
        theScreen.ontimer(game_step, 10)
    else:
        end_game()

# Create all the racers, and then run game_step.
def setup(numAssasins):
    """
    Sets up the key components of the game: assasins, draw scores and lives, position the player, and
    draw the boundaries. Then calls game_step() to begin the actual game.
    """
    # Setting up Assasins
    list_assasins.clear()
    list_agents.clear()

    # Position the player
    reset_player()

    # Draw Score and Lives
    draw_score(theScore)
    draw_lives(theLives)

    # Draw Boundaries
    lines = turtle.Turtle()
    lines.color('red')
    lines.hideturtle()
    lines.pensize(3)
    lines.penup()
    lines.goto(-screenWidth // 2, -boundary_offset)
    lines.setheading(0)
    lines.pendown()
    lines.forward(screenWidth)

    lines.penup()
    lines.goto(-screenWidth // 2, boundary_offset)
    lines.setheading(0)
    lines.pendown()
    lines.forward(screenWidth)


    for i in range(numAssasins):
        assasin = turtle.Turtle()
        assasin.penup()
        assasin.color('red')
        assasin.shape('circle')

        # 0.5 and 0.5 were chosen for the size to give the player more room to move around and allow
        # freer movements
        assasin.shapesize(0.5, 0.5)
        list_assasins.append(assasin)

    # Initialize the set number of assasins on screen - beginning of the game.
    for i, assasin in enumerate(list_assasins):
        xpos = - screenWidth // 2 + 15
        ypos = ((-1) ** (i)) * (30*i)
        assasin.goto(xpos, ypos)

    theScreen.update()
    theScreen.ontimer(game_step, 10)



'''
Below, I start the game and set up key components: the Screen, the Player, and Assasins
'''

# Score
theScore = turtle.Turtle()
theScore.hideturtle()
theScore.penup()
theScore.score = 0

# Lives
theLives = turtle.Turtle()
theLives.hideturtle()
theLives.penup()

# The game turned out to be quite difficult, so I gave a generous 5 lives.
theLives.lives = 5

# Create the Screen
theScreen = turtle.Screen()
theScreen.title(gameName)
theScreen.setup(screenWidth, screenHeight)
theScreen.bgpic('background.gif')
theScreen.tracer(False)  # want turtle to move as fast as possible.

# Create the Player (globally defined)
player = turtle.Turtle()
player.penup()
player.shape('square')
# The player should be slightly bigger than the assassins (partly because a normal human is more visible)
player.shapesize(0.8, 0.8)
player.color('white')
player.goto(- screenWidth // 2 + 80, 0)


# Set Up the game, and ready to play!
setup(3)

# Play the game forever
theScreen.mainloop()
