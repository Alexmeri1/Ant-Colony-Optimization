import pygame
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Set window to match screen resolution
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ants with Trails")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Creature (Ant) class
class Creature:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])
        self.color = BLUE
        self.trail = deque(maxlen=100)  # Longer trail

    def move(self):
        self.trail.append((self.x, self.y, 255))
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x + self.width > WIDTH or self.x < 0:
            self.speed_x = -self.speed_x
        if self.y + self.height > HEIGHT or self.y < 0:
            self.speed_y = -self.speed_y

    def draw(self, surface):
        # Draw the trail first (bottom layer)
        for i, (trail_x, trail_y, alpha) in enumerate(reversed(self.trail)):
            fade_alpha = int(255 * (0.99 ** i))  # Slow fade with 0.99
            if fade_alpha > 0:  # Only draw if visible
                trail_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                trail_surface.fill((*BLUE, fade_alpha))
                surface.blit(trail_surface, (trail_x, trail_y))

        # Draw the ant last (top layer)
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

# Create creatures (ants)
creatures = [Creature(random.randint(0, WIDTH-30), random.randint(0, HEIGHT-30)) for _ in range(3)]

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for creature in creatures:
        creature.move()

    screen.fill(WHITE)
    for creature in creatures:
        creature.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()