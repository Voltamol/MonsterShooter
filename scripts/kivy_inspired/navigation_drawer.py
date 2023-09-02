import pygame
pygame.init()
colors=dict(
    red=(255,0,0),
    green=(0,255,0),
    blue=(0,0,255),
    white=(255,255,255),
    black=(0,0,0),
    light_gray=(250,250,250),
    dark_gray=(200,200,200)
)
screen_width,screen_height=(500,500)
screen=pygame.display.set_mode((screen_width,screen_height))

#================================ font ==================
font=pygame.font.SysFont('comicsans',30, bold=True, italic=False, constructor=None)
#========================================================
#=============== Navgation Drawer=========================
drawer=pygame.Surface((screen_width/2.5,screen_height))
drawer_container=drawer.get_rect()
drawer_width=drawer_container.width
drawer_speed=5
drawer_current_speed=0
iterations=drawer_width//drawer_speed
itercount=iterations
#=========================================================

#====================== Nav Button =======================
nav=pygame.Surface((20,20))
button_container=nav.get_rect()
nav_color='light_gray'
nav_x,nav_y=button_container.center
#=========================================================
clock=pygame.time.Clock()
drawer_visible=True
drawer_toggled=False
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if button_container.collidepoint(event.pos):
                drawer_toggled=True
                if drawer_visible:
                    drawer_current_speed=-drawer_speed
                else:
                    drawer_current_speed=drawer_speed
                    
    if drawer_container.right<0:
        drawer_visible=False
        nav_color='black'

    elif drawer_container.left>0:
        drawer_visible=True
        nav_color='light_gray'

    if not drawer_toggled:
        drawer_current_speed=0
    
    drawer_container.move_ip([drawer_current_speed,0])
    screen.fill(colors.get('white'))
    pygame.draw.rect(screen,colors.get('dark_gray'),drawer_container)
    #pygame.draw.rect(screen,colors.get('white'),button_container)
    nav_text=font.render("+",1,colors.get(nav_color))
    screen.blit(nav_text,(nav_x-10,nav_y-25))
    pygame.display.flip()
    clock.tick(27)
    
pygame.quit()