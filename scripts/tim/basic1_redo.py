import pygame
pygame.init()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
SCREEN_WIDTH,SCREEN_HEIGHT=[500,500]
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
from pygame.locals import(
    KEYDOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)

colors=dict(
    red=[255,0,0],
    blue=[0,0,255],
    black=[0,0,0],
    white=[255,255,255]
    )

from math import pow
class Character(pygame.sprite.Sprite):
    def __init__(self):
        """this is probably an abstract base class which enforces implementation of its __init__ method"""
        super(Character,self).__init__()
        self.speed=4
        self.velocity=[0,0]
        self.is_jumping=False
        self.dimensions=[50,100]
        self.x=self.dimensions[0]/2
        self.y=SCREEN_HEIGHT-(self.dimensions[1]/2)
        self.coordinates=self.x,self.y
        self.surface=pygame.Surface(self.dimensions)
        self.surface.fill(colors["white"])
        self.rect=self.surface.get_rect(center=self.coordinates)

    def update_coordinates(self,keyboard):
        self.velocity=[0,0]
        if keyboard[K_LEFT]:
            self.velocity[0]=-self.speed
        elif keyboard[K_RIGHT]:
            self.velocity[0]=self.speed
        elif keyboard[K_SPACE]:
            self.is_jumping=True
            self.jumpCount=10

    def move(self):
        self.rect.move_ip(*self.velocity)
        if self.rect.left<0:
            self.rect.left=0
        elif self.rect.right>SCREEN_WIDTH:
            self.rect.right=SCREEN_WIDTH

    def jump(self):
        if self.is_jumping:
            if self.jumpCount>=0:
                self.velocity[1]=-pow(self.jumpCount,2)#making the jump quadratic
            else:
                if self.jumpCount>-11:
                    self.velocity[1]=pow(self.jumpCount,2)
                else:
                    self.is_jumping=False
            self.jumpCount-=1


character=Character()
clock=pygame.time.Clock()
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==KEYDOWN:
            if event.key==K_ESCAPE:
                running=False
    screen.fill(colors["black"])
    keyboard_commands=pygame.key.get_pressed()
    character.update_coordinates(keyboard_commands)
    character.jump()#should come after update_coordinates since it depends on is_jumping variable
    character.move()# comes after all forms of repositioning...
    screen.blit(character.surface,character.rect)
    pygame.display.update()
    clock.tick(27)#27 FPS therefore slower...
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
pygame.quit()


