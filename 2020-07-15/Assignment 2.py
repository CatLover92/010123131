# 6201012630045
#for assignment I
#Edit make new function

import pygame 
from random import randint
from random import choice
import math

pygame.init()
pygame.display.set_caption('Assignment 2') 


clock = pygame.time.Clock()

# Set screen size 
scr_w, scr_h = 800, 600
screen  = pygame.display.set_mode((scr_w, scr_h))

# Build Circle Class
class Circle():
    def __init__(self):
        self.x = randint(0,scr_w)
        self.y = randint(0,scr_h)
        self.radius = randint(10,20)
        self.red = randint(0,255)
        self.green = randint(0,255)
        self.blue = randint(0,255)
        self.alpha = randint(100,255)
        self.color = (self.red,self.green,self.blue,self.alpha)
        self.x_speed = choice(movespd)
        self.y_speed = choice(movespd)
        self.colli = True
                
    def create(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def delete(self):
        pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.radius)

# Make Draw Function
def Draw(Num_ofCircle):
    global List_of_circle, godraw
    count = 0
    i = 0
    test = True
    while test:
        List_of_circle.append('c'+str(i))
        List_of_circle[i] = Circle()
        draw = True
        for j in range(len(List_of_circle)):
            #Distance
            if i != j:
                dist = int(math.hypot(List_of_circle[i].x - List_of_circle[j].x, List_of_circle[i].y - List_of_circle[j].y))
                
                #Not Draw if overlap     
                if dist < int(List_of_circle[i].radius+List_of_circle[j].radius):
                    draw = False
                
        if draw:
            List_of_circle[j].create()
            godraw.append(List_of_circle[j])
            count += 1
        if count == Num_ofCircle:
            test = False
        else:
            i += 1
    return godraw
# Check if cursor in circle
def isInside(circle_x, circle_y, radius, x, y): 
      
    if ((x - circle_x) * (x - circle_x) + 
        (y - circle_y) * (y - circle_y) <= radius**2): 
        return True
    else: 
        return False
# Check if circle is the biggest
def isBiggest(target, all):
    big_count = 0
    for k in all:
        if target != k:
            if target.radius >= k.radius:
                big_count += 1
    if big_count == len(all) - 1:
        return True
    else:
        return False
# Have no circles in window
def noCircles():
    if len(godraw) == 0:
        return True
    else:
        return False
# Update coordinate
def update(item):
    item.x += item.x_speed
    item.y += item.y_speed
    item.top = item.y - item.radius
    item.bot = item.y + item.radius
    item.left = item.x - item.radius
    item.right = item.x + item.radius
#hit border
def checkColliBorder(item):
    if item.x < item.radius or item.x > scr_w - item.radius:
        item.x_speed *= -1
    if item.y < item.radius or item.y > scr_h - item.radius:
        item.y_speed *= -1
#hit other circle
def checkother(item,other):
    more_dist = math.hypot(item.x - other.x , item.y - other.y)
    sum_r = item.radius + other.radius
    if more_dist - sum_r <= 3:
        # Change directions
        itemSpeed = math.sqrt((item.x_speed ** 2) + (item.y_speed ** 2))
        XDiff = - (item.x - other.x)
        YDiff = - (item.y - other.y)
        if XDiff > 0:
            if YDiff > 0:
                Angle = math.degrees(math.atan(YDiff / XDiff))
                XSpeed = - itemSpeed * math.cos(math.radians(Angle))
                YSpeed = - itemSpeed * math.sin(math.radians(Angle))
            elif YDiff < 0:
                Angle = math.degrees(math.atan(YDiff / XDiff))
                XSpeed = - itemSpeed * math.cos(math.radians(Angle))
                YSpeed = - itemSpeed * math.sin(math.radians(Angle))
        elif XDiff < 0:
            if YDiff > 0:
                Angle = 180 + math.degrees(math.atan(YDiff / XDiff))
                XSpeed = - itemSpeed * math.cos(math.radians(Angle))
                YSpeed = - itemSpeed * math.sin(math.radians(Angle))
            elif YDiff < 0:
                Angle = -180 + math.degrees(math.atan(YDiff / XDiff))
                XSpeed = - itemSpeed * math.cos(math.radians(Angle))
                YSpeed = - itemSpeed * math.sin(math.radians(Angle))
        elif XDiff == 0:
            if YDiff > 0:
                Angle = -90
            else:
                Angle = 90
            XSpeed = itemSpeed * math.cos(math.radians(Angle))
            YSpeed = itemSpeed * math.sin(math.radians(Angle))
        elif YDiff == 0:
            if XDiff < 0:
                Angle = 0
            else:
                Angle = 180
            XSpeed = itemSpeed * math.cos(math.radians(Angle))
            YSpeed = itemSpeed * math.sin(math.radians(Angle))
        item.x_speed = int(XSpeed)
        item.y_speed = int(YSpeed)


movespd = [-3,3]
godraw = []
List_of_circle = []
Num_ofCircle = 10
running = True

#loop
while running:
    clock.tick( 25 ) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for n in godraw:
                if isInside(n.x, n.y, n.radius, mouse_pos[0], mouse_pos[1]):
                    if isBiggest(n, godraw):
                        n.delete()
                        godraw.remove(n)
    
    screen.fill((0,0,0))
    
    if noCircles():
        Draw(Num_ofCircle)
    
    for a in godraw:
        checkColliBorder(a)
        for b in godraw:
            if a != b:
                checkother(a,b)
                
    for c in godraw:
        update(c)
        c.delete()
        c.create()
    
    pygame.display.flip()

pygame.quit()

#ref https://stackoverflow.com/questions/46702987/python-pygame-randomly-draw-non-overlapping-circles
#ref https://stackoverflow.com/questions/29833035/how-do-i-check-to-see-if-a-mouse-click-is-within-a-circle-in-pygame
#ref https://stackoverflow.com/questions/19370622/pygame-simple-bouncing-animation
#ref http://www.geometrian.com/programming/projects/index.php?project=Circle%20Collisions
#ref other student code
