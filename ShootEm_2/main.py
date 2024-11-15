"""
Created on Oct 13, 2022

@author: Sangwook Cheon
Time Spent: 10 hours

This module represents my first Arcade game.

Credits:

Resource Used:
- Python Arcade Documentation: https://api.arcade.academy/en/latest/index.html

CREDITS FOR IMAGES USED
Background Image:
Photo by <a href="https://unsplash.com/@jeremyperkins?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Jeremy Perkins</a> on <a href="https://unsplash.com/s/photos/space?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
(from Unsplash, providing royalty-free images)

Spaceship Image:
https://creazilla.com/nodes/31640-moon-rocket-clipart
(from Creazilla, public domain, free for personal and commercial use)

Aestroid Image:
https://www.clipartmax.com/middle/m2K9A0m2d3d3A0A0_moon-clip-art-asteroid-clip-art/
(from ClipartMax, license for personal use)

Bullet Image:
https://pixabay.com/vectors/bullet-shell-cartridge-slug-36942/
(from Pixabay, free for commercial use)

CREDITS FOR AUDIO EFFECTS USED
* I downloaded all sounds from Pixabay, which provides royalty-free audio clips.

Game Begin Sound
Sound Effect from <a href="https://pixabay.com/sound-effects/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=102081">Pixabay</a>

Explosion Sound
Sound Effect from <a href="https://pixabay.com/sound-effects/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=37988">Pixabay</a>

Game Music
Sound Effect from <a href="https://pixabay.com/sound-effects/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=101886">Pixabay</a>

Missile Sound (gun)
Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=82067">Pixabay</a>

Game Over Sound
Sound Effect from <a href="https://pixabay.com/sound-effects/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=6435">Pixabay</a>




How to play the Game:
- You can move around using the arrow keys (forward/backward thrust, and left/right turning)
- You can shoot missiles using the spacebar. If the missile hits the asteroid, both are destroyed.
- Now, if the asteroid is large enough, it will split into two smaller pieces, so be careful.
- The smaller the asteroids are, the faster they move!
- The smaller asteroids are that you shoot down, the higher the points you get.
- You have three lives, and when it's game over, you have the option to start over.
- Now, this game also has sound effects.

Discussion of Fixed Values
- Size of Asteroids: random.uniform(0.06, 0.16) -> this was the range of scale values I used based on the initial image's
size. I randomly created small and large asteroids to fill the game with objects of various speed.
- Number of Asteroids: After playtesting, I determined 10 to be a reasonable number with good difficulty. The asteroids now
also split up, increasing difficulty, so I used less asteroids than the last game.
- Asteroid Movement Speed: I made it so that smaller asteroids move faster - I did this by using the same technique:
asteroid_speed / (scale * 10) - I multiplied scale by 10 to keep each asteroid's score to be one or two digit numbers.
Now the asteroid_speed variable is set to 4 - given the difficulty of maneuvering the rocket, I made asteroids relatively
slow.
- 'player_speed' determines the amount of thrust when moving forward or backward. In the on_key_press method of Game class,
I add / subtract this speed to change_x and change_y each time up / down is pressed - the value 6 made it exciting and difficult
to play after playtesting - need to be careful in each push.
- 'deceleration' models the drift effect - slowing down the player after each push - I multiplied 0.98 to the player's speed
each time it is updated in the update() function of Player class, smoothening out its movement.
- 'turn' determines the degrees turned each time 'Left' or 'Right' key is pressed - I decided it to be 5 degrees - this smaller
value makes sense as the angle is updated constantly during key press until key release.
- When initializing the asteroids at the start of the game (reset_pos function of Asteroid class), I randomly distributed them
across the four sides of the screen and randomly assigned angles within reasonable values - so that there's no complete
vertical or horizontal movement. I also wrote tweak_angle function to slightly change the angle every time an asteroid
goes out of the screen, to add even more randomness to the game (multiplying change_x and change_y by random.uniform(0.8, 1.2)
- I set the missile speed to be 15, making them quite fast - allowing some good prediction shots.


"""
import math
import arcade
import random

screenWidth = 1200
screenHeight = 800
gameName = "Wook's Arcade Asteroids"

