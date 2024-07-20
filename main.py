import pygame
import math
import time
from random import randint
from pygame.locals import QUIT
from classes import *

pygame.init()

width = 900
height = 550

RED = (255, 0, 0)
GREEN = (0, 255, 0)  # define the main colours: R,G,B
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((width, height))

#init timer
clock = pygame.time.Clock()

#font
font = pygame.font.SysFont("Arial Black", 50)

#global variables
playerx = 100
playery = height / 2
playerx_2 = width - 100
playery_2 = height / 2

powerup_x = randint(0, width - 80)
powerup_y = height - 100

bullet_visible = False

#------------images----------------------#
#background
background = pygame.image.load("bg.png")
background = pygame.transform.scale(background, (width, height))

#planes
plane = pygame.image.load("plane.png")
plane = pygame.transform.scale(plane, (50, 100))

plane2 = pygame.image.load("plane2.png")
plane2 = pygame.transform.scale(plane2, (50, 100))

#health hearts
player1_heart = pygame.image.load("heart1.png")
player1_heart = pygame.transform.scale(player1_heart, (50, 40))
player2_heart = pygame.image.load("heart2.png")
player2_heart = pygame.transform.scale(player2_heart, (50, 40))

#countdown
count_3 = pygame.image.load("3.png")
count_3 = pygame.transform.scale(count_3, (200, 200))
count_2 = pygame.image.load("2.png")
count_2 = pygame.transform.scale(count_2, (200, 200))
count_1 = pygame.image.load("1.png")
count_1 = pygame.transform.scale(count_1, (200, 200))
count_GO = pygame.image.load("GO.png")
count_GO = pygame.transform.scale(count_GO, (width, 400))

count_list = [count_3, count_2, count_1, count_GO]

#----intro/end screens-----#
#intro screen#
intro_screen_image = pygame.image.load("introscreen.png")
intro_screen_image = pygame.transform.scale(intro_screen_image,
                                            (width, height))

#game over screens#
gameover_red_image = pygame.image.load("gameover_red_wins.png")
gameover_red_image = pygame.transform.scale(gameover_red_image,
                                            (width, height))
gameover_blue_image = pygame.image.load("gameover_blue_wins.png")
gameover_blue_image = pygame.transform.scale(gameover_blue_image,
                                             (width, height))
gameover_draw_image = pygame.image.load("gameover_draw.png")
gameover_draw_image = pygame.transform.scale(gameover_draw_image,
                                             (width, height))

#instructions#
instructions_image = pygame.image.load("instructions.png")
instructions_image = pygame.transform.scale(instructions_image,
                                            (width, height))

#powerup#
powerup_image = pygame.image.load("airdrop.png")
powerup_image = pygame.transform.scale(powerup_image, (80, 100))

#------------audio----------------------#
countdown_audio = pygame.mixer.Sound("321GO!.mp3")

damage_audio = pygame.mixer.Sound("take_damage.mp3")

shoot_audio = pygame.mixer.Sound("gunshoot.mp3")

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)


#-----------functions-----------------#
#starting screen
def intro_screen():
    screen.blit(intro_screen_image, (0, 0))
    pygame.display.update()


def instruction_screen():
    screen.blit(instructions_image, (0, 0))
    pygame.display.update()


#initial countdown once main game begins
def countdown():
    current_screen = screen.copy()
    global countdown_finished
    if countdown_finished == False:
        countdown_audio.play()
        #goes through list of countdown images and blits them
        for i in count_list:
            screen.blit(current_screen, (0, 0))
            screen.blit(i, (width / 2 - i.get_width() / 2,
                            height / 2 - i.get_height() / 2))
            pygame.display.flip()
            if i == count_GO:
                countdown_finished = True
            time.sleep(1)
            pygame.display.update()


#checks how the game ends and blits the cooresponding end screen
def gameover():
    if player1.plane_health <= 0 and player2.plane_health <= 0:
        screen.blit(gameover_draw_image, (0, 0))

    elif player2.plane_health <= 0:
        screen.blit(gameover_red_image, (0, 0))

    elif player1.plane_health <= 0:
        screen.blit(gameover_blue_image, (0, 0))

    pygame.display.update()


