import pygame,sys
from math import *
from pygame.locals import *

pygame.init()

BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
BLUE=(  0,   0, 255)
GREY=(245, 245, 245)
CLOCK=pygame.time.Clock()
#Open Pygame window
WIDTH,HEIGHT=640,480
WALL,SPRITE=0,1
screen = pygame.display.set_mode((WIDTH, HEIGHT),) #add RESIZABLE or FULLSCREEN
#title
pygame.display.set_caption("raycaster")

grid=[[1,1,1,1,1,1,1,1,1,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,1,0,0,0,0,1],
      [1,0,0,0,1,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,1,1,1,1,1,1,1,1,1]]

sprite=pygame.image.load('plant-green.png').convert_alpha()
sprite2=pygame.image.load('armor.png').convert_alpha()
sprite_scaled=sprite
sprite_size=64
half_sprite_size=int(sprite_size/2)
sprite_scaled_size=64
sprite_pos=[64*3,64*2]
sprite_pos2=[64*7,64*4]
sprite_grid_pos=[int(sprite_pos[1]//64),int(sprite_pos[0]//64)] 
sprite_dist=10;sprite_x=10;sprite_y=10

texture=pygame.image.load('dk_wall.png').convert()
texture2=pygame.image.load('wolf_floor.png').convert()
ground=pygame.Surface((640,240)).convert();ground.fill((0,100,0))
x_limit=len(grid[0]);y_limit=len(grid)
#put resolution value to 1 for a clear display but it will be too slow
resolution=3
wall_hit=0
#field of view (FOV) 
fov=60
half_fov=fov/2
grid_height=64;grid_width=64;wall_height=64;wall_width=64
player_height=wall_height/2
player_pos=[160,224]
view_angle=45
#Dimension of the Projection Plane
projection_plane=[WIDTH, HEIGHT]
#Center of the Projection Plane
plane_center=HEIGHT//2 #[WIDTH/2, HEIGHT/2]
#distance from player to projection plane
to_plane_dist=int((WIDTH/2)/tan(radians(fov/2)))
#Angle between subsequent rays
angle_increment=fov/WIDTH
#angle of the casted ray
ray_angle=view_angle+(fov/2)

class game_objects:
    def __init__(self, pos=[0,0], image=None, obj_type=None):
        self.pos = pos
        self.grid_pos = [0,0]
        self.distance = 0
        self.image = image
        self.type = obj_type
        
screen_columns = [game_objects([x,0],None,WALL) for x in range(0,WIDTH,resolution)]
sprites = [game_objects(sprite_pos, sprite, SPRITE),
           game_objects(sprite_pos2, sprite2, SPRITE)]
objects_to_draw = screen_columns + sprites


move_speed=15
x_move=int(move_speed*cos(radians(view_angle)))
y_move=-int(move_speed*sin(radians(view_angle)))
rotation_speed=3

pygame.key.set_repeat(400, 30)

while True:
    
    #loop speed limitation
    #30 frames per second is enough
    CLOCK.tick(30)
    
    for event in pygame.event.get():    #wait for events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    #Movement controls
    keys = pygame.key.get_pressed()
 
    if keys[K_UP]:
       player_pos[0]+=x_move
       player_pos[1]+=y_move
       if grid[player_pos[1]//grid_height][player_pos[0]//grid_width]==1:
          player_pos[0]-=x_move
          player_pos[1]-=y_move
    elif keys[K_DOWN]:
       player_pos[0]-=x_move
       player_pos[1]-=y_move
       if grid[player_pos[1]//grid_height][player_pos[0]//grid_width]==1:
           player_pos[0]+=x_move
           player_pos[1]+=y_move       
    if keys[K_LEFT]:
       view_angle+=rotation_speed
       if view_angle>360:view_angle-=360
       x_move=int(move_speed*cos(radians(view_angle)))
       y_move=-int(move_speed*sin(radians(view_angle)))
    elif keys[K_RIGHT]:
       view_angle-=rotation_speed
       if view_angle<0:view_angle+=360
       x_move=int(move_speed*cos(radians(view_angle)))
       y_move=-int(move_speed*sin(radians(view_angle)))

       
    """if event.type == KEYDOWN:
            if event.key == K_UP:
               player_pos[0]+=x_move
               player_pos[1]+=y_move
            elif event.key == K_DOWN:
               player_pos[0]-=x_move
               player_pos[1]-=y_move
            elif event.key == K_LEFT:
               view_angle+=rotation_speed
               if view_angle>395:ray_angle-=360
               x_move=int(move_speed*cos(radians(view_angle)))
               y_move=int(move_speed*sin(radians(view_angle))*-1)               
            elif event.key == K_RIGHT:
               view_angle-=rotation_speed
               if view_angle<0:ray_angle+=360
               x_move=int(move_speed*cos(radians(view_angle)))
               y_move=int(move_speed*sin(radians(view_angle))*-1)"""
                 
    """here start raycasting"""
    
    #angle of the first casted ray
    ray_angle=view_angle+half_fov; i=0
    
    for x in range(0,WIDTH,resolution):
          
        if ray_angle<0:ray_angle+=360
        if ray_angle>360:ray_angle-=360
        if ray_angle==0:ray_angle+=0.01

        #tx and ty used to correct tangent direction
        if ray_angle>=0 and ray_angle<=90:tx=1;ty=-1#tan is(+)
        elif ray_angle>=91 and ray_angle<=180:tx=1;ty=1#tan is(-)
        elif ray_angle>=181 and ray_angle<=270:tx=-1;ty=1#tan is(+)
        elif ray_angle>=271 and ray_angle<=360:tx=-1;ty=-1#tan is(-)
        
        wall_hit=0;hor_wall_dist=ver_wall_dist=100000
        #(y_side)whether ray hit part of the block above the line,or the block below the line
        if ray_angle>=0 and ray_angle<=180:
           y_side=-1;signed_y=-1
        else:y_side=grid_height;signed_y=1
        #(x_side)whether ray hit left part of the block of the line,or the block right of the line
        if ray_angle>=90 and ray_angle<=270:
           x_side=-1;signed_x=-1
        else:x_side=grid_width;signed_x=1

        #tangante of the casted ray angle
        tan_angle=tan(radians(ray_angle))
        #first horizontal y step
        y_step=(player_pos[1]//grid_height)*(grid_height)+y_side
        #first horizontal x step (+0.4 to correct wall position)
        x_step=(player_pos[0]+abs(player_pos[1]-y_step)/tan_angle*tx)+0.4
        ray_x=x_step;ray_y=y_step
        ray_pos=[int(ray_y//grid_height),int(ray_x//grid_width)]
        #if there is a wall there
        if ray_pos[0]>=0 and ray_pos[0]<y_limit and  ray_pos[1]>=0 and ray_pos[1]<x_limit:
         if grid[ray_pos[0]][ray_pos[1]]==1:
           #finding distance to horizontal wall
           hor_wall_dist=int(sqrt((player_pos[0]-ray_x)**2+(player_pos[1]-ray_y)**2));wall_hit=1
         else:
           #from now horizontal x_step and y_step will remind the same for the rest of the casted ray
           x_step=(grid_height/tan_angle*tx);y_step=grid_height*signed_y
           ray_x+=x_step;ray_y+=y_step
           ray_pos=[int(ray_y//grid_height),int(ray_x//grid_width)]
           if ray_pos[0]>=0 and ray_pos[0]<y_limit and  ray_pos[1]>=0 and ray_pos[1]<x_limit:
            if grid[ray_pos[0]][ray_pos[1]]==1:
              #finding distance to horizontal wall
              hor_wall_dist=int(sqrt((player_pos[0]-ray_x)**2+(player_pos[1]-ray_y)**2));wall_hit=1
            else:
             while True:
                #remember that horizontal x_step and y_step will remind the same for the rest of the casted ray
                ray_x+=x_step;ray_y+=y_step
                ray_pos=[int(ray_y//grid_height),int(ray_x//grid_width)]
                if ray_pos[0]>=0 and ray_pos[0]<y_limit and  ray_pos[1]>=0 and ray_pos[1]<x_limit:
                 if grid[ray_pos[0]][ray_pos[1]]==1:
                   #finding distance to horizontal wall
                   hor_wall_dist=int(sqrt((player_pos[0]-ray_x)**2+(player_pos[1]-ray_y)**2));wall_hit=1
                   break
                else:break
        hor_wall_pos=ray_x
        
        #first vertical x step
        x_step=(player_pos[0]//grid_width)*(grid_width)+x_side
        #first vertical y step
        y_step=(player_pos[1]+abs(player_pos[0]-x_step)*tan_angle*ty)
        ray_x=x_step;ray_y=y_step
        ray_pos=[int(ray_y//grid_height),int(ray_x//grid_width)]
        #if there is a wall there
        if ray_pos[0]>=0 and ray_pos[0]<y_limit and  ray_pos[1]>=0 and ray_pos[1]<x_limit:
         if grid[ray_pos[0]][ray_pos[1]]==1: 
           #finding distance to vertical wall
           ver_wall_dist=int(sqrt((player_pos[0]-ray_x)**2+(player_pos[1]-ray_y)**2));wall_hit=1
         else:
          #from now verticaal x_step and y_step will remind the same for the rest of the casted ray
          x_step=grid_width*signed_x;y_step=(grid_width*tan_angle*ty)
          ray_x+=x_step;ray_y+=y_step
          ray_pos=[int(ray_y//grid_height),int(ray_x//grid_width)]
          if ray_pos[0]>=0 and ray_pos[0]<y_limit and  ray_pos[1]>=0 and ray_pos[1]<x_limit:
           if grid[ray_pos[0]][ray_pos[1]]==1:
             #finding distance to vertical wall
             ver_wall_dist=int(sqrt((player_pos[0]-ray_x)**2+(player_pos[1]-ray_y)**2));wall_hit=1
           else:
             while True:
                #remember that vertical x_step and y_step will remind the same for the rest of the casted ray
                ray_x+=x_step;ray_y+=y_step
                ray_pos=[int(ray_y//grid_height),int(ray_x//grid_width)]
                if ray_pos[0]>=0 and ray_pos[0]<y_limit and  ray_pos[1]>=0 and ray_pos[1]<x_limit:
                 if grid[ray_pos[0]][ray_pos[1]]==1:
                   #finding distance to horizontal wall
                   ver_wall_dist=int(sqrt((player_pos[0]-ray_x)**2+(player_pos[1]-ray_y)**2));wall_hit=1
                   break
                else:break
        ver_wall_pos=ray_y
        
        if wall_hit:         
           #chosing the closer distance          
           wall_dist=min(hor_wall_dist,ver_wall_dist)
           if wall_dist==hor_wall_dist:wall_side=1
           elif wall_dist==ver_wall_dist:wall_side=2
           """#chosing color for non-textured wall
           if wall_dist==hor_wall_dist:color=WHITE
           elif wall_dist==ver_wall_dist:color=GREY"""
           #to find the texture position with pressision
           if wall_side==1:wall_pos=int(hor_wall_pos)
           elif wall_side==2:wall_pos=int(ver_wall_pos)
           #finding the texture position
           texture_pos=int(wall_pos%wall_width)
           #invert the texture position for correction(-0.1 is to avoid error)
           if wall_side==1 and y_side==grid_height \
           or wall_side==2 and x_side==-1:
              texture_pos=int((wall_width-0.1)-texture_pos)
           #beta is the angle of the ray that is being cast relative to the viewing angle
           beta=radians(view_angle-ray_angle)
           cos_beta=cos(beta)
           #storing_distance_befbefore changing it
           screen_columns[i].distance = wall_dist
           #removing fish-eye effect
           wall_dist=(wall_dist*cos_beta)
           #Extract the part-column from the texture using the subsurface method:
           column=texture.subsurface(texture_pos,0,1,wall_height)       
           #finding the height of the projected wall slice
           slice_height=int(wall_height/wall_dist*to_plane_dist)
           #Scale it to the height at which we're going to draw it using transform.scale
           column = pygame.transform.scale(column, (resolution, slice_height))
           #the top position where the wall slice should be drawn
           slice_y=plane_center-(slice_height//2)
           """#shading(making shadow or fog)
           alpha=int(wall_dist*0.25)
           if alpha>255:alpha=255
           shadow=pygame.Surface((resolution,slice_height)).convert_alpha()
           shadow.fill((255,255,255,alpha))"""

           
           #now floor-casting and ceilings
           """cos_angle=cos(radians(ray_angle))
           sin_angle=-sin(radians(ray_angle))
           #begining of floor
           wall_bottom=slice_y+slice_height
           #begining of ceilings
           wall_top=slice_y
           #wall_bottom=plane_center+25
           #wall_top=plane_center-25
           while wall_bottom<HEIGHT:
              #(row at floor point-row of center)
              row=wall_bottom-plane_center
              #straight distance from player to the intersection with the floor 
              straight_p_dist=(player_height/row*to_plane_dist)
              #true distance from player to floor
              to_floor_dist=(straight_p_dist/cos_beta)
              #coordinates (x,y) of the floor
              ray_x=int(player_pos[0]+(to_floor_dist*cos_angle))
              ray_y=int(player_pos[1]+(to_floor_dist*sin_angle))
              #the texture position
              floor_x=(ray_x%wall_width);floor_y=(ray_y%wall_height)
              #shading(making shadow or fog)
              alpha2=int(to_floor_dist*0.25)
              if alpha2>255:alpha=255
              shadow2=pygame.Surface((resolution,resolution)).convert_alpha()
              shadow2.fill((255,255,255,alpha2))
              screen.blit(texture2,(x,wall_bottom),(floor_x,floor_y,resolution,resolution))
              #display_surface.blit(texture2,(x,wall_top),(floor_x,floor_y,resolution,resolution))
              #screen.blit(shadow2,(x,wall_bottom))
              #screen.blit(texture,(x,wall_top),(floor_x,floor_y,resolution,resolution))
              wall_bottom+=resolution
              wall_top-=resolution"""

           
           #drawing everything
           #pygame.draw.line(screen, WHITE, [x, slice_y], [x,slice_y+slice_height], resolution )
           #pygame.draw.rect(screen,color, [x, slice_y, resolution, slice_height], 0)#;print(x,slice_y,slice_height)
           #screen.blit(column,(x,slice_y))#;screen.blit(shadow,(x,slice_y))
           screen_columns[i].image = column
           screen_columns[i].pos[1] = slice_y
           i+= 1
        ray_angle-=angle_increment*resolution

    for spr in sprites:
        spr.distance = int(sqrt((player_pos[0]-spr.pos[0])**2+(player_pos[1]-spr.pos[1])**2))

    objects_to_draw.sort(key= lambda obj: obj.distance, reverse=True)

    for obj in objects_to_draw:
        if obj.type == WALL:
           screen.blit(obj.image,obj.pos)
        elif obj.type == SPRITE:
           
            #now projecting sprites
            #sprite_dist=int(sqrt((player_pos[0]-sprite_pos[0])**2+(player_pos[1]-sprite_pos[1])**2))
            sprite_boundary_angle = degrees(atan2(half_sprite_size,obj.distance))
            sprite_angle=degrees(atan2(player_pos[1]-obj.pos[1],-(player_pos[0]-obj.pos[0])))
            if sprite_angle<=0:sprite_angle+=360
            if (sprite_angle>270 and  view_angle<90):sprite_angle-=360
            elif (view_angle>270 and sprite_angle<90):sprite_angle+=360
            if -half_fov < (sprite_angle+sprite_boundary_angle)-view_angle < half_fov \
            or -half_fov < (sprite_angle-sprite_boundary_angle)-view_angle < half_fov:
               #if sprite_angle<0:sprite_angle+=360
               fov_start=view_angle+half_fov
               sprite_screen_angle=fov_start-sprite_angle
               #cases where the magnitude of the angles is small but the angles are far apart
               #like 1 degree and 359 degrees. You cant just subtract them, you need the interior angle
               #if (sprite_angle>270 and  view_angle<90):sprite_screen_angle+=360;
               #elif (view_angle>270 and sprite_angle<90):sprite_screen_angle-=360
               sprite_x=sprite_screen_angle/angle_increment  
               distance_ratio=to_plane_dist/obj.distance
               sprite_scaled_size=int(sprite_size*distance_ratio)
               half_sprite_scaled_size=sprite_scaled_size//2
               sprite_x-=half_sprite_scaled_size
               sprite_y=plane_center-half_sprite_scaled_size
               sprite_scaled=pygame.transform.scale(obj.image, (sprite_scaled_size, sprite_scaled_size))
               screen.blit(sprite_scaled,(sprite_x,sprite_y))
               #rect=sprite_scaled.get_rect()
               #rect.x=sprite_x;rect.y=sprite_y
               #pygame.draw.rect(screen,WHITE,rect,2)
    
    #measure the framerate   
    #print(CLOCK.get_fps())
    pygame.display.flip()
    screen.fill(BLUE)
    screen.blit(ground,(0,240))