deceleration = 0.98
player_speed = 6
turn = 5
lives = 3
asteroid_num = 10
asteroid_speed = 4
missile_speed = 15

# Load Sounds
gun_sound = arcade.load_sound("gun.wav")
explosion_sound = arcade.load_sound("explosion.wav")
game_over_sound = arcade.load_sound("game_over.wav")
game_start_sound = arcade.load_sound("game_begin.wav")
game_music = arcade.load_sound("game_music.wav")

# Load Background image
background = arcade.load_texture("space.jpg")

class Player(arcade.Sprite):

    def __init__(self, image, scale, x, y):
        super().__init__(image, scale)
        self.center_x = x
        self.center_y = y
        self.starting_x = x
        self.starting_y = y

    def reset_player(self):
        """
        Reset the player position to the center of the screen
        """
        self.center_x = self.starting_x
        self.center_y = self.starting_y

    def rotate(self, update_angle):
        # Change the heading of the rocket
        self.angle += update_angle

    def update(self):
        """
        Update the position of the player every frame.
        """

        # Angle of the player in radians
        angle_rad = math.radians(self.angle)

        # Change angle of the player
        self.angle += self.change_angle

        # Change position of the player based on the angle and speed
        self.center_x += - math.sin(angle_rad) * self.change_x
        self.center_y += math.cos(angle_rad) * self.change_y

        # Add Drift Effect
        self.change_x *= deceleration
        self.change_y *= deceleration

        # Check if the player goes out of screen and reposition
        if self.center_x < -40:
            self.center_x = screenWidth + 40
        elif self.center_x > screenWidth + 40:
            self.center_x = -40

        if self.center_y < -40:
            self.center_y = screenHeight + 40
        elif self.center_y > screenHeight + 40:
            self.center_y = -40


class Missile(arcade.Sprite):

    def __init__(self, image, scale, x, y, angle):
        super().__init__(image, scale)
        self.center_x = x
        self.center_y = y
        self.angle = angle

        # Missile's trajectory depends on the player's angle
        self.change_x = -math.sin(math.radians(angle)) * missile_speed
        self.change_y = math.cos(math.radians(angle)) * missile_speed

    def update(self):
        """
        Update the position of the missile every frame
        """
        self.center_x += self.change_x
        self.center_y += self.change_y



class Asteroid(arcade.Sprite):

    def __init__(self, image, scale, x=0, y=0, angle=0):
        super().__init__(image, scale)

        self.center_x = x
        self.center_y = y
        self.angle = angle

        # Only if no designated position is given for the asteroid, randomly set the position
        # This is to differentiate initializing asteroids from splitting asteroids
        if x == 0 and y == 0 and angle == 0:
            self.reset_pos()

        # Speed of the asteroid depends on its size - smaller it is, faster it is.
        self.speed = asteroid_speed / (scale * 10)
        self.change_x = -math.sin(math.radians(self.angle)) * self.speed
        self.change_y = math.cos(math.radians(self.angle)) * self.speed

    def reset_pos(self):
        """
        A function that randomly positions the asteroids to appear from any side of the screen with random angle
        """

        init_pos = random.choice([0, 1])

        # If the choice is 0, asteroid comes out from top or bottom of the screen
        if init_pos == 0:
            self.center_x = random.randrange(0, screenWidth)
            self.center_y = random.choice([0, screenHeight])
            self.angle = random.randrange(210, 330)

        # If the choice is 1, asteroid comes out from right or left side of the screen
        elif init_pos == 1:
            self.center_x = random.choice([0, screenWidth])
            self.center_y = random.randrange(0, screenHeight)
            if self.center_x < 0:
                self.angle = random.randrange(-60, 60)
            else:
                self.angle = random.randrange(150, 230)

    def tweak_angle(self):
        # Each time the asteroid goes out of the screen, this function is called to tweak its angle.
        # This adds more randomness and difficulty to the game.
        self.change_x *= random.uniform(0.8, 1.2)
        self.change_y *= random.uniform(0.8, 1.2)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check if asteroid goes out of screen and reposition and tweak angle
        if self.center_x < -60:
            self.center_x = screenWidth + 60
            self.tweak_angle()
        elif self.center_x > screenWidth + 60:
            self.center_x = -60
            self.tweak_angle()
        if self.center_y < -60:
            self.center_y = screenHeight + 60
            self.tweak_angle()
        elif self.center_y > screenHeight + 60:
            self.center_y = -60
            self.tweak_angle()


