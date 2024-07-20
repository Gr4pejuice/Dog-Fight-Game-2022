import pygame
import math
from random import *
from math import sqrt

BLACK = (0, 0, 0)
GREY = (56, 56, 56)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)
CYAN = (0, 183, 235)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

def distance(x1, y1, x2, y2):
    return sqrt((x1-x2)**2 + (y1-y2)**2)

# class Game_UI():
#     def __init__(self, surface, width, height):
#         self.surface = surface
#         self.width = width
#         self.height = height

#     def draw_health(font, player1_hp):
#         text = font.render(str(player1_hp))
#         self.surface.blit(text, (10,10))
        

class Plane():

    def __init__(self, surface, plane_x, plane_y):
        self.surface = surface
        self.plane_x = plane_x
        self.plane_y = plane_y
        self.direction_angle = math.pi
        self.plane_angle = 0
        self.plane_speed = 7
        self.plane_health = 10

        self.bullet_speed = 15
        self.bullet_visible = False
        self.bullets = []

    def rotate_plane(self, plane_image):
        self.plane_copy = pygame.transform.rotate(plane_image,
                                                  self.plane_angle)

    def draw_plane(self):
        self.surface.blit(self.plane_copy,
                          ((self.plane_x - self.plane_copy.get_width() / 2),
                           (self.plane_y - self.plane_copy.get_height() / 2)))

    def draw_direction(self, length):
        pygame.draw.line(
            self.surface, GREEN, (self.plane_x, self.plane_y),
            (self.plane_x - math.sin(self.direction_angle) * length,
             self.plane_y + math.cos(self.direction_angle) * length), 3)

    def turn_left(self):
        self.direction_angle -= 0.1
        self.plane_angle += 5.73

    def turn_right(self):
        self.direction_angle += 0.1
        self.plane_angle -= 5.73

    def move_plane(self):
        self.plane_x += -math.sin(self.direction_angle) * self.plane_speed
        self.plane_y += math.cos(self.direction_angle) * self.plane_speed

    def check_collide_walls(self, screen_width, screen_height):
        #wall collisions with player
        if self.plane_x < 0:
            self.plane_x = screen_width

        if self.plane_x > screen_width:
            self.plane_x = 0

        if self.plane_y < 0:
            self.plane_y = screen_height

        if self.plane_y > screen_height:
            self.plane_y = 0

    def add_bullet(self):
        bullet_x = self.plane_x
        bullet_y = self.plane_y
        bullet_angle = self.direction_angle
        bullet_visible = True

        bullet = Bullet(bullet_x, bullet_y, bullet_angle, bullet_visible)
        self.bullets.append(bullet)

    def shoot_bullet(self, width, height):
        for i in self.bullets:
            if i.bullet_visible == True:
                i.draw_bullet(self.surface)
                i.bullet_x += -math.sin(i.bullet_angle) * self.bullet_speed
                i.bullet_y += math.cos(i.bullet_angle) * self.bullet_speed

                if i.bullet_x < -10 or i.bullet_x > width + 10 or i.bullet_y < -10 or i.bullet_y > height + 10:
                    index = self.bullets.index(i)
                    self.bullets.pop(index)

    def check_collision_bullet(self, other, sound):    
        for bullet in other:
            if distance(self.plane_x + math.sin(self.direction_angle) * 25, self.plane_y - math.cos(self.direction_angle) * 25, bullet.bullet_x, bullet.bullet_y) < 25:
                index = other.index(bullet)
                other.pop(index)
                self.plane_health -= 1
                sound.play()

    def check_collision_players(self, other, cooldown, sound):
        if distance(self.plane_x + math.sin(self.direction_angle) * 25, self.plane_y - math.cos(self.direction_angle) * 25, other.plane_x + math.sin(other.direction_angle) * 25, other.plane_y - math.cos(other.direction_angle) * 25) < 50 and cooldown == 0:
            self.plane_health -= 1
            other.plane_health -= 1
            sound.play()
            return True

    def check_collision_powerup(self, other):
        pass

      
class Bullet():

    def __init__(self, bullet_x, bullet_y, bullet_angle, bullet_visible):
        self.bullet_x = bullet_x
        self.bullet_y = bullet_y
        self.bullet_angle = bullet_angle
        self.bullet_visible = bullet_visible

    def draw_bullet(self, screen):
        pygame.draw.circle(screen, BLACK, (self.bullet_x, self.bullet_y), 5)

class Airdrop():
    def __init__(self, surface, width, height, airdrop_x, airdrop_y, airdrop_speed, image):
        self.surface = surface
        self.width = width
        self.height = height
        self.image = image
        self.airdrop_x = airdrop_x
        self.airdrop_y = airdrop_y
        self.airdrop_speed = airdrop_speed

        self.powerup_visible = True
        self.powerup_cooldown = False

        self.number = randint(1,3)

    def draw_airdrop(self):
        if powerup_visible:
            self.powerup_hitbox = pygame.Rect(airdrop_x + 15, airdrop_y + 70, 50, 40)
            self.surface.blit(self.image, self.airdrop_x, self.airdrop_y)
            self.airdrop_y += self.airdrop_speed

    def powerup_function(self, player):
        if self.number == 1:
            player.plane_health += 1
        if self.number == 2:
            player.plane_speed = 10
        

    def cooldown(self):
        if powerup_cooldown:
            cooldown_tracker += clock.get_time() 
            if cooldown_tracker > 5000:
                cooldown_tracker = 0
                start_player_cooldown = False