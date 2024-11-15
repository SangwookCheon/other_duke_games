"""
Created on Oct 13, 2022

@author: Sangwook Cheon

Hours Spent: 10 Hours

HOW TO PLAY 'Save the Fuel'
- Objective of the game is to stay afloat until all enemies are gone using provided fuel and ability to shoot
- You win when all enemies are cleared from the screen. You lose when:
    - You run out of fuel!
    - You go above or below the screen limits.
- You have three lives to go as far as possible in levels completed. There are 5 levels in total. They are quite difficult.
- Press 'SPACE' to activate the jetpack, which will keep you in the air but continuously use up fuel. Manage it wisely!
- You can recharge your fuel by colliding with a yellow star. Small enemies also leave behind a star when you shoot them down!
- You can shoot a bullet by pressing 'M', which will destroy the first enemy it hits.
but be careful: each fire will use a significant portion of your fuel.
- Also, be aware that colliding with an enemy head-on will drain your fuel based on the enemy's size. The bigger it is,
the larger the drop.
- At any time, you can press 'ENTER' to reset the entire game.
- You can also press 'q' to play level 1, 'w' for level 2, 'e' for level 3, 'r' for level 4, and 't' for level 5 for
debugging reasons (or... if you cannot complete a level... they are indeed very hard)

DISCUSSION OF FIXED VALUES
Wow, I didn't use ANY randomness in this game. Below are my fixed values:

PLAYER_ACCELERATION
BULLET_SPEED = 10
    - Fast enough to be clearly visible, considering its small size.
STARTING_FUEL = 200
    - Goes hand-in-hand with amount of FUEL_DRAIN below.
FUEL_DRAIN = 0.7
    - This was the hardest to choose - this was enough to keep the player afloat for enough time before the player has no
    choice but to look for fuel recharges.
FUEL_BULLET_DRAIN = 15
    - 15 seemed to make firing a bullet a significant investment of fuel - if it is too small, then there is no motivation to
    save bullets.
FUEL_COLLIDE_DRAIN = 80
    - This is the starting value - the drain due to collision depends on the size of the enemy.
FUEL_BOOST = 100
    - Fuel Boost is larger than all the drops in fuel to have net positive gain in fuel - keeps the
NUM_LIVES = 3
    - It will take multiple tries to complete 5 levels with three lives!

Each level had a separate text file with position of enemies and their movement speed.
I followed the following general principle:
    - The Enemy 1 is the slowest and often largest - so they don't leave behind an item when shot down - the best bet
    for the player is to simply dodge them, rather than waste their fuel shooting them down. I used them mainly for Level 1 and 2
    because their slow movement is suitable for easy levels.
    - Enemy 2 is faster - some of them are small enough to leave an item - so player is often tempted to shoot them down
    even with the risk of collision.
    - Enemy 3 is super fast and small - all of them leave an item, and due to their small size, colliding with them doesn't
    cause a huge drop in fuel. So, the player would be very tempted to shoot them down, at the risk of missing them with
    the bullets, thus wasting fuel. Difficult levels (3, 4, 5) all have these to add excitement and element of risk-taking.
    In Level 5, in fact, you cannot complete the level unless you shoot some of them down successfully, because the fuel
    will run out!
    - These enemies and items were combined to restrict the available paths of the player, and to encourage certain behaviors,
    such as targeting Enemy 3 for extra items.

NOTE TO SELF:

I had a lagging issue for a long time, but deciding to draw obstacles only when it appears solved the issue like magic.
# Draw the obstacles based on its time of appearance
for obstacle in self.obstacle_list:
    if self.timer >= obstacle.dt:
        obstacle.draw()

RESOURCES USED:

Bullet - Open Game Art
https://opengameart.org/content/bullet-collection-different-colors

Enemies - Open Game Art
Enemy 1: https://opengameart.org/content/skull-in-a-ufo-spacecraft
Enemy 2: https://opengameart.org/content/ufo-enemy-game-character
Enemy 3: https://opengameart.org/content/enemy-game-character-ufo-spaceship

Background image: Open Game Art
https://opengameart.org/content/fluffy-clouds

Main Player: Open Game Art
https://opengameart.org/content/monkey-on-mars-share-the-love

"""

