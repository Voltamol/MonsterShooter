#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#ENVIRONMENT SETUP AND IMPORTS
import pygame
pygame.init()
pygame.display.set_caption("enemies2")
SCREEN_DIMENSIONS=[500,480]
screen=pygame.display.set_mode(SCREEN_DIMENSIONS)
colors=dict(
    red=(255,0,0),
    green=(0,255,0),
    blue=(0,0,255),
    white=(255,255,255),
    black=(0,0,0)
)
directions=dict(left=-1,right=1)
from pygame.locals import(
    KEYDOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_TAB,
)

clock=pygame.time.Clock()
from math import pow
ADD_ENEMY=pygame.USEREVENT+1
minute=60000
import random
pygame.time.set_timer(ADD_ENEMY,random.randint(minute/5,minute/4))#anytime between 12-15 seconds
#PATH TO GAME ASSETS(SPRITES,MUSIC,DATABASE,LOGS,...)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os
from os.path import join
def get_root(iterations):
    root=__file__
    for i in range(iterations):
        root=os.path.dirname(root)
    return root

ROOT=get_root(3)
game_assets=join(ROOT,"assets","Game")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#CHARACTERS(ENEMIES,PLAYERS,PROJECTILES)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super(Character,self).__init__()
        self.speed=5
        self.facing="right"#faces right by default
        self.velocity=[0,0]
        self.dimensions=[35,70]
        self.x=self.dimensions[0]/2
        self.y=SCREEN_DIMENSIONS[1]-self.dimensions[1]/2
        self.isJumping=False
        self.jumpCount=10
        self.coordinates=self.x,self.y
        self.walkLeft=[join(game_assets,f"L{i}.png") for i in range(1,10)]
        self.walkRight=[join(game_assets,f"R{i}.png") for i in range(1,10)]
        self.walkLeft=[pygame.image.load(filepath) for filepath in self.walkLeft]
        self.walkRight=[pygame.image.load(filepath) for filepath in self.walkRight]
        self.walkCount=0
        #self.surface=pygame.Surface(self.dimensions)
        self.surface=self.walkRight[-1]
        self.standing=dict(left=self.walkLeft[-1],right=self.walkRight[-1])
        #self.surface.fill(colors.get("white"))
        #self.rect=self.surface.get_rect(center=self.coordinates)
        self.rect=self.surface.get_rect()
        self.rect.left=0
        self.rect.bottom=SCREEN_DIMENSIONS[1]
        self.projectiles=pygame.sprite.Group()
        self.bulletRounds=5

    def update_coordinates(self,keyboard):
        if keyboard[K_LEFT]:
            self.walkCount+=1
            if self.walkCount==len(self.walkLeft):
                self.walkCount=0
            self.surface=self.walkLeft[self.walkCount]
            self.facing="left"

        elif keyboard[K_RIGHT]:
            self.walkCount+=1
            if self.walkCount==len(self.walkRight):
                self.walkCount=0
            self.surface=self.walkRight[self.walkCount]
            self.facing="right"

        elif keyboard[K_SPACE]:
            self.isJumping=True
            return
        elif keyboard[K_TAB]:
            self.shoot()
            return
        else:
            self.velocity=[0,0]
            self.surface=self.standing.get(self.facing)
            return

        self.velocity[0]=self.speed*directions.get(self.facing)

    def move(self):
        self.rect.move_ip(*self.velocity)
        if self.rect.left<0:
            self.rect.left=0
        elif self.rect.right>SCREEN_DIMENSIONS[0]:
            self.rect.right=SCREEN_DIMENSIONS[0]
        elif self.rect.bottom>SCREEN_DIMENSIONS[1]:
            self.rect.bottom=SCREEN_DIMENSIONS[1]
        elif self.rect.top<0:
            self.rect.top=0

    def jump(self):
        if self.isJumping:
            if self.jumpCount>=-10:
                jumpSize=pow(self.jumpCount,2)
                jumpSize*=-1 if self.jumpCount>=0 else 1
                self.jumpCount-=1
                self.velocity[1]=jumpSize
            else:
                self.isJumping=False
                self.jumpCount=10

    def shoot(self):
        if not pygame.sprite.spritecollideany(self,self.projectiles):
            if len(self.projectiles)<=self.bulletRounds:
                projectile=Projectile(self)
                self.projectiles.add(projectile)
                Projectiles.add(projectile)

    def displayBoundaries(self):
        pygame.draw.rect(screen,colors.get("black"),self.rect,1)

