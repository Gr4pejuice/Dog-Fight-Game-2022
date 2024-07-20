import pygame
import math
from pygame.locals import QUIT
from classes import *
pygame.init()

width = 900
height = 500

RED  =(255,0,0)                         
GREEN=(0,255,0)                   # define the main colours: R,G,B
BLUE =(0,0,255)                        
BLACK=(0,0,0)
WHITE = (255,255,255)

screen = pygame.display.set_mode((width, height))

#init timer
clock = pygame.time.Clock()

#global variables
playerx = 100
playery = height / 2
player_angle = math.pi
angle = 0

line_length = 40

speed = 7
bullet_speed = 20

bullet_visible = False

#images
background = pygame.image.load("bg.png")
background = pygame.transform.scale(background, (width,height))

plane = pygame.image.load("plane.png")
plane = pygame.transform.scale(plane, (50,100))
picW = plane.get_width()

def redraw():
    # screen.fill(WHITE)
    screen.blit(background, (0,0))

    #draw player
    # pygame.draw.circle(screen, RED, (playerx, playery), 10)
    plane_copy = pygame.transform.rotate(plane, angle)
    screen.blit(plane_copy,(playerx - int(plane_copy.get_width()/2), playery - int(plane_copy.get_height()/2)))

    #draw direction
    pygame.draw.line(screen, GREEN, (playerx, playery) , (playerx - math.sin(player_angle) * line_length, playery + math.cos(player_angle) * line_length), 3)

    #draw bullet
    if bullet_visible:
        pygame.draw.circle(screen, BLACK, (bulletx, bullety), 5)
    
    pygame.display.update()


#main game
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    #get user input
    keys = pygame.key.get_pressed()

    #handle user input
    if keys[pygame.K_LEFT]:
        player_angle -= 0.1
        angle += 5.735

    if keys[pygame.K_RIGHT]:
        player_angle += 0.1
        angle -= 5.735

    #shoot bullet
    if keys[pygame.K_UP] and bullet_visible == False:
        bulletx = playerx
        bullety = playery
        bullet_angle = player_angle
        bullet_visible = True

    #move player
    playerx += -math.sin(player_angle) * speed
    playery += math.cos(player_angle) * speed

    #move bullet
    if bullet_visible:
        bulletx += -math.sin(bullet_angle) * bullet_speed
        bullety += math.cos(bullet_angle) * bullet_speed
        #remove bullet if hit wall (or other player)
        if bulletx < 0:
            bullet_visible = False
        if bulletx > width:
            bullet_visible = False
        if bullety < 0:
            bullet_visible = False
        if bullety > height:
            bullet_visible = False
    
  
    #wall collisions with player
    if playerx <= 0:
        playerx = 0

    if playerx >= width:
        playerx = width

    if playery <= 0:
        playery = 0

    if playery >= height:
        playery = height

    redraw()

    #set FPS
    clock.tick(30)