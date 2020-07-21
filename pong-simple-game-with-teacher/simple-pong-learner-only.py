import math
import pygame
import random
from pygame.locals import *
from sprits import *


# Define some colors
BLACK = (0 ,0, 0)
WHITE = (255, 255, 255)
 
 
# This class represents the ball
# It derives from the "Sprite" class in Pygame
# This class represents the bar at the bottom that the player controls
## Main started
import socket
global client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0', 8080))

client.send(("Init:3:3#").encode())
client.recv(4096)

score1 = 0
score2 = 0
 
# Call this function so the Pygame library can initialize itself
pygame.init()
 

M = 400
N = 600 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([M, N])
 
# Set the title of the window
pygame.display.set_caption('Pong')
 
# Enable this to make the mouse disappear when over our window
pygame.mouse.set_visible(0)
 
# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)
 
# Create a surface we can draw on
background = pygame.Surface(screen.get_size())
 
# Create the ball
ball = Ball()
# Create a group of 1 ball (used in checking collisions)
balls = pygame.sprite.Group()
balls.add(ball)
 
# Create the player paddle object
learner = Player(580, client)
 
movingsprites = pygame.sprite.Group()
movingsprites.add(learner)
movingsprites.add(ball)
 
clock = pygame.time.Clock()
exit_program = False
cnt = 0
f = open("result.txt", "w")
i = 0
while not exit_program:
    i += 1

    if i % 10000 == 0:
        f.flush() 

    # Clear the screen
    screen.fill(BLACK)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
 

    # get the current state
    stateLearner = ((learner.rect.x + learner.width / 2) / M - 0.5, ball.x / M - 0.5, ball.y / N)
    reward = 0

    # Update the player and ball positions
    ball.update()
    actionLearner = learner.update(stateLearner)

    nextStateLearner = ((learner.rect.x + learner.width / 2) / M - 0.5, ball.x / M - 0.5, ball.y / N)

    if ball.y > 600:
        score1 += 1
        client.send(("Push:" + '1' + ':' + str(stateLearner) + ':' + str(actionLearner) + ':' + str(-1) + ':' + str(nextStateLearner) + "#").encode())
        client.recv(4096)

        client.send(("EpisodeFinish:1#").encode())
        client.recv(4096)
        f.write(str(i) + ':' + str(score1) + ':' + str(score2) + '\n')


        ball.reset()
        learner.rect.x = random.randint(0, M - learner.width)

    # See if the ball hits the player paddle
    if pygame.sprite.spritecollide(learner, balls, False):
        client.send(("Push:" + '1' + ':' + str(stateLearner) + ':' + str(actionLearner) + ':' + str(1) + ':' + str(nextStateLearner) + "#").encode())
        client.recv(4096)
        client.send(("EpisodeFinish:1#").encode())
        client.recv(4096)
        score2 += 1
        ball.reset()
        f.write(str(i) + ':' + str(score1) + ':' + str(score2) + '\n')

    else:
        client.send(("Push:" + '1' + ':' + str(stateLearner) + ':' + str(actionLearner) + ':' + str(-1) + ':' + str(nextStateLearner) + "#").encode())
        client.recv(4096)
    

     # Send the current state to the server
    if cnt == 400:
        client.send(("Train#").encode())
        client.recv(4096)
        cnt = 0
    cnt = cnt + 1

    # Print the score
    scoreprint = "Missed Ball: "+ str(score1)
    text = font.render(scoreprint, 1, WHITE)
    textpos = (0, 0)
    screen.blit(text, textpos)

    scoreprint = "Received Ball: "+ str(score2)
    text = font.render(scoreprint, 1, WHITE)
    textpos = (0, 40)
    screen.blit(text, textpos)

    # Draw Everything
    movingsprites.draw(screen)
 
    # Update the screen
    pygame.display.flip()
     
    clock.tick(180)

f.close()

pygame.quit()