#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
######################################### imports and pygame setup ##########################################
import pygame
pygame.init()
SCREEN_DIMENSIONS=[500,480]
screen=pygame.display.set_mode(SCREEN_DIMENSIONS)

colors=dict(
    black=[0,0,0],
    white=[255,255,255],
    red=[255,0,0],
    blue=[0,0,255],
    green=[0,255,0]
)

from pygame.locals import(
    KEYDOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)

import os
from os.path import join
#PATH TO ASSETS
def get_root(hierachy_index):
    root=__file__
    for i in range(hierachy_index):
        root=os.path.dirname(root)
    return root

root=get_root(3)
game_assets=join(root,"assets","Game")
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from math import pow
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super(Character,self).__init__()
        self.speed=5
        self.isJumping=False
        self.jumpCount=10
        self.left=False
        self.right=False
        self.walkCount=0
        self.standing=pygame.image.load(join(game_assets,"standing.png"))
        self.surface=self.standing
        self.rect=self.surface.get_rect()
        self.rect.left=0
        self.rect.bottom=SCREEN_DIMENSIONS[1]
        self.walkRight=[pygame.image.load(join(game_assets,f"R{i}.png")) for  i in range(1,10)]
        self.walkLeft=[pygame.image.load(join(game_assets,f"L{i}.png")) for i in range(1,10)]

    def update_coordinates(self,keyboard):
        self.velocity=[0,0]
        if keyboard[K_LEFT]:
            self.velocity[0]=-self.speed
            self.left=True
            self.right=False
        elif keyboard[K_RIGHT]:
            self.velocity[0]=self.speed
            self.right=True
            self.left=False
        elif keyboard[K_SPACE]:
            self.isJumping=True
        else:
            self.left=self.right=False

    def move(self):
        self.rect.move_ip(*self.velocity)
        if self.left:
            if self.walkCount<len(self.walkLeft):
                self.surface=self.walkLeft[self.walkCount]
                self.walkCount+=1
            else:
                self.walkCount=0
                self.surface=self.walkLeft[self.walkCount]
        elif self.right:
            if self.walkCount<len(self.walkRight):
                self.surface=self.walkRight[self.walkCount]
                self.walkCount+=1
            else:
                self.walkCount=0
                self.surface=self.walkRight[self.walkCount]
        else:
            self.surface=self.standing

        right=SCREEN_DIMENSIONS[0]
        if self.rect.left<0:
            self.rect.left=0

        elif self.rect.right>right:
            self.rect.right=right

    def jump(self):
        if self.isJumping:
            if self.jumpCount>=-10:
                speed=pow(self.jumpCount,2)
                if self.jumpCount>=0:
                    self.velocity[1]=-speed
                else:
                    self.velocity[1]=speed
                self.jumpCount-=1
            else:
                #when playerf is back on the ground, they are no longer jumping
                self.isJumping=False
                #when they are back on the ground they are allowed to jump to maximum height again
                #even pressing space does not make the character jump again in mid-air cause pressing space only 
                #toggles the boolean isJumping from False to True
                self.jumpCount=10

player1=Character()
running=True
clock=pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==KEYDOWN:
            if event.key==K_ESCAPE:
                running=False
    background=pygame.image.load(join(game_assets,"bg.jpg"))
    screen.blit(background,(0,0))
    keyboard_commands=pygame.key.get_pressed()
    player1.update_coordinates(keyboard_commands)
    player1.jump()
    player1.move()
    screen.blit(player1.surface,player1.rect)
    pygame.display.flip()
    clock.tick(27)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pygame.quit()