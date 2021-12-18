import pygame
from pygame import *
import math
import sys

pygame.init()
pygame.font.init()
WINDOW_SIZE = screen_width, screen_height = 900, 600
display = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
clock = pygame.time.Clock()
alive = True
timer = 0
score_font = pygame.font.SysFont('Comic Sans MS', 30)

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.player_movement = [0, 0]
        self.speed = 3
        self.smoothing = .5
        self.x_vel = 0
        self.y_vel = 0
        self.color = (255, 255, 255)

    def colision(self):
        if self.rect.x < 0:
            self.x = 1
        if self.rect.right > screen_width:
            self.x = screen_width - self.width - 1
        if self.rect.y < 0:
            self.y = 1
        if self.rect.bottom > screen_height:
            self.y = screen_height - self.height -1

    def move_data(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.right = True
                if event.key == K_LEFT:
                    self.left = True
                if event.key == K_UP:
                    self.up = True
                if event.key == K_DOWN:
                    self.down = True
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.right = False
                if event.key == K_LEFT:
                    self.left = False
                if event.key == K_UP:
                    self.up = False
                if event.key == K_DOWN:
                    self.down = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    player_bullets.append(Player_Bullet(player.x, player.y, mouse_x, mouse_y))

        self.player_movement = [0, 0]
        self.player_movement[0] += self.x_vel
        self.player_movement[1] += self.y_vel
        if self.right:
            self.x_vel += self.smoothing
            if self.x_vel >= self.speed:
                self.x_vel = self.speed
        elif self.left:
            self.x_vel -= self.smoothing
            if self.x_vel <= -self.speed:
                self.x_vel = -self.speed
        else:
            if self.x_vel > 0:
                self.x_vel -= self.smoothing
            elif self.x_vel < 0:
                self.x_vel += self.smoothing

        if self.down:
            self.y_vel += self.smoothing
            if self.y_vel >= self.speed:
                self.y_vel = self.speed
        elif self.up:
            self.y_vel -= self.smoothing
            if self.y_vel <= -self.speed:
                self.y_vel = -self.speed
        else:
            if self.y_vel > 0:
                self.y_vel -= self.smoothing
            elif self.y_vel < 0:
                self.y_vel += self.smoothing

    def move(self):
        self.x += self.player_movement[0]
        self.y += self.player_movement[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self, display):
        pygame.draw.rect(display, player.color, self.rect, 0, 15)

class Player_Bullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x + player.width //2
        self.y = y + player.height //2
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.radius = 5
        self.speed = 5
        self.angle = math.atan2(y - mouse_y + self.radius, x - mouse_x + self.radius)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.active = False
        self.is_player_collide_beggining = False
        self.is_player_collide = False
        self.color = (100, 100, 100)

    def colision(self):
        #walls
        if self.x < 0:
            self.x_vel = -self.x_vel
            self.speed -= 3
        if self.x + 5 > screen_width:
            self.x_vel = -self.x_vel
            self.speed -= 3
        if self.y < 0:
            self.y_vel = -self.y_vel
            self.speed -= 3
        if self.y + 5 > screen_height:
            self.y_vel = -self.y_vel
            self.speed -= 3

        #player
        if self.x + self.radius > player.x and self.x < player.x + player.width and self.y + self.radius > player.y\
                and self.y < player.y + player.height:
            self.is_player_collide_beggining = True
        else:
            self.is_player_collide_beggining = False

        if not self.active:
            if not self.is_player_collide_beggining:
                self.active = True
        else:
            if self.is_player_collide_beggining:
                self.color = (255, 0, 0)
                display.fill((200, 200, 200))
                player_bullets.pop(0)
                self.is_player_collide = True
            else:
                self.color = (100, 100, 100)
                self.is_player_collide = False

    def draw(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        pygame.draw.circle(display, self.color, (self.x, self.y), 5)

    def main(self, display):
        self.colision()
        self.draw(display)


player = Player(100, 100, 50, 50)
player_bullets = []


play = True
while play:
    display.fill((0, 0, 0))
    score_screen = score_font.render('Score: ' + str(timer), False, (255, 255, 255))
    display.blit(score_screen, (10, 10))

    if alive:
        timer += 1
        player.move_data()
        player.colision()
        player.move()
        player.draw(display)

        for bullet in player_bullets:
            bullet.main(display)
            if bullet.is_player_collide:
                alive = False

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(60)
    pygame.display.update()