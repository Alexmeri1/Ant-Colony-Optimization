#the basic idea behind the ants is the following:
#They have an angle (a direction), and a speed (probably a constant)
# they leave a constant pheramon trial behind them
#their goal is to gather food and bring it back
import math
import random
from collections import deque
from time import sleep
import pygame
# Initialize Pygame
pygame.init()

# Set up the display
screen_info = pygame.display.Info()  # Gets screen's resolution
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Rectangles")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
YELLOW = (255,222,33)

center_of_screen_x , center_of_screen_y = WIDTH / 2, HEIGHT / 2

class Food:

    def __init__(self,x ,y, r):
        self.x = x
        self.y = y
        self.radius = r
        self.color = YELLOW

    def draw(self,surface):
        pygame.draw.circle(surface, self.color, (self.x,self.y) , self.radius)

    def getCircleCenter(self):
        return self.x,self.y

    def collides_with_ant(self, ant):
        # Get the ant's bounding box
        ant_rect = ant.get_rect()

        # Find the closest point on the rectangle to the circle's center
        closest_x = max(ant_rect.left, min(self.x, ant_rect.right))
        closest_y = max(ant_rect.top, min(self.y, ant_rect.bottom))

        # Calculate the distance between the circle's center and the closest point
        dx = self.x - closest_x
        dy = self.y - closest_y
        distance = math.hypot(dx, dy)

        # Check if the distance is less than the circle's radius
        return distance < self.radius


class Ant:

    def __init__(self,angle,x,y):
        self.x = x  #x position on map
        self.y = y  #y position on map
        self.angle = angle #angle ant facing
        self.color = BLACK #color
        self.speed = 8 #speed of the ant
        self.width, self.height = 10, 20
        # Trail: deque to store (x, y, alpha) with max length
        self.trail = deque(maxlen=1000)  # Adjust maxlen for trail length
        self.turn_cooldown = 0
        self.sleep_cooldown = 0

    def get_rect(self):
        # Return a pygame.Rect representing the ant's bounding box
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_next_coordinates(self):
        deltaX = math.cos(self.angle * math.pi / 180) * self.speed
        deltaY = math.sin(self.angle * math.pi / 180) * self.speed
        return self.x + deltaX, self.y + deltaY

    def move(self, food):

        if self.sleep_cooldown > 0:
            self.sleep_cooldown -= 1
            return  # Don't move while stopped

        if food.collides_with_ant(self) and self.turn_cooldown <= 0:
            print("Food collected! Turning around...")
            self.sleep_cooldown = 60
            self.angle += 180 + random.randint(-50,50)  # Turn around
            self.turn_cooldown = 30  # Set cooldown to prevent immediate re-trigger

            # Update cooldown
        if self.turn_cooldown > 0:
            self.turn_cooldown -= 1


        self.trail.append((self.x,self.y,255))
        possible_x,possible_y = self.get_next_coordinates()

        if (possible_x > WIDTH or possible_x < 0 or possible_y > HEIGHT or possible_y < 0):
            self.angle += 180 + random.randint(-50,50)
            self.x , self.y = self.get_next_coordinates()

        self.x, self.y = self.get_next_coordinates()

    def draw(self, surface):

        for i, (trail_x,trail_y,alpha) in enumerate(reversed(self.trail)):

            fade_alpha = int(255 * (0.97 ** i))  # 0.97 controls fade rate
            if fade_alpha > 0:  # Only draw if visible
                trail_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                trail_surface.fill((*BLUE, fade_alpha))
                surface.blit(trail_surface, (trail_x, trail_y))


        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

ants = [Ant(random.randint(1,360),random.randint(1,WIDTH),random.randint(1,HEIGHT)) for _ in range(30)]
foods = [Food(random.randint(1,WIDTH) , random.randint(1,HEIGHT), 50 ) for _ in range(3)]

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
            running = False

    for food in foods:
        food.draw(screen)

    for ant in ants:
        for food in foods:
            ant.move(food)

    for ant in ants:
        ant.draw(screen)
        # Update the display


    pygame.display.flip()

    # Control frame rate
    clock.tick(60)  # 60 FPS

# Quit Pygame
pygame.quit()