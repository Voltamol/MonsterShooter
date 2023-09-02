import pygame
pygame.init()
SCREEN_WIDTH,SCREEN_HEIGHT=500,500
screen=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

from pygame.locals import(
    KEYDOWN,
    K_ESCAPE,
    K_DOWN,
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)

colors=dict(
    black=[0,0,0],
    white=[255,255,255],
    red=[255,0,0],
    green=[0,255,0],
    blue=[0,0,255]
    )

from math import pow
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.speed=5
        self.isJumping=False
        self.jumpCount=10
        self.velocity=[0,0]
        self.dimensions=[35,70]
        self.position=[10,SCREEN_HEIGHT]
        self.surface=pygame.Surface(self.dimensions)
        self.surface.fill(colors["white"])
        self.rect=self.surface.get_rect(center=self.position)

    def update_coordinates(self,keyboard):
        self.velocity=[0,0]
        if keyboard[K_LEFT]:
            self.velocity[0]=-self.speed
        elif keyboard[K_RIGHT]:
            self.velocity[0]=self.speed
        elif keyboard[K_SPACE]:
            # these nested if-statements prevent the character from jumping while in mid-air
            if self.rect.bottom==SCREEN_HEIGHT:
                if not self.isJumping:
                    self.isJumping=True
                    self.jumpCount=10

    def move(self):
        #moving the character
        self.rect.move_ip(*self.velocity)
        #preventing it from moving off the screen
        if self.rect.left<0:
            self.rect.left=0 
        elif self.rect.right>SCREEN_WIDTH:
            self.rect.right=SCREEN_WIDTH
        elif self.rect.top<0:
            self.rect.top=0
        elif self.rect.bottom>SCREEN_HEIGHT:
            self.rect.bottom=SCREEN_HEIGHT

    def jump(self):
        if self.isJumping:
            if self.jumpCount>=-10:
                jumpSize=pow(self.jumpCount,2)
                self.jumpCount-=1
                if self.jumpCount>=0:
                    self.velocity[1]=-jumpSize
                else:
                    self.velocity[1]=jumpSize
            else:
                self.isJumping=False

running=True
player=Player()
clock=pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==KEYDOWN:
            if event.key==K_ESCAPE:
                running=False
    pressed_key=pygame.key.get_pressed()
    player.update_coordinates(pressed_key)
    screen.fill(colors["black"])
    player.jump()
    player.move()
    screen.blit(player.surface,player.rect)
    pygame.display.flip()
    clock.tick(27)

pygame.quit()