import pygame,sys
from math import radians,degrees,cos,sin,atan2,sqrt
from pygame.locals import *
from pygame.math import Vector2

pygame.init()

#Open Pygame window
screen = pygame.display.set_mode((640, 480),) #add RESIZABLE ou FULLSCREEN
#title
pygame.display.set_caption("orbital_rottation")
BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
CLOCK=pygame.time.Clock()
SCREEN_WIDTH=640
SCREEN_HEIGHT=480

sphere_pos=Vector2(420,340)
sphere_angle=sphere_pos.angle_to((0,0))
sphere_pos=[420,340]
orbit_pos=[320,240]
ray=0

def dda(x1,y1,x2,y2): #Digital Differential Analyzer Algorithm
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
       steps = abs(dx)
    else:
       steps = abs(dy)  
    Xincrement = dx / steps
    Yincrement = dy / steps
    x=x1
    y=y1
    for i in range(steps):
        pygame.draw.rect(screen,(0,255,0), [x, y,5,5], 0)
        x = x + Xincrement
        y = y + Yincrement
    pygame.display.flip()

def orbital_rotation(angle):
    sphere_pos[0]-=orbit_pos[0]
    sphere_pos[1]-=orbit_pos[1]
    sphere_pos.rotate_ip(angle)
    sphere_pos[0]+=orbit_pos[0]
    sphere_pos[1]+=orbit_pos[1]
    
def orbital_rotation2(angle):
    """x = x*cos(a) - y*sin(a)
       y = x*sin(a) + y*cos(a)"""
    sphere_pos[0]-=orbit_pos[0]
    sphere_pos[1]-=orbit_pos[1]
    x=sphere_pos[0]
    y=sphere_pos[1]    
    sphere_pos[0]=x*cos(radians(angle))-y*sin(radians(angle))
    sphere_pos[1]=x*sin(radians(angle))+y*cos(radians(angle))
    sphere_pos[0]+=orbit_pos[0]
    sphere_pos[1]+=orbit_pos[1]

def orbital_rotation3(angle):
    sphere_pos[0]-=orbit_pos[0]
    sphere_pos[1]-=orbit_pos[1]    
    angle=degrees(atan2(sphere_pos[1],sphere_pos[0]))+angle
    magnitude=sqrt(sphere_pos[0]*sphere_pos[0]+sphere_pos[1]*sphere_pos[1])
    sphere_pos[0]=cos(radians(angle))*magnitude
    sphere_pos[1]=sin(radians(angle))*magnitude
    sphere_pos[0]+=orbit_pos[0]
    sphere_pos[1]+=orbit_pos[1]

    
pygame.key.set_repeat(400, 30)

while True:
    
    #loop speed limitation
    #30 frames per second is enough
    CLOCK.tick(30)
    
    
    for event in pygame.event.get():    #wait for events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
           if event.key == K_RIGHT:
              orbital_rotation2(10)
              ray=0
           elif event.key == K_LEFT:
              orbital_rotation2(-10)
              ray=0
           elif event.key == K_d:
              #dda(int(orbit_pos[0]),int(orbit_pos[1]),int(sphere_pos[0]),int(sphere_pos[1]))
              ray=1
              
           
    if not ray:         
       screen.fill(BLACK)    
    pygame.draw.circle(screen,(0,255,0),(int(sphere_pos[0]),int(sphere_pos[1])),10)
    pygame.draw.circle(screen,(0,0,255),orbit_pos,10)
    pygame.display.flip()