#draws everything in the main game
def redraw():
    screen.blit(background, (0, 0))

    #draw player
    player1.rotate_plane(plane)
    player1.draw_plane()

    player2.rotate_plane(plane2)
    player2.draw_plane()

    #draw direction
    # player1.draw_direction(line_length)

    #shoots bullets
    if bullet_shot1:
        player1.shoot_bullet(width, height)

    if bullet_shot2:
        player2.shoot_bullet(width, height)

    #draw health
    for i in range(player1.plane_health):
        screen.blit(player1_heart, (i * 30, 10))

    for i in range(player2.plane_health):
        screen.blit(player2_heart, (i * 30 + 580, 10))

    pygame.display.update()


def reinit_variables():
    global player1, player2, countdown_finished
    player1 = Plane(screen, playerx, playery)
    player1.plane_angle = 270
    player1.direction_angle = 4.71239
    player2 = Plane(screen, playerx_2, playery_2)
    player2.plane_angle = 90
    player2.direction_angle = 1.5708

    countdown_finished = False


#--------variables-----------#
playing = True
start_screen = True
instructions = False
inPlay = False
game_end = False
countdown_finished = False

player1 = Plane(screen, playerx, playery)
player1.plane_angle = 270
player1.direction_angle = 4.71239
player2 = Plane(screen, playerx_2, playery_2)
player2.plane_angle = 90
player2.direction_angle = 1.5708

# powerup = Airdrop(screen, width, height, )

bullet_speed = 20
bullet_shot1 = False
bullet_shot2 = False

bullet_cooldown = 0
player_cooldown = 0
start_bullet_cooldown = False
start_player_cooldown = True

#---------------main game---------------#
while playing:
    #intro screen
    while start_screen:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            intro_screen()
            start_button = pygame.Rect(300, 250, 300, 100)
            instructions_button = pygame.Rect(300, 370, 300, 100)
            (mousex, mousey) = pygame.mouse.get_pos()
            if start_button.collidepoint(
                    mousex, mousey) and event.type == pygame.MOUSEBUTTONDOWN:
                start_screen = False
                inPlay = True
            if instructions_button.collidepoint(
                    mousex, mousey) and event.type == pygame.MOUSEBUTTONDOWN:
                start_screen = False
                instructions = True
        #set FPS
        clock.tick(30)

    while instructions:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            instruction_screen()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                instructions = False
                start_screen = True
        clock.tick(30)

    #main game
    while inPlay:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        #turn plane left or right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player1.turn_left()
        if keys[pygame.K_d]:
            player1.turn_right()

        if keys[pygame.K_LEFT]:
            player2.turn_left()
        if keys[pygame.K_RIGHT]:
            player2.turn_right()

        #cooldown for shooting
        if start_bullet_cooldown:
            bullet_cooldown += clock.get_time()
            if bullet_cooldown > 300:
                bullet_cooldown = 0
                start_bullet_cooldown = False

        #shoot bullet
        if countdown_finished:
            if keys[pygame.K_w] and bullet_cooldown == 0:
                shoot_audio.play()
                bullet_shot1 = True
                player1.add_bullet()
                start_bullet_cooldown = True

            if keys[pygame.K_UP] and bullet_cooldown == 0:
                shoot_audio.play()
                bullet_shot2 = True
                player2.add_bullet()
                start_bullet_cooldown = True

        #move player
        if countdown_finished:
            player1.move_plane()
            player2.move_plane()

        #wall collisions with player
        player1.check_collide_walls(width, height)
        player2.check_collide_walls(width, height)

        if start_player_cooldown:
            player_cooldown += clock.get_time()
            if player_cooldown > 500:
                player_cooldown = 0
                start_player_cooldown = False

        #check if other player shoots at you
        player1.check_collision_bullet(player2.bullets, damage_audio)
        player2.check_collision_bullet(player1.bullets, damage_audio)

        #check if player collides with each other
        player1.check_collision_players(player2, player_cooldown, damage_audio)
        if player1.check_collision_players(player2, player_cooldown,
                                           damage_audio):
            start_player_cooldown = True

        redraw()
        countdown()

        if player1.plane_health <= 0 or player2.plane_health <= 0:
            inPlay = False
            game_end = True

        #set FPS
        clock.tick(30)

    while game_end:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            gameover()
            play_again = pygame.Rect(300, 370, 300, 100)
            (mousex, mousey) = pygame.mouse.get_pos()
            if play_again.collidepoint(
                    mousex, mousey) and event.type == pygame.MOUSEBUTTONDOWN:
                start_screen = True
                game_end = False
                reinit_variables()
        #set FPS
        clock.tick(30)
    clock.tick(30)

pygame.quit()