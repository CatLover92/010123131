import pygame
import pygame.camera
from pygame.locals import *
import sys

scr_w, scr_h = 1280, 720
list_rect = []
M,N = 5,5
rw, rh = scr_w//M, scr_h//N
list_swap_img = []
img = None
current = []
Drag_rect,Drop_rect = None,None

screen = pygame.display.set_mode((scr_w, scr_h))
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

pygame.init()

def open_camera( frame_size=(1280,720),mode='RGB'):
    pygame.camera.init()
    list_cameras = pygame.camera.list_cameras()
    print( 'Mumber of cameras found: ', len(list_cameras) )
    if list_cameras:
        # use the first camera found
        camera = pygame.camera.Camera(list_cameras[0], frame_size, mode )
        return camera 
    return None 
def swap_image(mouse):
    pos_x,pos_y = mouse[0],mouse[1]
    for rect in list_rect:
        if (pos_x > rect[0]) and (pos_x < rect[0]+rw) and (pos_y > rect[1]) and (pos_y < rect[1] + rh):
            return list_rect.index(rect)
    pass

camera = open_camera()

if camera:
    camera.start()
else:
    print('Cannot open camera')
    sys.exit(-1)

while(img == None):
    img = camera.get_image()

for i in range(M):
        for j in range(N):
            rect = (i*rw, j*rh, rw, rh)
            list_rect.append(rect)      
for i in range(len(list_rect)):
    current.append(i)
    

is_running = True 

while is_running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
            if img:
                # save the current image into the output file
                pygame.image.save( img, 'image.jpg' )
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouse_down_pos = pygame.mouse.get_pos()
            Drag_rect = swap_image(mouse_down_pos)
        elif e.type == pygame.MOUSEBUTTONUP:
            mouse_up_pos = pygame.mouse.get_pos()
            Drop_rect = swap_image(mouse_up_pos)
            current[Drag_rect],current[Drop_rect] = current[Drop_rect],current[Drag_rect]
            Drop_rect,Drag_rect = None,None

    img = camera.get_image()
    if img is None:
        continue
    else:
        for i in range(len(list_rect)):
            list_swap_img.append(img.subsurface(list_rect[i]))
    for i in range(len(list_rect)):
        surface.blit( list_swap_img[current[i]], list_rect[i])
        pygame.draw.rect( surface, (0,255,0), list_rect[i], 1)
    screen.blit( surface, (0,0) )
    pygame.display.update()
    list_swap_img = []
# close the camera
camera.stop()
print('Done....')
