"""
Created on Sep 13, 2022

@author: YOUR NAME HERE!!
@author: Robert Duvall

This module represents the game of Pong, the first popular arcode game!

Modify the game_step() function to make the game playable
Modify the reset_ball() function to make the ball start in a random direction
"""
import random
import turtle

# choose a name for your game to appear in the title bar of the game window
gameName = 'Pong'
# choose the size of your game window
screenWidth = 800
screenHeight = 600
# choose how fast paddles move
paddleSpeed = 20
# choose where paddles are positioned
paddleOffset = 50
# choose where scores are positioned
scoreXOffset = 50
scoreYOffset = 80

# Move the players' paddles up or down based on the speed
def paddle1_up():
    thePaddle1.sety(thePaddle1.ycor() + paddleSpeed)

def paddle1_down():
    thePaddle1.sety(thePaddle1.ycor() - paddleSpeed)

def paddle2_up():
    thePaddle2.sety(thePaddle2.ycor() + paddleSpeed)

def paddle2_down():
    thePaddle2.sety(thePaddle2.ycor() - paddleSpeed)

def reset_on_click(x, y):
    reset_ball(theBall)


def draw_scene(screen):
    """
    Draw the game's setting.

    Whatever turtles you create here or drawing that you do here will serve as the game's background
    to set the game's theme, but will not be part of the game's action.
    """
    screen.bgcolor('black')


def draw_paddle(paddle, xPos):
    """
    Draw the interactive piece of the game that the player uses to block the moving ball.
    """
    paddle.speed(0)
    paddle.penup()
    paddle.shape('square')
    paddle.shapesize(5, 1)
    paddle.color('white')
    paddle.goto(xPos, 0)


def draw_score(text, xPos):
    """
    Draw a player's score offset by the given amount from the center of the screen.
    """
    text.speed(0)
    text.penup()
    text.hideturtle()
    text.clear()
    text.color('white')
    text.goto(xPos, screenHeight // 2 - scoreYOffset)
    text.write(str(text.score), align='center', font=('Courier', 64, 'bold'))


def draw_ball(ball):
    """
    Draw the ball that will be moving around the game arena.
    """
    ball.speed(0)
    ball.penup()
    ball.shape('circle')
    ball.color('cyan')


def reset_ball(ball):
    """
    Reset the ball back at the center of the scene after a miss, restart its movement by setting dx and dy variables.
    """
    ball.goto(0, 0)
    # random_dx = random.randrange(2, 5)
    ball.dx = 3
    ball.dy = -3


def game_step():
    """
    Handle game "rules" for every step (i.e., frame or "moment"):
     - movement: move the ball each step?
     - collisions: check if the ball collided with the sides or paddles and then bounce or reset it
    Note, to make the ball appear to bounce, all that is needed is to reverse the appropriate "d" value:
     - if bouncing off the top or bottom, negate theBall.dy
     - if bouncing off either paddle, negate theBall.dx
    """
    # move ball based on its speed
    theBall.goto(theBall.xcor() + theBall.dx, theBall.ycor() + theBall.dy)

    # check if ball hits top or bottom side, bounce it by reversing theBall's dy variable

    if theBall.ycor() == int(screenHeight / 2) or theBall.ycor() == -int(screenHeight / 2):
        theBall.dy *= -1

    # check if the ball got past player 1's paddle (hit the right edge), then reset ball and update player 2's score

    if theBall.xcor() == screenWidth / 2:
        theBall.goto(0, 0)
        theScore2Text.score += 1
        draw_score(theScore2Text, -scoreXOffset)

    # check if the ball got past player 2's paddle (hit the left edge), then reset ball and update player 1's score

    if theBall.xcor() == screenWidth / -2:
        theBall.goto(0, 0)
        theScore1Text.score += 1
        draw_score(theScore1Text, scoreXOffset)

    # check if the ball hits thePaddle1, bounce it by reversing theBall's dx variable

    # Dimension is 120 for the paddle and 20 for the ball.

    # check if the ball hits thePaddle2, bounce it by reversing theBall's dx variable

    # DO NOT CHANGE - required to see the changes made and keep the game running
    theScreen.update()
    theScreen.ontimer(game_step, 10)


def setup():
    """
    Sets up the initial game scene
    """
    # make the game interactive
    theScreen.tracer(False)
    # listen for key presses
    theScreen.listen()
    theScreen.onkeypress(paddle1_up, 'Up')
    theScreen.onkeypress(paddle1_down, 'Down')
    theScreen.onkeypress(paddle2_up, 'w')
    theScreen.onkeypress(paddle2_down, 's')
    # for debugging purposes, allow mouse click to reset the ball
    theScreen.onclick(reset_on_click)
    # draw the game based on student's code
    draw_scene(theScreen)
    draw_score(theScore1Text, scoreXOffset)
    draw_score(theScore2Text, -scoreXOffset)
    draw_paddle(thePaddle1, screenWidth // 2 - paddleOffset)
    draw_paddle(thePaddle2, -(screenWidth // 2 - paddleOffset))
    draw_ball(theBall)
    reset_ball(theBall)
    # show the results
    theScreen.update()
    # start game's mainloop
    theScreen.ontimer(game_step, 10)


# Set up the game variables
theScreen = turtle.Screen()
theScreen.title(gameName)
theScreen.setup(screenWidth, screenHeight)
theScreen.tracer(False)

# Scores
theScore1Text = turtle.Turtle()
theScore1Text.score = 0
theScore2Text = turtle.Turtle()
theScore2Text.score = 0

# Game objects
thePaddle1 = turtle.Turtle()
thePaddle2 = turtle.Turtle()
theBall = turtle.Turtle()

setup()

# play the game forever
theScreen.mainloop(


'''
Additional Snippets of Code
'''

def isInBounds(projectile):
    """
    Check if the projectile is within the Game bounds.
    """
    return -StudentGameTheme.screenWidth / 2 < projectile.xcor() < StudentGameTheme.screenWidth / 2 and \
           -StudentGameTheme.screenHeight / 2 < projectile.ycor() < StudentGameTheme.screenHeight / 2


def isHit(projectile, target):
    """
    Check if the projectile hits the target.

    Not precise for turned turtles but close enough for the first game
    """
    width = 5 * (projectile.turtlesize()[0] + target.turtlesize()[0]) + projectile.turtlesize()[2] + target.turtlesize()[2]
    height = 5 * (projectile.turtlesize()[1] + target.turtlesize()[1]) + projectile.turtlesize()[2] + target.turtlesize()[2]
    return abs(projectile.xcor() - target.xcor()) < width and abs(projectile.ycor() - target.ycor()) < height
