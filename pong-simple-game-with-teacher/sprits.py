import math
import pygame
import random
from pygame.locals import *
BLACK = (0 ,0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GAIN = 1
class Ball(pygame.sprite.Sprite):
 
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Create the image of the ball
        self.image = pygame.Surface([10, 10])
 
        # Color the ball
        self.image.fill(WHITE)
 
        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()
 
        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
        # Speed in pixels per cycle
        self.speed = 0
 
        # Floating point representation of where the ball is
        self.x = 0
        self.y = 0

        self.prevX = 0
        self.prevY = 0 


        # Direction of ball in degrees
        self.direction = 0
 
        # Height and width of the ball
        self.width = 10
        self.height = 10
 
        # Set the initial ball speed and position
        self.reset()
 
    def reset(self):
        # self.x = random.randrange(50,350)
        self.x = 200
        self.prevX = -1
        self.y = 10
        self.prevY = -1
        self.speed= 10 * GAIN
 
        # Direction of ball (in degrees)
        self.direction = random.randrange(-10,10)
        self.direction += 180
        

    # This function will bounce the ball off a horizontal surface (not a vertical one)
    def bounce(self,diff):
        self.direction = (180-self.direction)%360
        if (self.direction % 90) == 0:
            self.reset()
        self.direction -= diff
 
    # Update the position of the ball
    def update(self):
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)
 
        self.prevX = self.x
        self.prevY = self.y

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y
 
        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360-self.direction)%360
        
        if (self.direction % 90) == 0:
            self.reset()
            # print(self.direction)
            #self.x=1
 
        # Do we bounce of the right side of the screen?
        if self.x > self.screenwidth-self.width:
            self.direction = (360-self.direction)%360
         
class Player(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, y_pos, client):
        # Call the parent's constructor
        super().__init__()
 
        self.width=75
        self.height=15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.client = client
        self.rect.x = 200
        self.rect.y = y_pos
 
    # Update the player
    def update(self, state):
 
        # This gets the position of the axis on the game controller
        # It returns a number between -1.0 and +1.0

        horiz_axis_pos = 0

        self.client.send(("GetAction:"  + str(state) + "#").encode())
        replyStr = self.client.recv(65536).decode()

        if (replyStr == '2'):
            horiz_axis_pos = 1
        elif (replyStr == '0'):
            horiz_axis_pos = -1
        elif (replyStr == '1'):
            horiz_axis_pos = 0

        # Move x according to the axis. We multiply by 15 to speed up the movement.
        self.rect.x=int(self.rect.x+horiz_axis_pos * 10 * GAIN)
 
        # Make sure we don't push the player paddle off the right side of the screen
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width
        if self.rect.x < 0:
            self.rect.x = 0

        return replyStr

         
class Teacher(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, y_pos, client):
        # Call the parent's constructor
        super().__init__()
 
        self.width=5
        self.height=15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.client = client
        self.rect.x = 200
        self.rect.y = y_pos
 
    # Update the player
    def update(self, ball):
 
        # This gets the position of the axis on the game controller
        # It returns a number between -1.0 and +1.0

        horiz_axis_pos = 0
        replyStr = '1'
        if ball.x < self.rect.x + self.width / 2:
            horiz_axis_pos = -1
            replyStr = '0'
        elif ball.x > self.rect.x + self.width / 2:
            horiz_axis_pos = 1
            replyStr = '2'
        # Move x according to the axis. We multiply by 15 to speed up the movement.
        self.rect.x=int(self.rect.x+horiz_axis_pos * 10 * GAIN)
 
        # Make sure we don't push the player paddle off the right side of the screen
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width
        if self.rect.x < 0:
            self.rect.x = 0

        return replyStr
