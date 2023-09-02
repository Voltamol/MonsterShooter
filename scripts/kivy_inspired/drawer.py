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
from pygame.locals import(
    K_BACKSPACE,
    K_RETURN
)
screen_width,screen_height=(500,500)
screen=pygame.display.set_mode((screen_width,screen_height))
#================================ font ==================
font=pygame.font.SysFont('comicsans',30, bold=True, italic=False, constructor=None)
#========================================================
#============== Alternatives to switch ====================
switch_event={
    pygame.QUIT:'quit',
    pygame.MOUSEBUTTONDOWN:'mouse_button_down',
    pygame.KEYDOWN:'keydown',
    K_BACKSPACE:'backspace',
    K_RETURN:'return'
}

clickables=[]
def get_clicked(event):
    for handler in clickables:
        if handler.collidepoint(event.pos):
            return handler
    return None

#============== singleton metaclass ======================
class Singleton(type):
    def __call__(cls,*args,**kwargs):
        try:
            return cls.instance
        except AttributeError:
            cls.instance=super(Singleton,cls).__call__(*args,**kwargs)
            return cls.instance

#============== event_listener ===========================
class Listener(metaclass=Singleton):
    def quit(self,event):
        global running
        running=False
    
    def mouse_button_down(self,event):
        global nav_button
        handler=get_clicked(event)
        if handler:
            handler.handle_click()

    def listen(self):
        """this one is not a pygame event but rather determines current event"""
        for event in pygame.event.get():
            self.notify_handler(event)

    def notify_handler(self,event):
        """this one makes sure the appropriate event_handler handles current event"""
        event_name=switch_event.get(event.type)
        if event_name is None:
            return
        event_handler=getattr(self,event_name)
        return event_handler(event)
        
#=========================================================
#forcing method definition
from abc import ABCMeta,abstractmethod
#creating a parent class to enforce an abstract method

class EventHandler(metaclass=ABCMeta):
    """every future shape/rendered font is an event handler of its own"""
    def __init__(self):
        global clickables
        clickables.append(self)

    @abstractmethod
    def handle_click(self):
        pass
    #most actions are done on/by rect hence the following 2 methods
    def __getattribute__(self,attributename):
        return super().__getattribute__(attributename)

    def __getattr__(self,attributename):
        rect=super(EventHandler,self).__getattribute__('rect')
        return getattr(rect,attributename)


#=============== Navgation Drawer=========================
class Drawer(pygame.sprite.Sprite):
    def __init__(self):
        super(Drawer,self).__init__()
        self.surface=pygame.Surface((screen_width/2.5,screen_height))
        self.container=self.surface.get_rect()
        self.width=self.container.width
        self.speed=10
        self.moving=False

    def draw(self,canvas):
        pygame.draw.rect(canvas,colors.get('dark_gray'),self.container)
  
    def move(self):
        global nav_button
        if self.moving:
            if self.container.right<=0:
                self.speed*=-1
            elif self.container.left>=0:
                self.speed*=-1
            self.container.move_ip([self.speed,0])
            if self.container.right<=0:
                self.moving=False
                nav_button.nav_color='dark_gray'
            elif self.container.left>=0:
                self.moving=False
                nav_button.nav_color='light_gray'

            
#================INSTANTIATING DRAWER=====================
drawer=Drawer()
#====================== Nav Button =======================

class NavButton(EventHandler,pygame.sprite.Sprite):
    def __init__(self):

        super(NavButton,self).__init__()
        #navbutton properties
        self.nav=pygame.Surface((20,20))
        self.rect=self.nav.get_rect()
        self.nav_color='light_gray'
        self.nav_x=self.rect.center[0]
        self.nav_y=self.rect.center[1]

    def handle_click(self):
        """when clicked it toggles the naviation drawer"""
        global drawer
        drawer.moving=True

nav_button=NavButton()
#=========================================================
clock=pygame.time.Clock()
event_listener=Listener()
running=True
while running:
    #listening for events(click,keypress,...)
    event_listener.listen()
    #giving the screen a white color
    screen.fill(colors.get('white'))
    #getting navigation drawer ready to move in and out of screen
    drawer.move()
    #displaying drawer
    drawer.draw(screen)
    #writing something inside the nav_button
    nav_text=font.render("+",1,colors.get(nav_button.nav_color))
    #displaying the text
    screen.blit(nav_text,(nav_button.nav_x-10,nav_button.nav_y-25))
    #flipping(mandatory)
    pygame.display.flip()
    #frames per second(currently set to 27)
    clock.tick(27)

pygame.quit()
