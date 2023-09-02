#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++ IMPORTS AND INITIALISATIONS ++++++++++++++++++++++++++++++++++++++++
import pygame
pygame.init()

# KEYBOARD STUFF...
from pygame.locals import(
    KEYDOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_RETURN,
    K_TAB,
    RLEACCEL,
    K_x,
)
# SCREEN STUFF...
SCREEN_DIMENSIONS=[800,480]
minute=60000
screen=pygame.display.set_mode(SCREEN_DIMENSIONS)

# COLORS...
colors=dict(
    red=[255,0,0],
    green=[0,255,0],
    blue=[0,0,255],
    white=[255,255,255],
    black=[0,0,0],
    gray=[100,100,100],
    yellow=[255,255,0]
)

# MATH STUFF...
from math import pow
from random import randint
# PATH STUFF...
import os
from os.path import join

def get_root(iterations):
    root=__file__
    for _ in range(iterations):
        root=os.path.dirname(root)
    if not os.path.isdir(root):
        root= os.path.dirname(root)
    return root

ROOT=get_root(3)
game_assets=join(ROOT,"assets","Game")

# DIRECTION HANDLING...
directions=dict(
    left=-1,
    right=1
)
direction=dict(
    left=lambda character:next(character.WLA),
    right=lambda character:next(character.WRA))

reset_direction=dict(
    left=("WLA",lambda character:iter(character.walkLeft)),
    right=("WRA",lambda character:iter(character.walkRight))
)

angle=dict(
    left=180,
    right=0,
)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++ SOUND EFFECTS ++++++++++++++++++++++++++++++++++++++++++++++++++++++
explosion=pygame.mixer.Sound(join(game_assets,"boom.wav"))
punch=pygame.mixer.Sound(join(game_assets,"punch.wav"))
music=pygame.mixer.music.load(join(game_assets,"music.mp3"))
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++ Attribute classes +++++++++++++++++++++++++++++++++++++++++++++++++
class HP:
    __hp=15

    def __get__(self,caller,objecttype):
        return self.__hp

    def __set__(self,caller,value):
        self.__hp=value
        if self.__hp==0:
            caller.kill()


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++ GAME CHARACTERS ++++++++++++++++++++++++++++++++++++++++++++++++++++
class Character(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Character,self).__init__()
        self.hp=HP()
        self.speed=5
        self.velocity=[0,0]
        #self.dimensions=[35,70]
        self.isJumping=False
        self.jumpCount=10
        #self.x=self.dimensions[0]/2
        #self.y=SCREEN_DIMENSIONS[1]-self.dimensions[1]/2
        #self.surface=pygame.Surface(self.dimensions)
        #self.surface.fill(colors.get("white"))
        self.standing=pygame.image.load(join(game_assets,"standing.png"))
        self.surface=self.standing
        self.rect=self.surface.get_rect()
        self.rect.left=0
        self.rect.bottom=SCREEN_DIMENSIONS[1]
        self.Left=[join(game_assets,f"L{i}.png") for i in range(1,10)]
        self.Right=[join(game_assets,f"R{i}.png") for i in range(1,10)]
        self.walkLeft=[pygame.image.load(image) for image in self.Left]
        self.walkRight=[pygame.image.load(image) for image in self.Right]
        self.WLA=iter(self.walkLeft)#walkLeftAnimations
        self.WRA=iter(self.walkRight)#walkRightAnimations
        self.facing="right"
        self.rounds=10
        self.moving=False
        self.damage=1
        self.fullHP=15
        self.takingDamage=False
        self.currentVelocity=self.velocity

    def update_coordinates(self,keyboard):
        if keyboard[K_LEFT]:
            self.velocity[0]=-self.speed
            self.facing="left"
            self.moving=True
        elif keyboard[K_RIGHT]:
            self.velocity[0]=self.speed
            self.facing="right"
            self.moving=True
        elif keyboard[K_SPACE]:
            self.isJumping=True
            self.moving=True
        elif keyboard[K_TAB]:
            projectile=Projectile(self)
            if len(Projectiles)<self.rounds:
                if not pygame.sprite.spritecollideany(projectile,Projectiles):
                    Projectiles.add(projectile)
        else:
            self.moving=False
            if keyboard[K_RETURN]:
                self.surface=self.standing
            self.velocity=[0,0]
    #will decorate you someday
    def move(self):
        if pause:
            return
        
        self.rect.move_ip(*self.velocity)
        if self.rect.left<0:
            self.rect.left=0
        elif self.rect.right>SCREEN_DIMENSIONS[0]:
            self.rect.right=SCREEN_DIMENSIONS[0]
        elif self.rect.bottom>SCREEN_DIMENSIONS[1]:
            self.rect.bottom=SCREEN_DIMENSIONS[1]
        sprite=None
        if self.moving:
            try:
                sprite=direction.get(self.facing)(self)
            except StopIteration:
                attribute,new_iterator=reset_direction.get(self.facing)
                setattr(self,attribute,new_iterator(self))
            finally:
                if sprite is None:
                    sprite=direction.get(self.facing)(self)
                self.surface=sprite

    def jump(self):
        if pause:
            return
        if self.isJumping:
            if self.jumpCount>=-10:
                jumpHeight=pow(self.jumpCount,2)
                if self.jumpCount>=0:
                    self.velocity[1]=-jumpHeight
                else:
                    self.velocity[1]=jumpHeight
                self.jumpCount-=1
            else:
                self.isJumping=False
                self.jumpCount=10

    def take_damage(self):
        self.hp-=self.damage
        punch.play()
        if self.hp==0:
            self.kill()
            explosion.play()

    def indicateHP(self,color="blue"):
        y=self.rect.top
        x=self.rect.left
        width=0.75*(self.rect.right-self.rect.left)
        height=10
        indicator=pygame.Surface([width,height])
        indicatorRect=indicator.get_rect()
        indicatorRect.left=x+width/4
        indicatorRect.bottom=y
        pygame.draw.rect(screen,colors.get("black"),indicatorRect,1)
        innerWidth=(width-2)*(self.hp/self.fullHP)
        innerSurface=pygame.Surface([innerWidth,height-2])
        innerRect=innerSurface.get_rect()
        innerRect.left=indicatorRect.left+1
        innerRect.bottom=indicatorRect.bottom-1
        if self.hp>=self.fullHP/2:
            pygame.draw.rect(screen,colors.get(color),innerRect)
        else:
            pygame.draw.rect(screen,colors.get("red"),innerRect)


