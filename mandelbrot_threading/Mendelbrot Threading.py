import threading
import pygame
import cmath

N=100 #number of thread
scr_w, scr_h = 500,500 
scale = 0.006
offset = complex(-0.55, 0.0)

#list_semaphores = [ threading.Semaphore(0) for i in range(N) ]

# a list for keeping the thread objects
list_threads = []

# initialize pygame
pygame.init()

# create a screen of width=500 and height=500
screen = pygame.display.set_mode( (scr_w, scr_h) )
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

# set window caption
pygame.display.set_caption('Mandelbrot Multithreads') 


def mandelbrot(c,max_iters=100):
    i = 0
    z = complex(0,0)
    while abs(z) <= 2 and i < max_iters:
        z = z*z + c
        i += 1 
    return i

def thread_func(start,surface):
    for x in range(int(scr_w/N)):
        for y in range(int(scr_h)):
            re = scale*(start+x-scr_w/2) + offset.real
            im = scale*(y-scr_h/2) + offset.imag
            c = complex(re, im)
            color = mandelbrot(c, 63)
            r = (color << 6) & 0xc0
            g = (color << 4) & 0xc0
            b = (color << 2) & 0xc0
            surface.set_at((start+x, y), (255-r,255-g,255-b))
        screen.blit(surface, (0,0))
        pygame.display.update()
    print('{} worked.'.format( threading.currentThread().getName() ) )
    
for i in range(N):
    t = threading.Thread(target=thread_func, args=(int(i*scr_w/N),surface))
    list_threads.append( t )

for t in list_threads:
    t.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()