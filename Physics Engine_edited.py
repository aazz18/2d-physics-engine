import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 600,600
clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Physics Engine')

# Constants
bounce_stop = 0.3
active = False
normal_scale = 100

#Parent class inherited by other classes
class Structure:
    def __init__(self,x,y,x_vel,y_vel,mass,colour,r,retention,friction):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = mass
        self.colour = colour
        self.r = r
        self.retention = retention
        self.friction = friction
        self.selected = False


    def move(self,pos,mouse_down):
        if self.shape.collidepoint(pos) and mouse_down:
            self.selected = True
        elif not mouse_down:
            self.selected = False

    def updatePosition(self,pos):
        if not self.selected:

            if abs(self.x_vel) < bounce_stop:
                self.x_vel = 0
            if abs(self.y_vel) < bounce_stop:
                self.y_vel = 0


            if 0 < self.x + self.x_vel < WIDTH:
                self.x += self.x_vel
            else:
                self.x = max(self.r, min(WIDTH - self.r, self.x))

            if 0 < self.y + self.y_vel < HEIGHT:
                self.y += self.y_vel
            else:
                self.y = max(self.r, min(HEIGHT - self.r, self.y))
        else:
            self.x = pos[0]
            self.y = pos[1]

# Ball (circle) shape
class Particle(Structure):
    def __init__(self,x,y,x_vel,y_vel,mass,colour,r,retention,friction):
        super().__init__(x,y,x_vel,y_vel,mass,colour,r,retention,friction)
        self.shape = ''

    def draw(self):
        self.shape = pygame.draw.circle(screen,self.colour,(int(self.x),int(self.y)),self.r)

    def get_bounds(self):
        return "circle", self.x, self.y, self.r


# Draws the outer boundaries of the screen
def walls():
    upper = pygame.draw.line(screen,'white',(0,0),(WIDTH,0),5)
    lower = pygame.draw.line(screen,'white',(0,HEIGHT),(WIDTH,HEIGHT),5)
    left = pygame.draw.line(screen,'white',(0,0),(0,HEIGHT),5)
    right = pygame.draw.line(screen,'white',(WIDTH,0),(WIDTH,HEIGHT),5)

# Calculates the vector for mouse movement
def vector(mouse_trajectory):
    start = mouse_trajectory[0][0],mouse_trajectory[1][1]
    end = mouse_trajectory[-1][0],mouse_trajectory[-1][1]

    delta_x = 0
    delta_y = 0

    if len(mouse_trajectory)>10:
        delta_x = (end[0]-start[0])/20
        delta_y = (end[1]-start[1])/20
    return delta_x,delta_y


def check_collision(obj1, obj2):
    dx = obj2.x - obj1.x
    dy = obj2.y - obj1.y
    distance = (dx**2 + dy**2)**0.5

    if distance < obj1.r + obj2.r:

        if distance == 0:
            normal = [1, 0]
        else:
            normal = [dx/distance, dy/distance]

        overlap = obj1.r + obj2.r - distance
        obj1.x -= overlap * normal[0] / 2
        obj1.y -= overlap * normal[1] / 2
        obj2.x += overlap * normal[0] / 2
        obj2.y += overlap * normal[1] / 2


        rel_vel_x = obj2.x_vel - obj1.x_vel
        rel_vel_y = obj2.y_vel - obj1.y_vel
        rel_vel_normal = rel_vel_x * normal[0] + rel_vel_y * normal[1]

        if rel_vel_normal < 0:

            impulse = -(1 + min(obj1.retention, obj2.retention)) * rel_vel_normal
            impulse /= 1/obj1.mass + 1/obj2.mass


            obj1.x_vel -= (impulse / obj1.mass) * normal[0]
            obj1.y_vel -= (impulse / obj1.mass) * normal[1]
            obj2.x_vel += (impulse / obj2.mass) * normal[0]
            obj2.y_vel += (impulse / obj2.mass) * normal[1]

    for obj in [obj1, obj2]:
        obj.x = max(obj.r, min(WIDTH - obj.r, obj.x))
        obj.y = max(obj.r, min(HEIGHT - obj.r, obj.y))



# Creating objects 
item_list = []

mouse_trajectory = []

# Main
running = True
while running:
    pos = pygame.mouse.get_pos()
    mouse_trajectory.append(pos)
    mouse_down = pygame.mouse.get_pressed()[0]
    if len(mouse_trajectory)>20:
        mouse_trajectory.pop(0)

    clock.tick(60)
    screen.fill((0,0,0))

    walls()
   
    for i,b in enumerate(item_list):
        b.draw()
        b.updatePosition(pos)
        b.move(pos,mouse_down)
        for c in range(i+1,len(item_list)):
            check_collision(b,item_list[c])

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            active = True
        if event.type == pygame.MOUSEBUTTONUP:
            active = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                new_ball = Particle(
                    np.random.randint(50, WIDTH-50),
                    np.random.randint(50, HEIGHT//2),
                    np.random.randint(-3, 3),
                    0,
                    10,
                    (np.random.randint(100, 255), np.random.randint(100, 255), np.random.randint(100, 255)),
                    20,
                    0.8,
                    0.05
                )
                item_list.append(new_ball)

    pygame.display.update()

pygame.quit()