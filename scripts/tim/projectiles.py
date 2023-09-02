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
    K_TAB,
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

class Projectile():
    def __init__(self,container,direction):
        mid=container.bottom-(container.top+container.bottom)/2
        self.speed=8*direction
        self.color=colors.get("black")
        self.radius=5
        if direction>0:
            self.coordinates=container.right,mid
        else:
            self.coordinates=container.left,mid

    def draw(self,container):
        pygame.draw.circle(container,self.color,self.coordinates,self.radius)

    def move(self,container):
        self.coordinates[0]+=self.speed
        self.draw(container)

class Character():
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
        self.projectiles=[]


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
        elif keyboard[K_TAB]:
            print("pressed tab...")
            if self.left:
                self.projectiles.add(Projectile(self.rect,-1))
            elif self.right:
                self.projectiles.add(Projectile(self.rect,1))
        else:
            if self.left:
                if self.walkCount<len(self.walkLeft):
                    self.surface=self.walkLeft[self.walkCount]
                else:
                    self.surface=self.walkLeft[self.walkCount-1]
            elif self.right:
                if self.walkCount<len(self.walkRight):
                    self.surface=self.walkRight[self.walkCount]
                else:
                    self.surface=self.walkRight[self.walkCount-1]
        
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
    for projectile in player1.projectiles:
        projectile.move(screen)
    pygame.display.flip()
    clock.tick(27)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pygame.quit()