import pygame

class Obstacle:

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (220, 50, 50)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.y, self.size, self.size)
        )

    def get_grid_position(self, cell_size):
        col = self.x // cell_size
        row = self.y // cell_size
        return int(row), int(col)