class Enemy(Character):
    def __init__(self):
        super(Enemy,self).__init__()
        self.speed=3
        self.velocity=[-self.speed,0]
        self.Left=[join(game_assets,f"L{i}E.png") for i in range(1,12)]
        self.Right=[join(game_assets,f"R{i}E.png") for i in range(1,12)]
        self.walkLeft=[pygame.image.load(image) for image in self.Left]
        self.walkRight=[pygame.image.load(image) for image in self.Right]
        self.WLA=iter(self.walkLeft)#walkLeftAnimations
        self.WRA=iter(self.walkRight)#walkRightAnimations
        self.facing="left"
        self.moving=True
        self.rect.right=SCREEN_DIMENSIONS[0]
        self.rect.bottom=SCREEN_DIMENSIONS[1]
       
    def move(self):
        super(Enemy,self).move()
        if self.rect.left==0:
            self.velocity[0]*=-1
            self.facing="right"
        elif self.rect.right==SCREEN_DIMENSIONS[0]:
            self.velocity[0]*=-1
            self.facing="left"

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++ CHARACTER INTERACTIONS+++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++ GAME NOTIFICATIONS +++++++++++++++++++++++++++++++++++++++++++++++++++++
class Notifier:
    __score=0
    def __init__(self):
        self.scoreSurface=font.render("Score:{}".format(self.score),1,colors.get("black"))
        self.scoreRect=self.scoreSurface.get_rect()
        self.scoreRect.top=self.scoreRect.left=10
    @property
    def score(self):
        _score=self.__score
        return _score

    @score.setter
    def score(self,value):
        self.__score=value
        self.scoreSurface=font.render("Score:{}".format(self.__score),1,colors.get("black"))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Projectile(pygame.sprite.Sprite):
    def __init__(self,shooter):
        super(Projectile,self).__init__()
        self.speed=8
        self.velocity=[self.speed,0]
        shooterRect=shooter.rect
        self.y=shooterRect.bottom-(shooterRect.bottom-shooterRect.top)/2
        self.x=getattr(shooterRect,shooter.facing)
        #surface=pygame.Surface([20,10])
        #self.surface.fill(colors["red"])
        assets=os.path.dirname(game_assets)
        general=os.path.join(assets,"General")
        self.surface=pygame.image.load(join(general,"missile.jpg")).convert()
        self.surface=pygame.transform.scale(self.surface,[30,15])
        self.surface.set_colorkey(colors.get("white"),RLEACCEL)
        self.rect=self.surface.get_rect(center=[self.x,self.y])
        self.velocity[0]*=directions.get(shooter.facing)
        self.surface=pygame.transform.rotate(self.surface,angle.get(shooter.facing))

    def move(self):
        if pause:
            return
        self.rect.move_ip(*self.velocity)
        if (self.rect.left>SCREEN_DIMENSIONS[0]) or (self.rect.right<0):
            self.kill()
        

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++ INSTANTIATIONS ++++++++++++++++++++++++++++++++++++++++++++++++++++
# SPRITES
player=Character()
# SPRITE GROUPS
Players=pygame.sprite.Group()
Projectiles=pygame.sprite.Group()
Enemies=pygame.sprite.Group()
ADD_ENEMY=pygame.USEREVENT+1
ALL_CHARACTERS=pygame.sprite.Group()
pygame.time.set_timer(ADD_ENEMY,randint(minute/5,minute/4))
Players.add(player)
ALL_CHARACTERS.add(player)
pygame.mixer.music.play(-1)
# FRAME HANDLING...
clock=pygame.time.Clock()
# GAME FONT...
font=pygame.font.SysFont("comicsans",30,1,1)
# NOTIFIER
notifier=Notifier()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++ GAME MAINLOOP +++++++++++++++++++++++++++++++++++++++++++++++++++++
running=True
pause=False
cwd=os.path.dirname(__file__)
with open(join(cwd,"player_scores.txt"),"r") as scores:
    highScore=scores.read().split(":").pop()