class Projectile(pygame.sprite.Sprite):
    def __init__(self,parentSprite):
        super(Projectile,self).__init__()
        self.dimensions=[10,5]
        self.speed=12
        self.surface=pygame.Surface(self.dimensions)
        self.surface.fill(colors.get("red"))
        self.y=(parentSprite.rect.top+parentSprite.rect.bottom)/2
        self.x=getattr(parentSprite.rect,parentSprite.facing)
        self.velocity=[self.speed*directions.get(parentSprite.facing),0]
        self.rect=self.surface.get_rect(center=[self.x,self.y])

    def move(self):
        self.rect.move_ip(*self.velocity)
        if self.rect.right<0:
            self.kill()
        elif self.rect.left>SCREEN_DIMENSIONS[0]:
            self.kill()


class Enemy(Character):
    #an enemy is also a character hence the inheritance
    def __init__(self):
        super(Enemy,self).__init__()
        self.speed=3
        self.facing="left"
        self.walkLeft=[join(game_assets,f"L{i}E.png") for i in range(1,12)]
        self.walkRight=[join(game_assets,f"R{i}E.png") for i in range(1,12)]
        self.walkLeft=[pygame.image.load(filepath) for filepath in self.walkLeft]
        self.walkRight=[pygame.image.load(filepath) for filepath in self.walkRight]
        self.surface=self.walkLeft[-1]
        self.rect.right=SCREEN_DIMENSIONS[0]
        self.velocity=[directions.get(self.facing)*self.speed,0]
        self.directions=dict(left=self.walkLeft,right=self.walkRight)
        self.direction=self.directions.get(self.facing)

    def move(self):
        super(Enemy,self).move()
        if self.walkCount+1<len(self.direction):
            self.walkCount+=1
        else:
            self.walkCount=0
        self.surface=self.direction[self.walkCount]
        if self.rect.left==0:#now using == since super.move sets this to 0
            self.velocity[0]*=-1
            self.walkCount=0
            self.surface=self.walkRight[self.walkCount]
            self.facing="right"
            self.direction=self.directions.get(self.facing)
        elif self.rect.right==SCREEN_DIMENSIONS[0]:
            self.velocity[0]*=-1
            self.walkCount=0
            self.surface=self.walkLeft[self.walkCount]
            self.facing="left"
            self.direction=self.directions.get(self.facing)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#INSTANTIATIONS
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
player1=Character()
ENEMIES=pygame.sprite.Group()
Players=pygame.sprite.Group()
Projectiles=pygame.sprite.Group()
Players.add(player1)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#GAME MAINLOOP
running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type==KEYDOWN:
            if event.key==K_ESCAPE:
                running=False
        elif event.type==ADD_ENEMY:
            enemy=Enemy()
            ENEMIES.add(enemy)

    screen.blit(pygame.image.load(join(game_assets,"bg.jpg")),[0,0])
    keyboard_commands=pygame.key.get_pressed()
    for player in Players:
        player.update_coordinates(keyboard_commands)
        player.jump()
        player.move()
        screen.blit(player.surface,player.rect)
        player.displayBoundaries()
        if pygame.sprite.spritecollideany(player,ENEMIES):
            player.kill()
    
        for projectile in player.projectiles:
            projectile.move()
            screen.blit(projectile.surface,projectile.rect)
            if pygame.sprite.spritecollideany(projectile,ENEMIES):
                setattr(projectile,"terminate",True)

    for enemy in ENEMIES:
        enemy.move()
        screen.blit(enemy.surface,enemy.rect)
        enemy.displayBoundaries()
        if pygame.sprite.spritecollideany(enemy,Projectiles):
            enemy.kill()
            for projectile in Projectiles:
                if hasattr(projectile,"terminate"):
                    projectile.kill()

    pygame.display.flip()
    clock.tick(27)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pygame.quit()