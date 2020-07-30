import pygame
import pygame.camera
from pygame.locals import *
import sys

scr_w, scr_h = 1280, 720
M,N = 5,5
rw, rh = scr_w//M, scr_h//N
rect_list = []
img_list = []
current = []
img=None 

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
    for i in rect_list:
        if (pos_x > rect[0]) and (pos_x < rect[0]+rw) and (pos_y > rect[1]) and (pos_y > rect[1]+rh):
            return rect_list.index(rect)
    return None      


pygame.init()
camera = open_camera()
if camera:
    camera.start()
else:
    print('Cannot open camera')
    sys.exit(-1)

screen = pygame.display.set_mode((scr_w, scr_h))
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

for i in range(M):
    for j in range(N):
        rect = (i*rw, j*rh, rw, rh)
        rect_list.append(rect)
for i in range(len(rect_list)):
    current.append(i)

rect_up,rect_down = None,None
click = False
img = None
is_running = True
while is_running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
            if img:
                # save the current image into the output file
                pygame.image.save( img, 'image.jpg' )
        if e.type == pygame.MOUSEBUTTONDOWN:
            click = True
            mouse_down = pygame.mouse.get_pos()
            rect_down = swap_image(mouse_down)
        if e.type == pygame.MOUSEBUTTONUP:
            click = False
            mouse_up = pygame.mouse.get_pos()
            rect_up = swap_image(mouse_up)
        if rect_up != rect_down and rect_up != None and rect_down != None and not(click):
            current[rect_down],current[rect_up] = current[rect_up],current[rect_down]
            rect_up,rect_down = None,None

    # try to capture the next image from the camera 
    img = camera.get_image()
    if img is None:
        continue
    else :
        for split in range(len(rect_list)):
            img_list.append(img.subsurface(rect_list[split]))
    for i in range(len(rect_list)):
        surface.blit( img_list[current[i]], rect_list[i],)
        pygame.draw.rect( surface, (0,255,0), rect_list[i], 1)
    screen.blit( surface, (0,0) )
    pygame.display.update()
    img_list = []

# close the camera
camera.stop()

print('Done....')