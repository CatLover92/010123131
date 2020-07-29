import pygame
import pygame.camera
from pygame.locals import *
import sys

scr_w, scr_h = 1280, 720
M,N = 3,4
rw, rh = scr_w//M, scr_h//N
list_blackrect = []
list_remove = []

def open_camera( frame_size=(1280,720),mode='RGB'):
    pygame.camera.init()
    list_cameras = pygame.camera.list_cameras()
    print( 'Mumber of cameras found: ', len(list_cameras) )
    if list_cameras:
        # use the first camera found
        camera = pygame.camera.Camera(list_cameras[0], frame_size, mode )
        return camera 
    return None 

def clickinside():
    for i in range(M):
        range_x = range(i*rw, i*rw + rw)
        for j in range(N):
            range_y = range(j*rh, j*rh + rh)
            if mouse_pos[0] in range_x and mouse_pos[1] in range_y:
                remove_rect = (i*rw, j*rh, rw, rh)
                if remove_rect in list_blackrect:
                    list_blackrect.remove(remove_rect)
                    list_remove.append(remove_rect)


pygame.init()
camera = open_camera()
if camera:
    camera.start()
else:
    print('Cannot open camera')
    sys.exit(-1)

screen = pygame.display.set_mode((scr_w, scr_h))

surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

img = None
is_running = True 

for i in range(M):
    for j in range(N):
        black = (i*rw, j*rh, rw, rh)
        if black not in list_blackrect:
            list_blackrect.append(black)


while is_running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
            if img:
                # save the current image into the output file
                pygame.image.save( img, 'image.jpg' )
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clickinside()

                
    # try to capture the next image from the camera 
    img = camera.get_image()
    if img is None:
        continue
    
    # get the image size
    img_rect = img.get_rect()
    img_w, img_h = img_rect.w, img_rect.h

    # draw (MxN) tiles of the images
    M,N = 3,4
    rw, rh = scr_w//M, scr_h//N

    if len(list_blackrect) !=0:
        for black in list_blackrect:
            pygame.draw.rect(surface, (0,255,0), black, 1)

    if len(list_remove) !=0:
        for removed in list_remove:
            surface.blit(img,removed,removed)

    # write the surface to the screen and update the display
    screen.blit( surface, (0,0) )
    pygame.display.update()

# close the camera
camera.stop()

print('Done....')