import arcade
import random
import math

GAME_NAME = "Save the Fuel"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Game Variables
PLAYER_ACCELERATION = 3
BULLET_SPEED = 10
STARTING_FUEL = 200
FUEL_DRAIN = 0.7
FUEL_BULLET_DRAIN = 15
FUEL_COLLIDE_DRAIN = 80
FUEL_BOOST = 100
NUM_LIVES = 3


# Images and Font
FONT = "Kenney Future"
ENEMY_1 = 'enemy1.png'
ENEMY_2 = ''
ITEM_1_SRC = 'item.png'
PLAYER_LAUNCH_SRC = 'player2.png'
BACKGROUND_SRC = 'background1.png'
BULLET_SRC = 'bullet.png'

# Load Sounds

# Load Background image

class Player(arcade.Sprite):

    def __init__(self, image, scale, x, y):
        super().__init__(image, scale)
        self.center_x = x
        self.center_y = y
        self.pressed = False

    def update(self):

        # If the spacebar is pressed, increase y velocity by 0.3. Otherwise keep it decreasing at 0.3
        if self.pressed:
            self.change_y += 0.3
        else:
            self.change_y -= 0.3

        self.center_y += self.change_y


class Missile(arcade.Sprite):
    def __init__(self, image, scale, x, y):
        super().__init__(image, scale)
        self.center_x = x
        self.center_y = y
        self.change_x = BULLET_SPEED

    def update(self):
        self.center_x += self.change_x

class Fuel(arcade.SpriteSolidColor):
    def __init__(self, width, height, color, x, y):
        super().__init__(width, height, color)
        self.width = width
        self.height = height
        self.color = color
        self.center_x = x
        self.center_y = y

class Obstacle(arcade.Sprite):
    def __init__(self, image, scale, y, dx, dt):
        super().__init__(image, scale)
        self.center_x = SCREEN_WIDTH + 100
        self.center_y = y
        self.change_x = dx
        self.dt = dt

    def update(self):
        self.center_x += self.change_x

class Item(arcade.Sprite):
    def __init__(self, image, scale, y, dx, dt, x_specified=0):
        super().__init__(image, scale)

        # If the center-x is specified (in case item spawns where enemy is destroyed) then this is used.
        if x_specified != 0:
            self.center_x = x_specified
        else:
            self.center_x = SCREEN_WIDTH + 100
        self.center_y = y
        self.change_x = dx
        self.dt = dt

    def update(self):
        self.center_x += self.change_x


