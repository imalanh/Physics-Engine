from pygame import *
from random import *
import math

screen = display.set_mode((800,600))
running = True
global_accel = [0, 1]
energy_loss = 1

class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
    def __setitem__(self, key, val):
        if key == 0:
            self.x = val
        elif key == 1:
            self.y = val
        
    def dot_product(self, vec):
        return vec.x*self.x + vec.y*self.y

    def sub(self,vec):
        """returns vector resulting in self-vec"""
        return Vec(self.x-vec.x,self.y-vec.y)

    def magnitude(self):
        """returns the magnitude"""
        return math.hypot(self.x,self.y)
    def recip(self):
        return Vec(-self.y,self.x)
    def unit(self):
        m = self.magnitude()
        return Vec(self.x/self.magnitude(),self.y/self.magnitude())
    def scale(self,a):
        return Vec(self.x*a,self.y*a)
    
    def proj(self,vec):
        """returns proj of self onto vec"""
        return vec.scale((vec.dot_product(self)/vec.magnitude()**2))
    def localAdd(self,vec):
        self.x+=vec.x
        self.y+=vec.y
    def localSub(self,vec):
        self.x-=vec.x
        self.y-=vec.y
    def __str__(self):
        return "(%.2f,%.2f)"%(self.x,self.y)
    def __repr__(self):
        return "(%.2f,%.2f)"%(self.x,self.y)
class ball:
    def __init__(self, x, y, radius, mass):
        self.mass = mass
        self.radius = radius
        self.location = Vec(x,y)
        self.velocity = Vec(10, -10)
        draw.circle(screen, (0,255,0), (x, y), radius, 0)

    def update(self):
        self.velocity.x += global_accel[0] 
        self.velocity.y += global_accel[1] 
        self.location.x += self.velocity.x
        self.location.y += self.velocity.y
    def check_collision(self, ball):
        dist = ball.location.sub(self.location)
        mag = dist.magnitude()
        if mag < ball.radius*2:
            #dist = ball.location.sub(self.location)
            localaxis = dist.unit()
            #normalaxis = dist.recip().unit()
            tmp = self.velocity.proj(localaxis)
            tmp2 = ball.velocity.proj(localaxis)
            self.velocity.localSub(tmp)
            ball.velocity.localAdd(tmp)
            ball.velocity.localSub(tmp2)
            self.velocity.localAdd(tmp2)
                
            #set the two balls just far enough C:
            deltaDist = (ball.radius*2-mag)/2 + 1
            self.location.localSub(localaxis.scale(deltaDist))
            ball.location.localAdd(localaxis.scale(deltaDist))
        
    def render(self, screen):
        draw.circle(screen, (0,255,0), (round(self.location[0]), round(self.location[1])), self.radius, 0)
    
class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.location = Vec(x, y)
        draw.rect(screen, (0,255,0), (200, 150, 100, 50))

    #def check_collision(self, ball):
     #   self.x = 0

class physics_space:
    def __init__(self):
        self.objects = []
        
    def add_obj(self, obj):
        self.objects.append(obj)

    def render(self,screen):
        for x in self.objects:
            x.render(screen)

    def collision(self):
        for i in range(len(self.objects)):
            for j in range(len(self.objects)):
                if(i != j):
                    self.objects[i].check_collision(self.objects[j])
        
    def update(self):
        self.collision()
        for x in self.objects:
            x.update()
            if(x.location[0] > 800 - x.radius):
                x.velocity.x = x.velocity.x * -energy_loss + global_accel[0]
                x.location[0] = 800 - x.radius
            elif(x.location[0] < x.radius):
                x.velocity.x = x.velocity.x * -energy_loss + global_accel[0]
                x.location[0] = x.radius
            if(x.location[1] > 600 - x.radius):
                x.velocity.y = x.velocity.y * -energy_loss + global_accel[1]
                x.location[1] = 600 - x.radius
            elif(x.location[1] < x.radius):
                x.velocity.y = x.velocity.y * -energy_loss + global_accel[1]
                x.location[1] = x.radius

            

world = physics_space()
for i in range(3):
    y = randint(100,200)
    x = randint(100,700)
    mass = randint(1, 4)
    myBall = ball(x, y, 30, mass)
    world.add_obj(myBall)
#plat = Platform(69, 69)
#world.add_obj(plat)
myClock = time.Clock()
fps = 30
while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    screen.fill((0,0,0))

    world.update()
    world.render(screen)
    myClock.tick(fps)
    display.flip()
quit()