class Game(arcade.Window):
    """
    This class controls how the game runs, creating the game window and managing game actions
    """
    def __init__(self):
        super().__init__(screenWidth, screenHeight, gameName)

        # Create Player
        self.thePlayer = Player("rocket1.png", 0.1, screenWidth // 2, screenHeight // 2)

        # Create Asteroids
        self.asteroid_list = []

        # This is a list that only contains asteroids that split after collision with missile.
        self.asteroid_split_list = []

        for i in range(asteroid_num):
            self.asteroid_list.append(Asteroid("asteroid.png", random.uniform(0.06, 0.16)))

        self.missile_list = []

        # Create Texts
        self.end_text = ''

        self.score = 0
        self.lives = lives
        self.initial_lives = lives

        # Boolean for shooting missiles
        self.shoot_missile = True

        # Boolean for starting the game when first opening the game
        self.start_game = False

    def setup(self):
        # Set up the initial game scene
        arcade.set_background_color(arcade.color.BLACK)
        arcade.play_sound(game_music)


    def reset_game(self):
        self.asteroid_list.clear()
        self.asteroid_split_list.clear()
        self.missile_list.clear()

        self.thePlayer = Player("rocket1.png", 0.1, screenWidth // 2, screenHeight // 2)

        for i in range(asteroid_num):
            self.asteroid_list.append(Asteroid("asteroid.png", random.uniform(0.06, 0.16)))

        arcade.play_sound(game_music)

        self.score = 0
        self.lives = self.initial_lives
        self.shoot_missile = True

    def reset_round(self):
        self.asteroid_list.clear()
        self.asteroid_split_list.clear()
        self.missile_list.clear()

        arcade.play_sound(game_start_sound)

        self.thePlayer = Player("rocket1.png", 0.1, screenWidth // 2, screenHeight // 2)

        for i in range(asteroid_num):
            self.asteroid_list.append(Asteroid("asteroid.png", random.uniform(0.06, 0.16)))

        self.shoot_missile = True

    # This is where change happens.
    def on_update(self, dt):
        # if arcade.check_for_collision(self.thePlayer):
        self.thePlayer.update()

        if self.lives == 0:
            self.thePlayer.remove_from_sprite_lists()
            self.asteroid_list.clear()
            self.asteroid_split_list.clear()
            self.missile_list.clear()
            self.shoot_missile = False
            self.end_text = "Game Over! Press 'R' to Restart"


        # Update the asteroid and check collision
        for asteroid in self.asteroid_list:
            asteroid.update()
            if arcade.check_for_collision(self.thePlayer, asteroid):
                self.thePlayer.reset_player()

                asteroid.reset_pos()

                self.lives -= 1

                arcade.play_sound(game_over_sound)

                self.thePlayer.remove_from_sprite_lists()
                self.asteroid_list.clear()
                self.asteroid_split_list.clear()
                self.missile_list.clear()
                self.shoot_missile = False
                self.end_text = "Press 'C' to Continue"

        for asteroid in self.asteroid_split_list:
            asteroid.update()
            if arcade.check_for_collision(self.thePlayer, asteroid):
                self.thePlayer.reset_player()

                asteroid.reset_pos()

                self.lives -= 1

                self.thePlayer.remove_from_sprite_lists()
                self.asteroid_list.clear()
                self.asteroid_split_list.clear()
                self.missile_list.clear()
                self.shoot_missile = False
                self.end_text = "Press 'C' to Continue"


        # Update Missiles and check collision with asteroids
        for missile in self.missile_list:
            missile.update()

            # Check of asteroid_list collision
            for asteroid in self.asteroid_list:
                if arcade.check_for_collision(asteroid, missile):
                    self.missile_list.remove(missile)

                    arcade.play_sound(explosion_sound)

                    # Add asteroid split
                    if asteroid.scale > 0.10:
                        self.asteroid_split_list.append(
                            Asteroid("asteroid.png", asteroid.scale / 1.8, asteroid.center_x, asteroid.center_y,
                                     asteroid.angle + 40))

                        self.asteroid_split_list.append(
                            Asteroid("asteroid.png", asteroid.scale / 1.2, asteroid.center_x, asteroid.center_y,
                                     asteroid.angle - 40))

                    asteroid.reset_pos()
                    self.score += round(1 / asteroid.scale)

            # Check of asteroid_split_list collision
            for asteroid in self.asteroid_split_list:
                if arcade.check_for_collision(asteroid, missile):

                    arcade.play_sound(explosion_sound)

                    try:
                        self.missile_list.remove(missile)
                        self.asteroid_split_list.remove(asteroid)
                        self.score += round(1 / asteroid.scale)
                    except:
                        arcade.draw_text('Remove Error Occurred', screenWidth // 2 , screenHeight // 2, arcade.color.RED, 100)

        # If missile goes out of screen, remove it to save computing power
        for missile in self.missile_list:
            if missile.center_x < -500 or missile.center_x > screenWidth + 500 or missile.center_y < -500 or missile.center_y > screenHeight + 500:
                self.missile_list.remove(missile)



    def on_draw(self):

        # Clear the screen before drawing again

        # Draw background first
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            screenWidth, screenHeight,
                                            background)

        arcade.draw_text(
            "Wook's Asteroids",
            20, screenHeight // 2,
            arcade.color.CYAN,
            50,
            10,
            "left",
            "Kenney Pixel Square"
        )

        arcade.draw_text(
            "Press 'ENTER' to Begin the Game",
            20, screenHeight // 2 - 70,
            arcade.color.CYAN,
            25,
            10,
            "left",
            "Kenney Pixel Square"
        )

        if self.start_game:
            self.clear()

            # Draw background again because the screen is cleared.
            arcade.draw_lrwh_rectangle_textured(0, 0,
                                                screenWidth, screenHeight,
                                                background)

            # Draw the player
            self.thePlayer.draw()

            # Draw Text

            # Draw Score
            arcade.draw_text(
                "Score:: " + str(self.score), # str(self.score)
                20, 20,
                arcade.color.YELLOW,
                20,
                10,
                "left",
                "Kenney Pixel Square"
            )

            # Draw Lives
            arcade.draw_text(
                "Lives: " + str(self.lives), # str(self.lives)
                20, 60,
                arcade.color.GREEN,
                20,
                10,
                "left",
                "Kenney Pixel Square"
            )

            arcade.draw_text(
                self.end_text,
                20, screenHeight // 2,
                arcade.color.CYAN,
                40,
                10,
                "left",
                "Kenney Pixel Square"
            )

            for asteroid in self.asteroid_list:
                asteroid.draw()

            for asteroid in self.asteroid_split_list:
                asteroid.draw()

            for missile in self.missile_list:
                missile.draw()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.thePlayer.change_x += player_speed
            self.thePlayer.change_y += player_speed
        if key == arcade.key.DOWN:
            self.thePlayer.change_x -= player_speed
            self.thePlayer.change_y -= player_speed
        if key == arcade.key.RIGHT:
            self.thePlayer.change_angle = -turn
        if key == arcade.key.LEFT:
            self.thePlayer.change_angle = turn
        if key == arcade.key.R:
            if self.lives == 0:
                self.end_text = ''
                self.reset_game()
        if key == arcade.key.C:
            self.end_text = ''
            self.reset_round()

        # Shoot Missile
        if key == arcade.key.SPACE:
            if self.shoot_missile:
                self.missile_list.append(Missile("bullet.png", 0.1, self.thePlayer.center_x, self.thePlayer.center_y, self.thePlayer.angle))
                arcade.play_sound(gun_sound)

        # Begin the Game
        if key == arcade.key.ENTER:
            self.start_game = True
            if self.start_game:
                self.reset_game()
                self.clear()

    def on_key_release(self, key, modifiers):
        # if key == arcade.key.UP or key == arcade.key.DOWN:
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.thePlayer.change_angle = 0


# Open up a window with a width, height, and title
# arcade.open_window(screenWidth, screenHeight, gameName)
window = Game()
window.setup()
# Keep the window up until the player closes it
arcade.run()