class Background(arcade.Sprite):
    def __init__(self, image, scale, dx):
        super().__init__(image, scale)
        self.center_x = SCREEN_WIDTH
        self.center_y = SCREEN_HEIGHT // 2
        self.change_x = dx

    def update(self):
        self.center_x += self.change_x


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME)

        # Timer used to deermine how long spacebar is pressed.
        self.timer = 0
        self.begin_time = 0
        self.fuel = STARTING_FUEL

        # Set of boolean values to determine various game states, used mainly for displaying separate messages.
        self.game_start = False
        self.game_over = False
        self.current_level = 1
        self.level_passed = False
        self.restart_level = False

        self.lives = NUM_LIVES

        self.score = 0

        # Create Player
        self.thePlayer = Player(PLAYER_LAUNCH_SRC, 3, 200, SCREEN_HEIGHT // 2)

        # Create Fuel Bar
        self.theFuel = Fuel(self.fuel, 10, arcade.color.RED, 100, 50)

        # Create Bullet List
        self.bullet_list = []

        # Create objects by reading the file
        self.obstacle_list = []
        self.item_list = []

        # Set background
        self.background = Background(BACKGROUND_SRC, 3, -1)

        # Read initial level 1
        self.read_level(self.current_level)


    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)

    def read_level(self, name):

        self.obstacle_list.clear()
        self.item_list.clear()

        self.background = Background(BACKGROUND_SRC, 3, -1)

        # Read level by opening text file in the format "Level_{}.txt"
        with open("Level_{}.txt".format(str(name))) as file:
            for line in file:
                vals = line.split(',')
                if str(vals[0]) == 'o':
                    obstacle = Obstacle(str(vals[1]), float(vals[2]), float(vals[3]), float(vals[4]), float(vals[5]))
                    self.obstacle_list.append(obstacle)
                elif str(vals[0]) == 'i':
                    item = Item(str(vals[1]), float(vals[2]), float(vals[3]), float(vals[4]), float(vals[5]))
                    self.item_list.append(item)

    def reset_game(self):

        # Reset the entire game back to level 1
        self.clear()

        self.timer = 0
        self.begin_time = 0
        self.fuel = STARTING_FUEL

        self.game_over = False
        self.current_level = 1
        self.level_passed = False
        self.restart_level = False

        self.lives = NUM_LIVES

        self.score = 0

        # Create Player
        self.thePlayer = Player(PLAYER_LAUNCH_SRC, 3, 200, SCREEN_HEIGHT // 2)
        self.acc = 1

        # Create Fuel Bar
        self.theFuel = Fuel(self.fuel, 10, arcade.color.RED, 100, 50)

        # Create Bullet List
        self.bullet_list = []

        # Create objects by reading the file
        self.obstacle_list = []
        self.item_list = []

        # Set background
        self.background = Background(BACKGROUND_SRC, 3, -1)

        self.read_level(self.current_level)

    def reset_level(self):

        # Only reset level - not the entire game.
        self.clear()

        self.timer = 0
        self.begin_time = 0
        self.fuel = STARTING_FUEL

        self.game_over = False
        self.level_passed = False
        self.restart_level = False

        # Create Player
        self.thePlayer = Player(PLAYER_LAUNCH_SRC, 3, 200, SCREEN_HEIGHT // 2)

        # Create Fuel Bar
        self.theFuel = Fuel(self.fuel, 10, arcade.color.RED, 100, 50)

        # Create Bullet List
        self.bullet_list = []

        # Create objects by reading the file
        self.obstacle_list = []
        self.item_list = []

        self.read_level(self.current_level)

        # Set background
        self.background = Background(BACKGROUND_SRC, 3, -1)


    def on_update(self, dt):

        self.background.update()

        # If lives is 0, game is over.
        if self.lives == 0:
            self.game_over = True

        if not self.game_over and not self.level_passed and not self.restart_level and self.game_start:

            self.timer += dt

            # Update the player
            self.thePlayer.update()

            # Update the bullets
            for bullet in self.bullet_list:
                bullet.update()

                # Remove bullets that are out of bounds
                if bullet.center_x >= SCREEN_WIDTH - 10:
                    self.bullet_list.remove(bullet)

            # Update the obstacle that are supposed to appear on time
            for obstacle in self.obstacle_list:
                if self.timer >= obstacle.dt:
                    obstacle.update()

                # Remove obstacles out of bounds
                if obstacle.center_x <= -100:
                    self.obstacle_list.remove(obstacle)

            # Update the items
            for item in self.item_list:
                if self.timer >= item.dt:
                    item.update()

            # Update the fuel
            if self.thePlayer.pressed:
                # First check if deducting fuel makes it less than or equal to 0 - then game is over
                if self.fuel - FUEL_DRAIN <= 0:
                    if self.lives == 1:
                        self.game_over = True
                    else:
                        self.restart_level = True
                        self.lives -= 1
                else:
                    self.fuel -= FUEL_DRAIN

            # Update the width of fuel bar
            self.theFuel.width = self.fuel

            # Check player out of bounds
            if self.thePlayer.center_y >= SCREEN_HEIGHT or self.thePlayer.center_y <= 0:
                self.lives -= 1

                if self.lives != 0:
                    self.restart_level = True

            # Check player - obstacle collision
            for obstacle in self.obstacle_list:
                if arcade.check_for_collision(self.thePlayer, obstacle):
                    if self.fuel - FUEL_COLLIDE_DRAIN * obstacle.scale <= 0:

                        if self.lives == 1:
                            self.game_over = True
                        else:
                            self.lives -= 1
                            self.restart_level = True

                    else:
                        self.fuel -= FUEL_COLLIDE_DRAIN * obstacle.scale
                        self.obstacle_list.remove(obstacle)

            # Check missile - obstacle collision
            for bullet in self.bullet_list:
                for obstacle in self.obstacle_list:
                    if arcade.check_for_collision(bullet, obstacle):

                        # Small objects leave behind a fuel boost item
                        if obstacle.scale < 0.5:
                            item = Item(ITEM_1_SRC, 0.05, obstacle.center_y, obstacle.change_x, 0, obstacle.center_x)
                            self.item_list.append(item)

                        # I saw game-breaking errors occasionally happening when trying to remove an obstacle
                        # so try/except is used.
                        try:
                            self.obstacle_list.remove(obstacle)
                            self.bullet_list.remove(bullet)
                        except:
                            pass

            # Check player - item collision
            for item in self.item_list:
                if arcade.check_for_collision(self.thePlayer, item):

                    # Fuel boost
                    self.fuel += FUEL_BOOST

                    # Remove the item after it is used
                    self.item_list.remove(item)

            # Check if level is successful
            if len(self.obstacle_list) == 0:
                # Scoring is based on remaining fuel.
                self.score += self.fuel
                self.level_passed = True


    def on_draw(self):

        if not self.game_start:
            self.clear()

            self.background.draw()

            arcade.draw_text('Save the Fuel', 25, SCREEN_HEIGHT // 2 + 50, arcade.color.DUKE_BLUE, 35, font_name=FONT)
            arcade.draw_text('Press Space to Begin', 25, SCREEN_HEIGHT // 2, arcade.color.DUKE_BLUE, 20, font_name=FONT)
            arcade.draw_text('Press ENTER to reset the entire game', 25, SCREEN_HEIGHT // 2 - 50, arcade.color.DUKE_BLUE, 20, font_name=FONT)

        if not self.game_over and not self.level_passed and not self.restart_level and self.game_start:
            self.clear()

            self.background.draw()

            # Draw the player
            self.thePlayer.draw()

            # Draw Fuel Bar
            self.theFuel.draw()
            # arcade.draw_text(self.fuel, SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2, arcade.color.RED, 100)
            arcade.draw_rectangle_filled(50, 50, 100, 30, arcade.color.SKY_BLUE)
            arcade.draw_text('FUEL', 25, 45, arcade.color.RED, 15, font_name=FONT)

            # Draw the Lives

            arcade.draw_text('LIVES:  ' + str(self.lives), 25, 75, arcade.color.RED, 15, font_name=FONT)

            # Draw the Bullets
            for bullet in self.bullet_list:
                bullet.draw()

            # Draw the obstacles based on its time of appearance
            for obstacle in self.obstacle_list:
                if self.timer >= obstacle.dt:
                    obstacle.draw()

            # Draw items
            for item in self.item_list:
                item.draw()

        elif self.game_over:
            self.clear()
            arcade.draw_text('GAME OVER', 25, SCREEN_HEIGHT // 2, arcade.color.RED, 50, font_name=FONT)
            arcade.draw_text("Press C to restart", 25, SCREEN_HEIGHT // 2 - 50, arcade.color.ORANGE, 20, font_name=FONT)

        elif self.level_passed and self.current_level != 5:
            self.clear()
            arcade.draw_text('Level ' + str(self.current_level) + ' Passed!', 25, SCREEN_HEIGHT // 2, arcade.color.CYAN,
                             30, font_name=FONT)
            arcade.draw_text("Press C to continue", 25, SCREEN_HEIGHT // 2 - 50, arcade.color.ORANGE, 20, font_name=FONT)
            arcade.draw_text("Total Score: " + str(int(self.score)), 25, SCREEN_HEIGHT // 2 - 100, arcade.color.ORANGE, 20, font_name=FONT)

        elif self.level_passed and self.current_level == 5:
            self.clear()
            arcade.draw_text('MISSION ACCOMPLISHED!', 25, SCREEN_HEIGHT // 2, arcade.color.CYAN, 30, font_name=FONT)
            arcade.draw_text('Total Score: ' + str(int(self.score)), 25, SCREEN_HEIGHT // 2 - 100, arcade.color.CYAN, 20, font_name=FONT)

        elif self.restart_level:
            self.clear()
            arcade.draw_text('MISSION FAILED!', 25, SCREEN_HEIGHT // 2, arcade.color.RED, 30, font_name=FONT)
            arcade.draw_text("Press C to continue", 25, SCREEN_HEIGHT // 2 - 50, arcade.color.ORANGE, 30, font_name=FONT)

    def on_key_press(self, key, modifiers):

        if not self.game_start:
            if key == arcade.key.SPACE:
                self.game_start = True

        if not self.game_over and not self.level_passed and not self.restart_level:
            # Use jetpack
            if key == arcade.key.SPACE:
                # Record the time when the space is pressed
                self.begin_time = self.timer
                self.thePlayer.change_y += 1
                self.thePlayer.pressed = True

            # Shoot bullets
            if key == arcade.key.M:
                self.bullet_list.append(Missile(BULLET_SRC, 0.8, self.thePlayer.center_x, self.thePlayer.center_y))

                # Firing a bullet uses fuel
                if self.fuel - FUEL_BULLET_DRAIN <= 0:
                    if self.lives == 1:
                        self.game_over = True
                    else:
                        self.lives -= 1
                        self.restart_level = True
                else:
                    self.fuel -= FUEL_BULLET_DRAIN

        if key == arcade.key.ENTER:
            self.reset_game()

        elif self.restart_level:
            if key == arcade.key.C:
                self.reset_level()

        elif self.game_over:
            if key == arcade.key.C:
                self.reset_game()

        # Continue when level is completed
        elif self.level_passed:
            if key == arcade.key.C and self.current_level != 5:
                self.fuel = STARTING_FUEL
                self.current_level += 1
                self.timer = 0
                self.read_level(self.current_level)
                self.level_passed = False


        # Access to individual levels for debugging
        elif key == arcade.key.Q:
            self.fuel = STARTING_FUEL
            self.current_level = 1
            self.timer = 0
            self.read_level(self.current_level)
            self.level_passed = False

        elif key == arcade.key.W:
            self.fuel = STARTING_FUEL
            self.current_level = 2
            self.timer = 0
            self.read_level(self.current_level)
            self.level_passed = False

        elif key == arcade.key.E:
            self.fuel = STARTING_FUEL
            self.current_level = 3
            self.timer = 0
            self.read_level(self.current_level)
            self.level_passed = False

        elif key == arcade.key.R:
            self.fuel = STARTING_FUEL
            self.current_level = 4
            self.timer = 0
            self.read_level(self.current_level)
            self.level_passed = False

        elif key == arcade.key.T:
            self.fuel = STARTING_FUEL
            self.current_level = 5
            self.timer = 0
            self.read_level(self.current_level)
            self.level_passed = False


    def on_key_release(self, key, modifiers):
        if not self.game_over:
            if key == arcade.key.SPACE:
                self.thePlayer.change_y -= -1
                self.acc = 1
                self.thePlayer.pressed = False


# Open up a window with a width, height, and title
window = Game()
window.setup()
# Keep the window up until the player closes it
arcade.run()