highScore=int(highScore)

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==KEYDOWN:
            if event.key==K_ESCAPE:
                running=False
            elif event.key==K_x:
                pause=not pause
                if pause:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
        elif event.type==ADD_ENEMY:
            enemy=Enemy()
            Enemies.add(enemy)
            ALL_CHARACTERS.add(enemy)
    #screen.fill(colors["black"])
    screen.blit(pygame.image.load(join(game_assets,"bg.jpg")),[0,0])
    keyboard_commands=pygame.key.get_pressed()
    for player in Players:
        player.update_coordinates(keyboard_commands)
        player.jump()
        player.move()
        if pygame.sprite.spritecollideany(player,Enemies):
            if not player.takingDamage:
                player.take_damage()
                player.takingDamage=True
        else:
            player.takingDamage=False
        screen.blit(player.surface,player.rect)
    for projectile in Projectiles:
        projectile.move()
        screen.blit(projectile.surface,projectile.rect)
        if pygame.sprite.spritecollideany(projectile,Enemies):
            setattr(projectile,"terminate",True)
    for enemy in Enemies:
        enemy.move()
        screen.blit(enemy.surface,enemy.rect)
        if pygame.sprite.spritecollideany(enemy,Projectiles):
            enemy.take_damage()
            if enemy.hp==0:
                notifier.score+=5
                if notifier.score>highScore:
                    highScore=notifier.score
                    print("new high  reached...")
            for projectile in Projectiles:
                if hasattr(projectile,"terminate"):
                    projectile.kill()
    for character in ALL_CHARACTERS:
        if isinstance(character,Enemy):
            character.indicateHP(color="yellow")
        else:
            character.indicateHP()

    screen.blit(notifier.scoreSurface,notifier.scoreRect)
        
    pygame.display.flip()
    clock.tick(27)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

pygame.quit()
with open(join(cwd,"player_scores.txt"),"w") as scoresheet:
    scoresheet.write(f"score:{highScore}")