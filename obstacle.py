import pygame
import random

class Obstacle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (220, 50, 50)

        # movement velocity (NEW)
        self.vx = random.choice([-40, -30, 30, 40])
        self.vy = random.choice([-40, -30, 30, 40])

    def update(self, dt, width, height):
        self.x += self.vx * dt
        self.y += self.vy * dt

        # bounce logic (keep inside screen)
        if self.x <= 0 or self.x >= width - self.size:
            self.vx *= -1

        if self.y <= 0 or self.y >= height - self.size:
            self.vy *= -1

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (int(self.x), int(self.y), self.size, self.size)
        )