#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#ENVIRONMENT SETUP AND IMPORTS
import pygame
pygame.init()
pygame.display.set_caption("scoring")
SCREEN_DIMENSIONS=[500,480]
screen=pygame.display.set_mode(SCREEN_DIMENSIONS)
score=0
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
    RLEACCEL,
)
import winsound
clock=pygame.time.Clock()
from math import pow
ADD_ENEMY=pygame.USEREVENT+1
minute=60000
import random
pygame.time.set_timer(ADD_ENEMY,random.randint(minute/12,minute/10))#anytime between 12-15 seconds
#PATH TO GAME ASSETS(SPRITES,MUSIC,DATABASE,LOGS,...)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os
from os.path import join
os.chdir(os.getcwd())
def get_root(iterations):
    root=__file__
    for i in range(iterations):
        root=os.path.dirname(root)
    return root

ROOT=get_root(3)
game_assets=join(ROOT,"assets","Game")
font=pygame.font.SysFont('comicsans',30,True,True)
music1=pygame.mixer.music.load(join(game_assets,'music.mp3'))
punch=pygame.mixer.Sound(join(game_assets,"punch.wav"))
explosion=pygame.mixer.Sound(join(game_assets,"boom.wav"))
#pygame.font.SysFont(FontName,FontSize,Bold,Italicised)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#CHARACTERS(ENEMIES,PLAYERS,PROJECTILES)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Character(pygame.sprite.Sprite):
    __hp=15
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
        self.blinking=False
        self.blinkCount=0
        self.damaged=False
        self.healthIndicator=pygame.Surface(
            [
                (self.rect.right-self.rect.left)*0.75,10
            ]
            )
        self.healthBar=self.healthIndicator.get_rect()
        self.healthBar.left=self.rect.left
        self.healthBar.bottom=self.rect.top
        self.fullHp=self.__hp

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
        self.healthBar.move_ip(*self.velocity)
        if self.rect.left<0:
            self.rect.left=0
        elif self.rect.right>SCREEN_DIMENSIONS[0]:
            self.rect.right=SCREEN_DIMENSIONS[0]
        elif self.rect.bottom>SCREEN_DIMENSIONS[1]:
            self.rect.bottom=SCREEN_DIMENSIONS[1]
        elif self.rect.top<0:
            self.rect.top=0
        self.healthBar.left=self.rect.left
        self.healthBar.bottom=self.rect.top

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

    def displayBoundaries(self,color):
        pygame.draw.rect(screen,colors.get(color),self.rect,1)

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self,val):
        self.__hp=val
        if self.__hp==0:
            self.kill()
        
    def blink(self):
        if self.blinking:
            if self.blinkCount%2==0:
                self.displayBoundaries("red")
            else:
                self.displayBoundaries("white")
            self.blinkCount+=1

    def displayHP(self):
        pygame.draw.rect(screen,colors.get("black"),self.healthBar,1)
    
    def displayDamage(self,color="red"):
        fraction=0.75*(self.hp/self.fullHp)
        width=fraction*(self.rect.right-self.rect.left)
        container=pygame.Surface([width,10])
        containerRect=container.get_rect()
        containerRect.left=self.healthBar.left
        containerRect.bottom=self.healthBar.bottom
        pygame.draw.rect(screen,colors.get(color),containerRect)

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
        self.hp=15
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
        self.healthBar.right=self.rect.right
        self.healthBar.bottom=self.rect.top
        self.fullHp=self.hp
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
pygame.mixer.music.play()
while running:
    text=font.render('Score: {}'.format(score),1,colors.get('black'))
    #font.render(text,antialias,color)
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
    screen.blit(text,[330,10])
    keyboard_commands=pygame.key.get_pressed()
    for player in Players:
        player.update_coordinates(keyboard_commands)
        player.jump()
        player.move()
        player.displayHP()
        color="blue" if player.hp>=(player.fullHp//2) else "red"
        player.displayDamage(color=color)
        screen.blit(player.surface,player.rect)
        #player.displayBoundaries("black")
        if pygame.sprite.spritecollideany(player,ENEMIES):
            if not player.damaged:
                player.hp-=1
                punch.play()
            player.displayBoundaries("red")
            player.blinking=True
            player.damaged=True
            if len(Players)==0:
                running=False
        else:
            player.blinking=False
            player.damaged=False
        player.blink()

        for projectile in player.projectiles:
            projectile.move()
            screen.blit(projectile.surface,projectile.rect)
            if pygame.sprite.spritecollideany(projectile,ENEMIES):
                setattr(projectile,"terminate",True)

    for enemy in ENEMIES:
        enemy.move()
        screen.blit(enemy.surface,enemy.rect)
        enemy.displayHP()
        enemy.displayDamage()
        #enemy.displayBoundaries("black")
        if pygame.sprite.spritecollideany(enemy,Projectiles):
            enemy.hp-=1
            explosion.play()
            if enemy.hp==0:
                score+=5
            enemy.displayBoundaries("white")
            for projectile in Projectiles:
                if hasattr(projectile,"terminate"):
                    projectile.kill()

    pygame.display.flip()
    clock.tick(27)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pygame.quit()
