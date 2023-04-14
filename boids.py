import pygame
import random
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the width and height of the screen [width, height]
WIDTH = 1920
HEIGHT = 1080
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

WEIGHT_ALIGNMENT = .1
WEIGHT_COHESION = .01
WEIGHT_SEPARATION = .1
SPEED_LIMIT = 3

pygame.display.set_caption("Boids")

# Define the class for each boid
class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-1, 1) * 10
        self.dy = random.uniform(-1, 1) * 10
        self.rgb = (random.randrange(256), random.randrange(256), random.randrange(256))

    def update(self, flock):
        # Compute the average velocity of nearby boids
        
        nearby_boids = [b for b in flock if b != self and math.dist((self.x, self.y), (b.x, b.y)) < 100]
        if nearby_boids:
            avg_dx = sum(b.dx for b in nearby_boids) / len(nearby_boids)
            avg_dy = sum(b.dy for b in nearby_boids) / len(nearby_boids)
            # moves 1/8th of the way towards the average velocity
            self.dx += (avg_dx - self.dx) * WEIGHT_ALIGNMENT
            self.dy += (avg_dy - self.dy) * WEIGHT_ALIGNMENT

        # Compute the average position of nearby boids
        if nearby_boids:
            avg_x = sum(b.x for b in nearby_boids) / len(nearby_boids)
            avg_y = sum(b.y for b in nearby_boids) / len(nearby_boids)
            # moves 1/8th of the way towards the average position
            self.dx += (avg_x - self.x) * WEIGHT_COHESION
            self.dy += (avg_y - self.y) * WEIGHT_COHESION

        # boids inside 50 pixel radius will move away from each other
        nearby_boids = [b for b in flock if b != self and math.dist((self.x, self.y), (b.x, b.y)) < 50]
        if nearby_boids:
            for b in nearby_boids:
                self.dx -= (b.x - self.x) * WEIGHT_SEPARATION
                self.dy -= (b.y - self.y) * WEIGHT_SEPARATION

        # normalize the velocity
        speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        self.dx *= SPEED_LIMIT / speed
        self.dy *= SPEED_LIMIT / speed

        # Update the boid's position
        self.x += self.dx
        self.y += self.dy

        # Wrap around the edges of the screen
        if self.x > WIDTH:
            self.x -= WIDTH
        elif self.x < 0:
            self.x += WIDTH
        if self.y > HEIGHT:
            self.y -= HEIGHT
        elif self.y < 0:
            self.y += HEIGHT

    def draw(self):
        # Compute the angle of the boid's velocity
        angle = math.atan2(self.dy, self.dx)

        # Compute the vertices of the quadrilateral
        length = 20  # Length of the arrow
        width = 8  # Width of the arrow
        x1, y1 = self.x + length * math.cos(angle), self.y + length * math.sin(angle)
        x2, y2 = self.x + width * math.cos(angle + 3 * math.pi / 4), self.y + width * math.sin(angle + 3 * math.pi / 4)
        x3, y3 = self.x + 0.05 * length * math.cos(angle), self.y + 0.05 * length * math.sin(angle)
        x4, y4 = self.x + width * math.cos(angle - 3 * math.pi / 4), self.y + width * math.sin(angle - 3 * math.pi / 4)

        # Draw the quadrilateral
        pygame.draw.polygon(screen, self.rgb, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

        # debug visibility radius
        #pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 50, width=1)
        


flock = []
for i in range(50):
    boid = Boid(random.randrange(WIDTH), random.randrange(HEIGHT))
    flock.append(boid)

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            boid = Boid(x, y)
            flock.append(boid)

    for boid in flock:
        boid.update(flock)

    screen.fill(BLACK)
    for boid in flock:
        boid.draw()
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
