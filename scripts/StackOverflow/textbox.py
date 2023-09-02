import pygame
pygame.init()
colors=dict(red=(255,0,0),green=(0,255,0),blue=(0,0,255),white=(255,255,255),black=(0,0,0))
screen_width,screen_height=(500,500)
screen=pygame.display.set_mode((screen_width,screen_height))
textbox=pygame.Surface((300,40))
screen_center=screen_width/2,screen_height/2
rect=textbox.get_rect(center=screen_center)
active=False
characters=[]
font=pygame.font.SysFont('comicsans',18, bold=False, italic=False, constructor=None)
from pygame.locals import(
    K_BACKSPACE,K_RETURN
)
cursor=True
running=True
clock=pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                active=True
                print('active')
            else:
                active=False
                print('inactive')
        elif event.type==pygame.KEYDOWN:
            if event.key==K_BACKSPACE:
                cursor=True
                if characters:
                    characters.pop()
            elif event.key==K_RETURN:
                print("user said {}".format("".join(characters)))
                print('font to char ratio for textbox of width=300: {}'.format(12/len(characters)))
                characters=[]
            else:
                if active:
                    if characters:
                        if characters[-1]=='|':
                            characters.pop()
                    characters.append(event.unicode)
                    cursor=True

    if cursor:
        characters.append('|')
        cursor=False
    else:
        if characters:
            if characters[-1]=='|':
                characters.pop()
                cursor=True

    

    screen.fill(colors.get('white'))
    pygame.draw.rect(screen,colors.get('blue'),rect,width=1)
    text=font.render("".join(characters),1,colors.get('black'))
    screen.blit(text,[rect.left+10,rect.bottom-30])
    pygame.display.flip()
    clock.tick(10)

pygame.quit()