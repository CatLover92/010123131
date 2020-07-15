#6201012630045
#for Assignment I

import pygame 
from random import randint
import math

pygame.init()

pygame.display.set_caption('Assignment 1') 

clock = pygame.time.Clock()
scr_w, scr_h = 800, 600
screen = pygame.display.set_mode((scr_w, scr_h))

surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

class circle():
    def __init__(self):
        self.x = randint(0,scr_w)
        self.y = randint(0,scr_h)
        self.radius = randint(10,20)
        self.red = randint(0,255)
        self.green = randint(0,255)
        self.blue = randint(0,255)
        self.alpha = randint(100,255)
        self.color = (self.red,self.green,self.blue,self.alpha)
    
    def new(self):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        pygame.display.update()
    
    def delete(self):
        pygame.draw.circle(surface, (255,255,255), (self.x, self.y), self.radius)
        pygame.display.update()

# Find cursor in circle
def isInside(circle_x, circle_y, radius, x, y): 
      
    if ((x - circle_x) * (x - circle_x) + 
        (y - circle_y) * (y - circle_y) <= radius**2): 
        return True
    else: 
        return False

def isBiggest(target, all):
    b_count = 0
    for k in all:
        if target != k:
            if target.radius > k.radius:
                b_count+=1
            elif target.radius == k.radius:
                b_count+=1
    if b_count == len(all) - 1:
        return True
    else:
        return False
    
number_of_circles=0
c = []
go_draw = []
running = True
i = 0
count = 0
# Main code
while running:
    clock.tick( 10 ) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for n in go_draw:
                if isInside(n.x, n.y, n.radius, mouse_pos[0], mouse_pos[1]):
                    if isBiggest(n, go_draw):
                        n.delete()
                        go_draw.remove(n)

    while number_of_circles < 10 :
        c.append('c'+str(i))
        c[i] = circle()
        draw = True
        
        for j in range(len(c)):
            #check all circle class
            if i != j:
                distance = int(math.hypot(c[i].x - c[j].x, c[i].y - c[j].y))
                #if circle overlaped        
                if distance < int(c[i].radius+c[j].radius):
                    draw = False
            
        if draw:
            c[j].new()
            go_draw.append(c[j])
            number_of_circles+=1
        i+=1
    number_of_circles+=1        
    # fill the screen with the white color
    screen.fill((255,255,255))
    # draw the surface on the screen
    screen.blit(surface, (0,0))
    pygame.display.update()

pygame.quit()

#ref https://stackoverflow.com/questions/46702987/python-pygame-randomly-draw-non-overlapping-circles
#ref https://stackoverflow.com/questions/29833035/how-do-i-check-to-see-if-a-mouse-click-is-within-a-circle-in-pygame