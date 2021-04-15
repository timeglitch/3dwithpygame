# Simple pygame program


# Import and initialize the pygame library

import pygame

import math

import time

import random

import camera
# Import pygame.locals for easier access to key coordinates

# Updated to conform to flake8 and black standards

from pygame.locals import (

    K_w,
    K_s,
    K_a,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,

)


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


#Classes
class Player:
    global walls
    def __init__(s):
        s.width = 50
        s.height = 50
        s.x = 100
        s.y = 100
        s.xvel = 0
        s.yvel = 0
        s.rotation = 0
        s.accel = 5
        s.rect = pygame.Rect(s.x-s.width/2, s.y-s.height, s.width, s.height)
        s.colDist = 10

    def update(s):

        #input and movement
        keys = pygame.key.get_pressed()
        s.rotation -= pygame.mouse.get_rel()[0] * s.accel/500
        if keys[pygame.K_a]:
            s.yvel-= s.accel * math.cos(s.rotation)
            s.xvel-= s.accel * math.sin(s.rotation) 
        if keys[pygame.K_d]:
            s.yvel+= s.accel * math.cos(s.rotation)
            s.xvel+= s.accel * math.sin(s.rotation) 
        if keys[pygame.K_w]:
            s.yvel-= s.accel * math.sin(s.rotation)
            s.xvel+= s.accel * math.cos(s.rotation) 
        if keys[pygame.K_s]:
            s.yvel+= s.accel * math.sin(s.rotation)
            s.xvel-= s.accel * math.cos(s.rotation)

        #calculate collisions
        for i in walls:
            if s.rect.colliderect(i.rect):
                
                if abs(s.rect.top - i.rect.bottom) < s.colDist:
                    s.yvel = s.yvel * -0.5 + 5
                if abs(s.rect.bottom - i.rect.top) < s.colDist:
                    s.yvel = s.yvel * -0.5 - 5
                if abs(s.rect.left - i.rect.right) < s.colDist:
                    s.xvel = s.xvel * -0.5 + 5
                if abs(s.rect.right - i.rect.left) < s.colDist:
                    s.xvel = s.xvel * -0.5 - 5

        #s.xvel = math.copysign(math.sqrt(abs(s.xvel)), s.xvel)
        #s.yvel = math.copysign(math.sqrt(abs(s.yvel)), s.yvel)
        s.x += s.xvel
        s.y += s.yvel
        s.xvel, s.yvel = 0, 0
        s.rect = pygame.Rect(s.x-s.width/2, s.y-s.height/2, s.width, s.height)
        #print("x" + str(s.x) + "y" + str(s.y) + "xvel" + str(s.xvel) + "yvel" + str(s.yvel))

        
        
        s.drawPlayer()

    def drawPlayer(s):
        #draw character
        pygame.draw.rect(screen, (0,0,255), s.rect)
        pygame.draw.circle(screen, (100, 100, 100), (s.x, s.y), s.width/2)
        pygame.draw.circle(screen, (255, 255, 255), (s.x, s.y), s.width/10)
        pygame.draw.arc(screen, (255, 0, 0), s.rect, s.rotation - 1, s.rotation + 1 )

class Wall:
    def __init__(s, rect, texture):
        s.rect = rect
        s.fourLines = ((s.rect.topleft, s.rect.topright), (s.rect.topright, s.rect.bottomright), (s.rect.bottomright, s.rect.bottomleft), (s.rect.bottomleft, s.rect.topleft))
        s.texture = texture
        
        #self.imgAr = pygame.PixelArray(pygame.image.load(texture))
    
    def drawWalls():
        global walls
        
        for i in walls:
            pygame.draw.rect(screen, i.texture ,i.rect)






# Initialize pygame
pygame.init()

# Set up the drawing window

screen = pygame.display.set_mode([1000, 1000])
pygame.display.set_caption("Vroom")
pixAr = pygame.PixelArray(screen)

#playerinit
player = Player()


#wallsinit
walls = []
walls.append(Wall(pygame.Rect(-50,0, 50, screen.get_height()), RED))
walls.append(Wall(pygame.Rect(screen.get_width(), 0, 50, screen.get_height()), RED))
walls.append(Wall(pygame.Rect(0,-50, screen.get_width(), 50), RED))
walls.append(Wall(pygame.Rect(0,screen.get_height(), screen.get_width(), 50), RED))
walls.append(Wall(pygame.Rect(200,200, 200, 300), BLUE))

#camerainit
camera = camera.Camera(screen, pixAr, walls)

# Event Loop
running = True

while running:
    
    #pygame.time.delay(10)

    #exit
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False
    

    #pixAr[10,10] = (255, 255, 255)
    screen.fill((255,255,255))
    
    player.update()
    Wall.drawWalls()
    camera.update(player.x, player.y, player.rotation)

    pygame.display.update()





# Done! Time to quit.

pygame.quit()


    
