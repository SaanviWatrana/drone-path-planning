import pygame

class Drone:
    def __init__(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.cell_size = cell_size

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (0, 0, 255),
            (int(self.x), int(self.y)),
            10
        )